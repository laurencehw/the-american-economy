"""Tooling for keeping the manuscript's numbers current.

The manuscript states a reference year for every table and names the source
series beneath it. That makes the annual data refresh enumerable: this package
reads those declarations, fetches the corresponding series, and reports where
the book and the source disagree.

Nothing here edits the manuscript. The output is a report for a human to act on.
"""

__all__ = ["inventory", "registry", "sources", "report"]
