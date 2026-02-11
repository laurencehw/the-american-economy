#!/usr/bin/env python3
"""Build a PDF of The American Economy textbook from GitBook markdown sources."""

import os
import re
import subprocess
import sys

BOOK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "book")

# Chapter order from SUMMARY.md
CHAPTERS = [
    "README.md",
    "how-to-use.md",
    "part1/ch01-economy-in-numbers.md",
    "part1/ch02-how-it-fits.md",
    "part1/ch03-geography.md",
    "part1/interlude-inequality.md",
    "part2/ch04-government.md",
    "part2/ch05-real-estate.md",
    "part2/ch06-healthcare.md",
    "part2/ch07-professional-services.md",
    "part2/ch08-finance-insurance.md",
    "part2/ch09-manufacturing.md",
    "part2/ch10-retail-wholesale.md",
    "part2/ch11-tech-media.md",
    "part2/ch12-transportation.md",
    "part2/ch13-construction.md",
    "part2/ch14-energy.md",
    "part2/ch15-education.md",
    "part2/ch16-agriculture.md",
    "part2/ch17-leisure-hospitality.md",
    "part3/ch18-how-finance-works.md",
    "part3/ch19-capital-markets.md",
    "part3/ch20-corporate-finance.md",
    "part4/ch21-trade.md",
    "part4/ch22-supply-chains.md",
    "part5/ch23-northeast.md",
    "part5/ch24-sunbelt.md",
    "part5/ch25-midwest.md",
    "part5/ch26-west.md",
    "part5/ch27-rural.md",
    "part6/ch28-federal-governance.md",
    "part6/ch29-trade-associations.md",
    "part6/ch30-labor.md",
    "part7/ch31-perspective.md",
    "part7/ch32-shock-transmission.md",
    "appendices/appendix-a-data-sources.md",
    "appendices/appendix-b-bea-reference.md",
    "appendices/appendix-c-naics-codes.md",
    "appendices/appendix-d-glossary.md",
]

# Part headers to insert before specific chapters
PART_HEADERS = {
    "part1/ch01-economy-in-numbers.md": "# Part I: The Shape of the Economy\n\n\\newpage\n\n",
    "part2/ch04-government.md": "# Part II: The Sectors\n\n\\newpage\n\n",
    "part3/ch18-how-finance-works.md": "# Part III: The Financial Architecture\n\n\\newpage\n\n",
    "part4/ch21-trade.md": "# Part IV: Trade and Global Linkages\n\n\\newpage\n\n",
    "part5/ch23-northeast.md": "# Part V: Regional Economies\n\n\\newpage\n\n",
    "part6/ch28-federal-governance.md": "# Part VI: Institutions and Governance\n\n\\newpage\n\n",
    "part7/ch31-perspective.md": "# Part VII: Conclusion\n\n\\newpage\n\n",
    "appendices/appendix-a-data-sources.md": "# Appendices\n\n\\newpage\n\n",
}


def preprocess_markdown(content, chapter_path):
    """Convert GitBook-specific syntax to pandoc-compatible markdown."""

    # Resolve image paths relative to book directory
    chapter_dir = os.path.dirname(chapter_path)

    def fix_img_path(match):
        full_tag = match.group(0)
        src_match = re.search(r'src="([^"]*)"', full_tag)
        if src_match:
            src = src_match.group(1)
            # Convert relative path to absolute path from book dir
            abs_path = os.path.normpath(os.path.join(BOOK_DIR, chapter_dir, src))
            full_tag = full_tag.replace(src_match.group(0), f'src="{abs_path}"')
        return full_tag

    content = re.sub(r'<img\s[^>]*>', fix_img_path, content)

    # Convert {% hint style="info" %} ... {% endhint %} to blockquotes
    def convert_hint(match):
        style = match.group(1)
        body = match.group(2).strip()
        prefix_map = {
            "info": "**\u2139\ufe0f Info:**",
            "warning": "**\u26a0\ufe0f Note:**",
            "success": "**\u2705 Key Point:**",
            "danger": "**\u274c Warning:**",
        }
        prefix = prefix_map.get(style, "**Note:**")
        # Convert to blockquote
        lines = body.split("\n")
        quoted = "\n".join(f"> {line}" for line in lines)
        return f"> {prefix}\n>\n{quoted}\n"

    content = re.sub(
        r'{%\s*hint\s+style="(\w+)"\s*%}(.*?){%\s*endhint\s*%}',
        convert_hint,
        content,
        flags=re.DOTALL,
    )

    # Convert HTML figures to markdown images for better pandoc handling
    def convert_figure(match):
        figure_html = match.group(0)
        img_match = re.search(r'<img\s[^>]*src="([^"]*)"[^>]*>', figure_html)
        caption_match = re.search(
            r"<figcaption>(.*?)</figcaption>", figure_html, re.DOTALL
        )

        # Clean caption: remove HTML links, keep text
        caption = ""
        if caption_match:
            caption = caption_match.group(1)
            caption = re.sub(r"<a[^>]*>([^<]*)</a>", r"\1", caption)
            caption = re.sub(r"<[^>]+>", "", caption)
            caption = caption.strip()

        if img_match:
            src = img_match.group(1)

            # If the image file doesn't exist, render caption as a blockquote
            if not os.path.exists(src):
                if caption:
                    return f"\n> *[Figure: {caption}]*\n"
                return ""

            # Use pandoc's implicit figure syntax
            return f"\n![{caption}]({src})\n"

        return figure_html

    content = re.sub(
        r"<figure>.*?</figure>", convert_figure, content, flags=re.DOTALL
    )

    # Remove any remaining style attributes from HTML
    content = re.sub(r'\s*style="[^"]*"', "", content)

    # Remove interactive-only links that won't work in PDF
    content = re.sub(
        r"\[View interactive[^\]]*\]\([^)]*\)", "(see online interactive version)", content
    )

    return content


def build_combined_markdown():
    """Combine all chapters into a single markdown file with preprocessing."""
    combined = []

    for chapter in CHAPTERS:
        filepath = os.path.join(BOOK_DIR, chapter)
        if not os.path.exists(filepath):
            print(f"WARNING: Missing chapter: {filepath}", file=sys.stderr)
            continue

        # Add part header if applicable
        if chapter in PART_HEADERS:
            combined.append(PART_HEADERS[chapter])

        with open(filepath, "r") as f:
            content = f.read()

        content = preprocess_markdown(content, chapter)

        # Add page break between chapters
        combined.append(content)
        combined.append("\n\n\\newpage\n\n")

    return "\n".join(combined)


def main():
    print("Building PDF of The American Economy...")

    # Step 1: Combine and preprocess
    print("  Combining and preprocessing chapters...")
    combined_md = build_combined_markdown()

    combined_path = os.path.join(BOOK_DIR, "_build_combined.md")
    with open(combined_path, "w") as f:
        f.write(combined_md)

    # Step 2: Build PDF with pandoc
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "the-american-economy.pdf"
    )

    print("  Running pandoc...")
    cmd = [
        "pandoc",
        combined_path,
        "-o",
        output_path,
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2",
        "-V",
        "geometry:margin=1in",
        "-V",
        "documentclass=report",
        "-V",
        'title=The American Economy: A Structural Geography',
        "-V",
        "fontsize=11pt",
        "-V",
        "linkcolor=blue",
        "-V",
        "urlcolor=blue",
        "-V",
        "toccolor=black",
        "-V",
        "mainfont=DejaVu Serif",
        "-V",
        "sansfont=DejaVu Sans",
        "-V",
        "monofont=DejaVu Sans Mono",
        "--columns=80",
        "--wrap=auto",
        "-f",
        "markdown+raw_html+implicit_figures+pipe_tables+raw_tex",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Clean up temp file
    os.remove(combined_path)

    if result.returncode != 0:
        print(f"ERROR: pandoc failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  PDF generated: {output_path} ({file_size:.1f} MB)")


if __name__ == "__main__":
    main()
