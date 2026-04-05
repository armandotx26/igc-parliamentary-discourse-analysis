#!/usr/bin/env python3
"""
igc_country_analyzer.py
------------------------
Analyze IGC corpus (JSONL) for country/region mentions using the
igc_world_gazetteer.json, producing CSV outputs and KWIC concordances.

Usage:
    python igc_country_analyzer.py igc_parla.jsonl --output-dir country_results
    python igc_country_analyzer.py file1.jsonl file2.jsonl --output-dir country_results
    python igc_country_analyzer.py --dir converted-corpora/ --output-dir country_results
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


# ---------------------------------------------------------------------------
# Regex helpers — match the same Unicode-safe word boundary as
# parla_full_genealogy.py:  (?<![^\W_])  means: not preceded by a word char
# (where word chars = \w minus underscore, i.e. letters+digits).
# ---------------------------------------------------------------------------

WB_LEFT  = r"(?<![^\W_])"   # Unicode-safe left boundary (zero-width)
WB_RIGHT = r"(?![^\W_])"    # Unicode-safe right boundary (zero-width)


def _escape(s: str) -> str:
    """re.escape with Icelandic special characters preserved (they are already
    unicode-safe in Python re when re.UNICODE is active)."""
    return re.escape(s)


def build_pattern(term: str) -> re.Pattern:
    """Build a compiled regex for a single term.

    Rules:
    - Multi-word terms (contain space/hyphen word boundary): case-folded
      substring matching with word boundaries on outer edges.
    - Single-word terms of 4+ chars: word boundary on both sides.
    - Short terms (2-3 chars): strict word boundaries on BOTH sides to
      avoid false positives.
    """
    stripped = term.strip()
    if not stripped:
        return None

    flags = re.IGNORECASE | re.UNICODE

    # Multi-word: require word boundaries only on outer edges
    if " " in stripped or "-" in stripped or len(stripped.split()) > 1:
        pat = WB_LEFT + _escape(stripped) + WB_RIGHT
        return re.compile(pat, flags)

    # Single word
    if len(stripped) >= 4:
        pat = WB_LEFT + _escape(stripped) + WB_RIGHT
        return re.compile(pat, flags)
    else:
        # Short (2-3 chars): strict word boundaries both sides
        pat = WB_LEFT + _escape(stripped) + WB_RIGHT
        return re.compile(pat, flags)


# ---------------------------------------------------------------------------
# Gazetteer loading
# ---------------------------------------------------------------------------

def load_gazetteer(gazetteer_path: str):
    """Load the JSON gazetteer and return a list of entry dicts, each with:
      - key: unique identifier string
      - english_name
      - icelandic_name
      - region
      - subregion
      - patterns: list of compiled re.Pattern objects
    """
    with open(gazetteer_path, encoding="utf-8") as f:
        data = json.load(f)

    entries = []

    for country in data.get("countries", []):
        key = country.get("iso_code", country["english_name"])
        terms = set()

        # Primary icelandic name and variants
        iname = country.get("icelandic_name", "")
        if iname:
            terms.add(iname)

        for v in country.get("icelandic_variants", []):
            if v:
                terms.add(v)

        # Demonym stems
        for stem in country.get("demonym_stems", []):
            if stem:
                terms.add(stem)

        patterns = []
        for t in terms:
            p = build_pattern(t)
            if p:
                patterns.append(p)

        entries.append({
            "key": key,
            "english_name": country.get("english_name", ""),
            "icelandic_name": iname,
            "region": country.get("region", ""),
            "subregion": country.get("subregion", ""),
            "entry_type": "country",
            "patterns": patterns,
            "terms": sorted(terms),
        })

    for region in data.get("regions", []):
        key = region.get("code", region["english_name"])
        terms = set()

        iname = region.get("icelandic_name", "")
        if iname:
            terms.add(iname)

        for v in region.get("icelandic_variants", []):
            if v:
                terms.add(v)

        patterns = []
        for t in terms:
            p = build_pattern(t)
            if p:
                patterns.append(p)

        entries.append({
            "key": key,
            "english_name": region.get("english_name", ""),
            "icelandic_name": iname,
            "region": region.get("english_name", ""),
            "subregion": "",
            "entry_type": "region",
            "patterns": patterns,
            "terms": sorted(terms),
        })

    for sup in data.get("supranational", []):
        key = sup.get("code", sup["english_name"])
        terms = set()

        for n in sup.get("icelandic_names", []):
            if n:
                terms.add(n)

        patterns = []
        for t in terms:
            p = build_pattern(t)
            if p:
                patterns.append(p)

        entries.append({
            "key": key,
            "english_name": sup.get("english_name", ""),
            "icelandic_name": sup.get("icelandic_names", [""])[0] if sup.get("icelandic_names") else "",
            "region": "Supranational",
            "subregion": sup.get("type", ""),
            "entry_type": "supranational",
            "patterns": patterns,
            "terms": sorted(terms),
        })

    return entries


# ---------------------------------------------------------------------------
# Document I/O
# ---------------------------------------------------------------------------

def iter_documents(file_paths):
    """Yield (year, text, source_path) for each JSONL line in file_paths."""
    for fpath in file_paths:
        with open(fpath, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    doc = json.loads(line)
                except json.JSONDecodeError:
                    continue

                text = doc.get("document") or doc.get("text") or ""
                if not text:
                    continue

                # Extract year: try 'year' key, then date-like strings
                year = doc.get("year")
                if not year:
                    for k in ("date", "datum", "created", "published"):
                        val = doc.get(k, "")
                        if val:
                            m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", str(val))
                            if m:
                                year = int(m.group(1))
                                break
                if year:
                    try:
                        year = int(year)
                    except (ValueError, TypeError):
                        year = None

                yield year, text, str(fpath)


def collect_file_paths(args):
    """Collect all JSONL/JSON file paths from positional args or --dir."""
    paths = []

    if args.dir:
        base = Path(args.dir)
        for ext in ("*.jsonl", "*.json"):
            paths.extend(sorted(base.rglob(ext)))
    else:
        for pattern in args.files:
            p = Path(pattern)
            if p.is_file():
                paths.append(p)
            else:
                # Treat as glob pattern
                import glob as glob_mod
                matched = glob_mod.glob(pattern, recursive=True)
                paths.extend(Path(m) for m in sorted(matched) if Path(m).is_file())

    return [str(p) for p in paths]


# ---------------------------------------------------------------------------
# KWIC concordance helpers
# ---------------------------------------------------------------------------

CONTEXT_CHARS = 80  # characters on each side for KWIC


def extract_kwic(text: str, pattern: re.Pattern, label: str, max_hits: int = 20):
    """Return up to max_hits KWIC lines (left, match, right)."""
    results = []
    for m in pattern.finditer(text):
        if len(results) >= max_hits:
            break
        start = max(0, m.start() - CONTEXT_CHARS)
        end = min(len(text), m.end() + CONTEXT_CHARS)
        left = text[start:m.start()].replace("\n", " ").replace("\t", " ")
        word = m.group(0)
        right = text[m.end():end].replace("\n", " ").replace("\t", " ")
        results.append((left, word, right))
    return results


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def analyze(file_paths, entries, output_dir: str, max_kwic: int = 20):
    os.makedirs(output_dir, exist_ok=True)

    # Accumulate data structures
    # mentions_by_year[year][key] = document count (binary)
    mentions_by_year = defaultdict(lambda: defaultdict(int))
    total_mentions = defaultdict(int)

    # For region aggregation: country_to_region[key] -> region string
    country_to_region = {e["key"]: e["region"] for e in entries}
    # region_mentions_by_year[year][region] = doc count
    region_mentions_by_year = defaultdict(lambda: defaultdict(int))

    # Co-occurrence: cooccur[key1][key2] += 1
    cooccur = defaultdict(lambda: defaultdict(int))

    # KWIC concordances: kwic_data[key] = list of (left, word, right)
    kwic_data = defaultdict(list)

    total_docs = 0
    skipped = 0

    for year, text, source in iter_documents(file_paths):
        total_docs += 1

        if total_docs % 10000 == 0:
            print(f"  Processed {total_docs:,} documents...", flush=True)

        if not text:
            skipped += 1
            continue

        # For each entry, check if it appears in this document (binary)
        doc_hits = set()  # keys found in this doc

        for entry in entries:
            key = entry["key"]
            found_in_doc = False

            for pat in entry["patterns"]:
                m = pat.search(text)
                if m:
                    found_in_doc = True
                    # Collect KWIC if under limit
                    if len(kwic_data[key]) < max_kwic:
                        kwic_data[key].append((
                            text[max(0, m.start()-CONTEXT_CHARS):m.start()].replace("\n"," "),
                            m.group(0),
                            text[m.end():min(len(text), m.end()+CONTEXT_CHARS)].replace("\n"," ")
                        ))
                    break  # one match per entry per doc is enough for binary

            if found_in_doc:
                doc_hits.add(key)
                year_key = year if year else "unknown"
                mentions_by_year[year_key][key] += 1
                total_mentions[key] += 1

                # Region aggregation from country
                region = country_to_region.get(key, "")
                if region:
                    region_mentions_by_year[year_key][region] += 1

        # Co-occurrence (among found keys)
        doc_hits_list = sorted(doc_hits)
        for i, k1 in enumerate(doc_hits_list):
            for k2 in doc_hits_list[i+1:]:
                cooccur[k1][k2] += 1
                cooccur[k2][k1] += 1

    print(f"\nProcessed {total_docs:,} total documents ({skipped:,} skipped — no text).")

    # ------------------------------------------------------------------
    # Output 1: country_mentions_by_year.csv
    # ------------------------------------------------------------------
    all_years = sorted(y for y in mentions_by_year.keys() if y != "unknown")
    if "unknown" in mentions_by_year:
        all_years.append("unknown")

    all_keys = [e["key"] for e in entries]

    out1 = os.path.join(output_dir, "country_mentions_by_year.csv")
    print(f"Writing {out1}...")
    with open(out1, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["year"] + all_keys)
        for yr in all_years:
            row = [yr] + [mentions_by_year[yr].get(k, 0) for k in all_keys]
            writer.writerow(row)

    # ------------------------------------------------------------------
    # Output 2: country_mentions_total.csv
    # ------------------------------------------------------------------
    key_to_entry = {e["key"]: e for e in entries}
    ranked = sorted(total_mentions.items(), key=lambda x: x[1], reverse=True)

    out2 = os.path.join(output_dir, "country_mentions_total.csv")
    print(f"Writing {out2}...")
    with open(out2, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "key", "english_name", "icelandic_name",
                          "region", "subregion", "entry_type", "total_docs"])
        for rank, (key, count) in enumerate(ranked, 1):
            e = key_to_entry.get(key, {})
            writer.writerow([
                rank, key, e.get("english_name", ""), e.get("icelandic_name", ""),
                e.get("region", ""), e.get("subregion", ""), e.get("entry_type", ""),
                count
            ])

    # Include entries with 0 mentions
    mentioned_keys = {k for k, _ in ranked}
    with open(out2, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        rank_offset = len(ranked) + 1
        for i, e in enumerate(entries):
            if e["key"] not in mentioned_keys:
                writer.writerow([
                    rank_offset + i, e["key"], e.get("english_name", ""),
                    e.get("icelandic_name", ""), e.get("region", ""),
                    e.get("subregion", ""), e.get("entry_type", ""), 0
                ])

    # ------------------------------------------------------------------
    # Output 3: region_mentions_by_year.csv
    # ------------------------------------------------------------------
    all_regions = set()
    for yr_data in region_mentions_by_year.values():
        all_regions.update(yr_data.keys())
    all_regions = sorted(all_regions)

    out3 = os.path.join(output_dir, "region_mentions_by_year.csv")
    print(f"Writing {out3}...")
    with open(out3, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["year"] + all_regions)
        for yr in all_years:
            row = [yr] + [region_mentions_by_year[yr].get(r, 0) for r in all_regions]
            writer.writerow(row)

    # ------------------------------------------------------------------
    # Output 4: country_cooccurrence_top50.csv
    # ------------------------------------------------------------------
    top50_keys = [k for k, _ in ranked[:50]]

    out4 = os.path.join(output_dir, "country_cooccurrence_top50.csv")
    print(f"Writing {out4}...")
    with open(out4, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + top50_keys)
        for k1 in top50_keys:
            row = [k1] + [cooccur[k1].get(k2, 0) for k2 in top50_keys]
            writer.writerow(row)

    # ------------------------------------------------------------------
    # Output 5: country_concordances.tsv
    # ------------------------------------------------------------------
    out5 = os.path.join(output_dir, "country_concordances.tsv")
    print(f"Writing {out5}...")
    with open(out5, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["key", "english_name", "left_context", "keyword", "right_context"])
        for e in entries:
            key = e["key"]
            ename = e.get("english_name", "")
            for (left, word, right) in kwic_data.get(key, [])[:max_kwic]:
                writer.writerow([key, ename, left.strip(), word, right.strip()])

    # ------------------------------------------------------------------
    # Summary: top 30
    # ------------------------------------------------------------------
    print("\n" + "="*60)
    print("TOP 30 MOST MENTIONED COUNTRIES/REGIONS")
    print("="*60)
    print(f"{'Rank':<5} {'Key':<20} {'English Name':<30} {'Docs':>8}")
    print("-"*65)
    for rank, (key, count) in enumerate(ranked[:30], 1):
        e = key_to_entry.get(key, {})
        print(f"{rank:<5} {key:<20} {e.get('english_name',''):<30} {count:>8,}")

    print("\nDone. Output files:")
    for f in [out1, out2, out3, out4, out5]:
        size = os.path.getsize(f)
        print(f"  {f}  ({size:,} bytes)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="IGC Country/Region Mention Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Single file
  python igc_country_analyzer.py igc_parla.jsonl --output-dir country_results

  # Multiple files / globs
  python igc_country_analyzer.py igc_parla.jsonl igc_news/*.jsonl --output-dir country_results

  # Directory (recursive)
  python igc_country_analyzer.py --dir converted-corpora/ --output-dir country_results
""")

    parser.add_argument(
        "files", nargs="*",
        help="JSONL file(s) or glob patterns to analyze"
    )
    parser.add_argument(
        "--dir", metavar="DIRECTORY",
        help="Recursively process all .jsonl/.json files in this directory"
    )
    parser.add_argument(
        "--output-dir", "-o", default="country_results", metavar="DIR",
        help="Directory for output CSV/TSV files (default: country_results)"
    )
    parser.add_argument(
        "--gazetteer", default=None, metavar="PATH",
        help="Path to igc_world_gazetteer.json (default: same directory as this script)"
    )
    parser.add_argument(
        "--max-kwic", type=int, default=20, metavar="N",
        help="Maximum KWIC concordance lines per entry (default: 20)"
    )

    args = parser.parse_args()

    # Resolve gazetteer path
    if args.gazetteer:
        gaz_path = args.gazetteer
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gaz_path = os.path.join(script_dir, "igc_world_gazetteer.json")
        if not os.path.exists(gaz_path):
            # Try current working directory
            gaz_path = "igc_world_gazetteer.json"

    if not os.path.exists(gaz_path):
        print(f"ERROR: Gazetteer not found at '{gaz_path}'.", file=sys.stderr)
        print("Use --gazetteer PATH to specify the location.", file=sys.stderr)
        sys.exit(1)

    # Collect input files
    if not args.files and not args.dir:
        parser.print_help()
        sys.exit(1)

    file_paths = collect_file_paths(args)

    if not file_paths:
        print("ERROR: No input files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading gazetteer from: {gaz_path}")
    entries = load_gazetteer(gaz_path)
    total_patterns = sum(len(e["patterns"]) for e in entries)
    print(f"  Loaded {len(entries)} entries, {total_patterns} compiled patterns.")

    print(f"\nInput files: {len(file_paths)}")
    for fp in file_paths[:5]:
        print(f"  {fp}")
    if len(file_paths) > 5:
        print(f"  ... and {len(file_paths)-5} more")

    print(f"\nOutput directory: {args.output_dir}")
    print(f"Max KWIC per entry: {args.max_kwic}")
    print("\nStarting analysis...\n")

    analyze(file_paths, entries, args.output_dir, max_kwic=args.max_kwic)


if __name__ == "__main__":
    main()
