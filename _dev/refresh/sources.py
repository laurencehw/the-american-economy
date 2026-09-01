"""Fetch economic series from public APIs.

Two providers are supported:

* ``fred``  — St. Louis Fed. Uses the public CSV endpoint (``fredgraph.csv``),
  which needs no API key. Set ``FRED_API_KEY`` to use the JSON API instead,
  which is more reliable under load.
* ``bls``   — Bureau of Labor Statistics. The v1 public API needs no key but is
  limited to 25 queries a day; set ``BLS_API_KEY`` for the v2 API.

Responses are cached on disk so a report can be regenerated without re-fetching,
and so a run with no network can still say what it knows.
"""
from __future__ import annotations

import csv
import io
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
CACHE_TTL = timedelta(days=1)
TIMEOUT = 30
USER_AGENT = "the-american-economy/refresh_data (+https://github.com/laurencehw/the-american-economy)"


class FetchError(RuntimeError):
    """A series could not be retrieved."""


@dataclass
class Observation:
    period: str      # "2024" or "2024-06"
    value: float


@dataclass
class Series:
    provider: str
    series_id: str
    observations: list[Observation]
    from_cache: bool = False

    def annual(self) -> dict[int, float]:
        """Collapse observations to a mean per calendar year.

        Averaging is right for a rate or a seasonally adjusted annual rate, which
        is what every series in the registry is. A registry entry needing a
        year-end level rather than a mean should say so via its ``reducer``.
        """
        buckets: dict[int, list[float]] = {}
        for obs in self.observations:
            buckets.setdefault(int(obs.period[:4]), []).append(obs.value)
        return {year: sum(v) / len(v) for year, v in buckets.items()}

    def latest_complete_year(self, today: date | None = None) -> int | None:
        """The most recent year with a full set of observations.

        A partial current year would compare unfairly against an annual figure,
        so it is excluded unless the series is itself annual.
        """
        annual = self.annual()
        if not annual:
            return None
        current = (today or date.today()).year
        candidates = [y for y in annual if y < current]
        return max(candidates) if candidates else max(annual)


def _cache_path(provider: str, series_id: str) -> Path:
    return CACHE_DIR / provider / f"{series_id}.json"


def _read_cache(provider: str, series_id: str, max_age: timedelta | None) -> Series | None:
    path = _cache_path(provider, series_id)
    if not path.exists():
        return None
    if max_age is not None:
        age = time.time() - path.stat().st_mtime
        if age > max_age.total_seconds():
            return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return Series(
        provider=provider,
        series_id=series_id,
        observations=[Observation(**o) for o in payload["observations"]],
        from_cache=True,
    )


def _write_cache(series: Series) -> None:
    path = _cache_path(series.provider, series.series_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "series_id": series.series_id,
                "retrieved": date.today().isoformat(),
                "observations": [{"period": o.period, "value": o.value} for o in series.observations],
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _get(url: str, data: bytes | None = None, headers: dict[str, str] | None = None) -> bytes:
    request = urllib.request.Request(url, data=data, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.read()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        raise FetchError(f"{url}: {exc}") from exc


def _fetch_fred(series_id: str) -> Series:
    key = os.environ.get("FRED_API_KEY")
    if key:
        url = (
            "https://api.stlouisfed.org/fred/series/observations"
            f"?series_id={series_id}&api_key={key}&file_type=json"
        )
        payload = json.loads(_get(url))
        observations = [
            Observation(period=o["date"][:7], value=float(o["value"]))
            for o in payload.get("observations", [])
            if o.get("value") not in (None, ".", "")
        ]
    else:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        rows = list(csv.reader(io.StringIO(_get(url).decode("utf-8"))))
        if not rows:
            raise FetchError(f"FRED returned no rows for {series_id}")
        observations = []
        for row in rows[1:]:
            if len(row) < 2 or row[1] in (".", ""):
                continue
            observations.append(Observation(period=row[0][:7], value=float(row[1])))
    if not observations:
        raise FetchError(f"FRED returned no usable observations for {series_id}")
    return Series(provider="fred", series_id=series_id, observations=observations)


def _fetch_bls(series_id: str, start_year: int, end_year: int) -> Series:
    key = os.environ.get("BLS_API_KEY")
    version = "v2" if key else "v1"
    body: dict[str, object] = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
    }
    if key:
        body["registrationkey"] = key
    payload = json.loads(
        _get(
            f"https://api.bls.gov/publicAPI/{version}/timeseries/data/",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
    )
    if payload.get("status") != "REQUEST_SUCCEEDED":
        raise FetchError(f"BLS: {payload.get('status')} {'; '.join(payload.get('message', []))}")
    results = payload.get("Results", {}).get("series", [])
    if not results:
        raise FetchError(f"BLS returned no series for {series_id}")
    observations = []
    for item in results[0].get("data", []):
        period = item["period"]
        if period.startswith("M") and period != "M13":
            key_period = f"{item['year']}-{period[1:]}"
        elif period in ("M13", "A01"):
            key_period = item["year"]
        else:
            continue
        observations.append(Observation(period=key_period, value=float(item["value"].replace(",", ""))))
    if not observations:
        raise FetchError(f"BLS returned no usable observations for {series_id}")
    return Series(provider="bls", series_id=series_id, observations=observations)


def fetch(provider: str, series_id: str, *, offline: bool = False,
          refresh: bool = False, years: int = 12) -> Series:
    """Return a series, from cache when possible.

    Three modes, in precedence order:

    * ``offline`` — never touches the network. Returns a cached copy of any age
      if one exists, and raises FetchError otherwise. Use where egress is
      blocked.
    * ``refresh`` — ignores the cache entirely and re-fetches.
    * default — uses the cache while it is within ``CACHE_TTL``, else fetches.
    """
    if offline:
        cached = _read_cache(provider, series_id, None)
        if cached is not None:
            return cached
        raise FetchError(f"offline and no cached copy of {provider}:{series_id}")

    if not refresh:
        cached = _read_cache(provider, series_id, CACHE_TTL)
        if cached is not None:
            return cached

    if provider == "fred":
        series = _fetch_fred(series_id)
    elif provider == "bls":
        this_year = date.today().year
        series = _fetch_bls(series_id, this_year - years, this_year)
    else:
        raise FetchError(f"unknown provider {provider!r}")
    _write_cache(series)
    return series
