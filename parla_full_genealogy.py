#!/usr/bin/env python3
"""
parla_full_genealogy.py — Comprehensive IGC-Parla Discourse Analyzer
=====================================================================
Targeted analysis of Icelandic parliamentary debates (1909–present)
across 15 discursive domains for genealogical discourse study.

Usage:
    python parla_full_genealogy.py /path/to/IGC-Parla.jsonl [--output-dir ./results]
"""

import re
import json
import csv
import sys
import os
import argparse
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# 1.  DOMAIN DEFINITIONS
# ---------------------------------------------------------------------------
# Each domain is a dict with:
#   "name"   : human-readable label
#   "stems"  : list of stem strings (single or multi-word)
# Matching rules (applied after lowercasing):
#   - multi-word stems  → plain substring search (lowercased text)
#   - single-word stems → r'\b' + re.escape(stem) with re.IGNORECASE
# ---------------------------------------------------------------------------

DOMAINS = [
    {
        "id": "D01_immigration",
        "name": "Immigration / movement",
        "stems": [
            "innflytjend",
            "innflytjand",
            "aðflutning",
            "búseta erlend",
        ],
    },
    {
        "id": "D02_foreigners",
        "name": "Foreigners / alterity",
        "stems": [
            "útlending",
            "utlending",
            "erlend ríkisborgari",
            "erlent vinnuafl",
        ],
    },
    {
        "id": "D03_asylum",
        "name": "Asylum / refuge",
        "stems": [
            "hælisleit",
            "haelisleit",
            "flóttafólk",
            "flóttamenn",
            "flóttamaður",
            "flóttama",
            "alþjóðleg vernd",
            "umsókn um vernd",
        ],
    },
    {
        "id": "D04_border",
        "name": "Border / legal governance",
        "stems": [
            "landamær",
            "vegabréfsáritun",
            "dvalarleyf",
            "útlendingastofnun",
            "brottvísun",
            "brottvisun",
            "framsending",
        ],
    },
    {
        "id": "D05_security",
        "name": "Security / policing",
        "stems": [
            "almannaöryggi",
            "lögreglu",
            "logreglu",
            "ríkislögreglu",
            "glæp",
            "handtek",
            "ógn",
            "hryðjuverk",
            "ofbeldi",
            "fangels",
        ],
    },
    {
        "id": "D06_integration",
        "name": "Integration / welfare",
        "stems": [
            "aðlögun",
            "samþætting",
            "tungumálanám",
            "íslenskunám",
            "félagsþjónust",
            "félagslega þjónust",
            "vinnumarkaður",
            "vinnumarkað",
        ],
    },
    {
        "id": "D07_housing",
        "name": "Housing / quartering",
        "stems": [
            "húsnæði",
            "húsaleig",
            "húsaleigufrumvarp",
            "herbergi",
            "íbúð",
            "innvistun",
            "húsaskipan",
            "geymsluhús",
            "niðursetning",
            "niðursetningar",
            "friðhelgi heimil",
            "heimilisfriðu",
            "útburðarheimild",
            "utanhéraðsm",
            "innanhéraðsm",
        ],
    },
    {
        "id": "D08_morality",
        "name": "Morality / Ástandið",
        "stems": [
            "ástand",
            "siðferðis",
            "siðferðislögreglu",
            "lauslát",
            "varnarlaus",
            "kynferðis",
            "kynlíf",
            "vændi",
            "kleppjárnsreyk",
            "sauðárkrók",
        ],
    },
    {
        "id": "D09_poverty",
        "name": "Poverty / poor law",
        "stems": [
            "fátæk",
            "fátækra",
            "fátækling",
            "framfærslu",
            "framfærslulög",
            "framfærslusveit",
            "heimilislaus",
            "heimilisleysi",
            "urfam",
            "ftkra",
            "fátækrasjóð",
            "ómagar",
            "ómögul",
        ],
    },
    {
        "id": "D10_labour",
        "name": "Labour discipline / emergency economy",
        "stems": [
            "gengislög",
            "kaupgjald",
            "dýrtíð",
            "dýrtíðaruppbætur",
            "verkfall",
            "verkfalls",
            "gerðardóm",
            "kaupmálasamning",
            "verðtrygg",
            "launakröf",
            "vinnufriðu",
            "verkamenn",
            "verkalýð",
            "neyðarráðstaf",
        ],
    },
    {
        "id": "D11_racial",
        "name": "Racial terms / racialized language",
        "stems": [
            "negri",
            "negra",
            "neger",
            "svertingi",
            "svertingja",
            "blámaður",
            "blámann",
            "blökkumaður",
            "blökkumann",
            "litaður",
            "litað",
            "kynþátt",
            "þjóðern",
            "kínverj",
            "gyðing",
            "múslim",
            "sígaun",
        ],
    },
    {
        "id": "D12_military",
        "name": "Military / occupation",
        "stems": [
            "setulið",
            "setuliðs",
            "hernám",
            "hernaðar",
            "hersveit",
            "varnarsvæð",
            "varnarliðs",
            "varnarliði",
            "keflavík",
            "miðnesheiði",
            "bandaríkjaher",
            "brezkur her",
            "breska her",
        ],
    },
    {
        "id": "D13_gender",
        "name": "Women / gender / sexuality",
        "stems": [
            "kvenréttind",
            "kvennaréttind",
            "konur og",
            "kvenna",
            "stúlk",
            "mæðra",
            "barnsmóðir",
            "einstæð",
            "launabarn",
            "barnshafandi",
            "ólögleg",
        ],
    },
    {
        "id": "D14_identity",
        "name": "National identity / belonging",
        "stems": [
            "íslensk menning",
            "íslenskri menning",
            "þjóðleg",
            "þjóðlíkam",
            "hreinleik",
            "kynstofn",
            "norræn",
            "norðurgerman",
            "hvítra manna",
            "hvít",
        ],
    },
    {
        "id": "D15_welfare",
        "name": "Welfare state / social services",
        "stems": [
            "tryggingastofnun",
            "almannatrygging",
            "lífeyri",
            "sjúkratrygging",
            "barnabætur",
            "meðlag",
            "barnavernd",
            "félagsráðgjaf",
        ],
    },
]

# ---------------------------------------------------------------------------
# 2.  COMPILE PATTERNS
# ---------------------------------------------------------------------------

def _is_multiword(stem):
    """True if stem contains a space (multi-word phrase)."""
    return " " in stem.strip()


def compile_domain_patterns(domains):
    """
    Returns a dict keyed by domain id, mapping to a list of
    (stem_string, compiled_regex_or_None) tuples.
    For multi-word stems we use None as the regex; matching is done via
    plain lowercased substring search to avoid Unicode word-boundary issues.
    For single-word stems we compile r'\b' + re.escape(stem) with
    re.IGNORECASE | re.UNICODE.
    """
    compiled = {}
    for domain in domains:
        patterns = []
        for stem in domain["stems"]:
            if _is_multiword(stem):
                # Multi-word: substring match on lowercased text; no regex needed
                patterns.append((stem, None))
            else:
                pat = re.compile(
                    r"(?<![^\W_])" + re.escape(stem),
                    re.IGNORECASE | re.UNICODE,
                )
                patterns.append((stem, pat))
        compiled[domain["id"]] = patterns
    return compiled


def stem_matches(text, text_lower, stem, pattern):
    """
    Returns True if the stem matches anywhere in the text.
    Uses pattern (regex) for single-word stems, substring for multi-word.
    """
    if pattern is None:
        # multi-word substring
        return stem.lower() in text_lower
    else:
        return bool(pattern.search(text))


def find_match_positions(text, text_lower, stem, pattern):
    """
    Returns a list of (start, end) character positions for all matches.
    """
    positions = []
    if pattern is None:
        # multi-word: find all occurrences
        needle = stem.lower()
        start = 0
        while True:
            idx = text_lower.find(needle, start)
            if idx == -1:
                break
            positions.append((idx, idx + len(needle)))
            start = idx + 1
    else:
        for m in pattern.finditer(text):
            positions.append((m.start(), m.end()))
    return positions


# ---------------------------------------------------------------------------
# 3.  CONCORDANCE HELPERS
# ---------------------------------------------------------------------------

def extract_kwic(text, match_start, match_end, window=20):
    """
    Extract ±window tokens around the match.
    Tokenise by whitespace, find the token(s) containing the match,
    then return a KWIC triple (left_context, keyword, right_context).
    """
    tokens = text.split()
    # Rebuild token offsets
    offsets = []
    pos = 0
    for tok in tokens:
        idx = text.find(tok, pos)
        offsets.append((idx, idx + len(tok)))
        pos = idx + len(tok)

    # Find which token indices fall within the match
    match_toks = [
        i for i, (s, e) in enumerate(offsets)
        if s < match_end and e > match_start
    ]
    if not match_toks:
        return None

    first_tok = match_toks[0]
    last_tok = match_toks[-1]

    left_start = max(0, first_tok - window)
    right_end = min(len(tokens), last_tok + window + 1)

    left_ctx = " ".join(tokens[left_start:first_tok])
    keyword = " ".join(tokens[first_tok:last_tok + 1])
    right_ctx = " ".join(tokens[last_tok + 1:right_end])

    return left_ctx, keyword, right_ctx


# ---------------------------------------------------------------------------
# 4.  MAIN PROCESSING
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze IGC-Parla JSONL across 15 discursive domains."
    )
    parser.add_argument(
        "jsonl_file",
        help="Path to the IGC-Parla JSONL file",
    )
    parser.add_argument(
        "--output-dir",
        default="./parla_results",
        help="Directory for output CSV/TSV files (default: ./parla_results)",
    )
    return parser.parse_args()


def extract_year(record):
    """Extract 4-digit year string from metadata."""
    meta = record.get("metadata", {})
    ts = meta.get("publish_timestamp", "")
    if ts and len(ts) >= 4:
        candidate = ts[:4]
        if candidate.isdigit():
            return candidate
    # Fallback: try xml_id
    xml_id = meta.get("xml_id", "")
    m = re.search(r"IGC-Parla_(\d{4})", xml_id)
    if m:
        return m.group(1)
    return "unknown"


def extract_text(record):
    """Return the document text, supporting both 'document' and 'text' keys."""
    return record.get("document") or record.get("text") or ""


def main():
    args = parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Compile all patterns
    domain_patterns = compile_domain_patterns(DOMAINS)
    domain_ids = [d["id"] for d in DOMAINS]
    domain_names = {d["id"]: d["name"] for d in DOMAINS}

    # Build a flat list of (domain_id, stem, pattern) for concordance collection
    all_stem_entries = []
    for d in DOMAINS:
        for stem, pat in domain_patterns[d["id"]]:
            all_stem_entries.append((d["id"], stem, pat))

    # -----------------------------------------------------------------------
    # Data accumulators
    # -----------------------------------------------------------------------
    # stem_year_counts[stem][year] = total occurrence count
    stem_year_counts = defaultdict(lambda: defaultdict(int))

    # domain_year_docs[domain_id][year] = number of docs with >= 1 match
    domain_year_docs = defaultdict(lambda: defaultdict(int))

    # cooccurrence[domain_i][domain_j] = number of docs where both match
    cooccurrence = defaultdict(lambda: defaultdict(int))

    # yearly_totals[year] = {"docs": int, "tokens": int}
    yearly_totals = defaultdict(lambda: {"docs": 0, "tokens": 0})

    # concordances[stem] = list of concordance dicts (capped at 50)
    concordances = defaultdict(list)

    # -----------------------------------------------------------------------
    # Process JSONL
    # -----------------------------------------------------------------------
    print(f"Opening: {args.jsonl_file}", flush=True)
    doc_count = 0
    error_count = 0

    with open(args.jsonl_file, encoding="utf-8", errors="replace") as fh:
        for line_num, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue

            # Parse JSON
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                error_count += 1
                continue

            text = extract_text(record)
            if not text:
                continue

            year = extract_year(record)
            meta = record.get("metadata", {})
            xml_id = meta.get("xml_id", "")
            speaker = meta.get("speaker", "")

            doc_count += 1
            tokens = text.split()
            token_count = len(tokens)
            text_lower = text.lower()

            # Update yearly totals
            yearly_totals[year]["docs"] += 1
            yearly_totals[year]["tokens"] += token_count

            # Which domains matched this document?
            matched_domains = set()

            for d in DOMAINS:
                did = d["id"]
                domain_matched = False

                for stem, pat in domain_patterns[did]:
                    positions = find_match_positions(text, text_lower, stem, pat)
                    if not positions:
                        continue

                    occ_count = len(positions)
                    stem_year_counts[stem][year] += occ_count
                    domain_matched = True

                    # Concordances (up to 50 per stem)
                    if len(concordances[stem]) < 50:
                        for ms, me in positions:
                            if len(concordances[stem]) >= 50:
                                break
                            kwic = extract_kwic(text, ms, me)
                            if kwic:
                                left_ctx, keyword, right_ctx = kwic
                                concordances[stem].append(
                                    {
                                        "xml_id": xml_id,
                                        "year": year,
                                        "speaker": speaker,
                                        "domain": domain_names[did],
                                        "stem": stem,
                                        "left_context": left_ctx,
                                        "keyword": keyword,
                                        "right_context": right_ctx,
                                    }
                                )

                if domain_matched:
                    domain_year_docs[did][year] += 1
                    matched_domains.add(did)

            # Co-occurrence matrix
            matched_list = sorted(matched_domains)
            for i, da in enumerate(matched_list):
                for db in matched_list[i:]:
                    cooccurrence[da][db] += 1
                    if da != db:
                        cooccurrence[db][da] += 1

            # Progress report
            if doc_count % 10_000 == 0:
                print(
                    f"  Processed {doc_count:,} documents "
                    f"(line {line_num:,}, errors: {error_count}) ...",
                    flush=True,
                )

    print(
        f"\nFinished reading. Total documents: {doc_count:,}  "
        f"Skipped (JSON errors): {error_count:,}",
        flush=True,
    )

    # -----------------------------------------------------------------------
    # 5.  WRITE OUTPUTS
    # -----------------------------------------------------------------------

    all_years = sorted(yearly_totals.keys())
    # Collect all stems encountered
    all_stems = sorted(stem_year_counts.keys())

    # -------------------------------------------------------------------
    # 5a. parla_domain_stems_by_year.csv
    # -------------------------------------------------------------------
    stems_by_year_path = os.path.join(args.output_dir, "parla_domain_stems_by_year.csv")
    with open(stems_by_year_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        header = ["stem"] + all_years
        writer.writerow(header)
        # Iterate all defined stems in domain order to preserve grouping
        written_stems = set()
        for d in DOMAINS:
            for stem, _ in domain_patterns[d["id"]]:
                if stem in written_stems:
                    continue
                written_stems.add(stem)
                row = [stem] + [stem_year_counts[stem].get(yr, 0) for yr in all_years]
                writer.writerow(row)
        # Write any remaining stems not explicitly defined (shouldn't happen)
        for stem in all_stems:
            if stem not in written_stems:
                row = [stem] + [stem_year_counts[stem].get(yr, 0) for yr in all_years]
                writer.writerow(row)

    print(f"Wrote: {stems_by_year_path}", flush=True)

    # -------------------------------------------------------------------
    # 5b. parla_domains_by_year.csv
    # -------------------------------------------------------------------
    domains_by_year_path = os.path.join(args.output_dir, "parla_domains_by_year.csv")
    with open(domains_by_year_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        header = ["domain_id", "domain_name"] + all_years
        writer.writerow(header)
        for d in DOMAINS:
            did = d["id"]
            row = (
                [did, d["name"]]
                + [domain_year_docs[did].get(yr, 0) for yr in all_years]
            )
            writer.writerow(row)

    print(f"Wrote: {domains_by_year_path}", flush=True)

    # -------------------------------------------------------------------
    # 5c. parla_domain_cooccurrence.csv
    # -------------------------------------------------------------------
    cooc_path = os.path.join(args.output_dir, "parla_domain_cooccurrence.csv")
    with open(cooc_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        header = ["domain"] + domain_ids
        writer.writerow(header)
        for da in domain_ids:
            row = [da] + [cooccurrence[da].get(db, 0) for db in domain_ids]
            writer.writerow(row)

    print(f"Wrote: {cooc_path}", flush=True)

    # -------------------------------------------------------------------
    # 5d. parla_concordances.tsv
    # -------------------------------------------------------------------
    conc_path = os.path.join(args.output_dir, "parla_concordances.tsv")
    with open(conc_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(
            [
                "xml_id",
                "year",
                "speaker",
                "domain",
                "stem",
                "left_context",
                "keyword",
                "right_context",
            ]
        )
        for d in DOMAINS:
            for stem, _ in domain_patterns[d["id"]]:
                for conc in concordances[stem]:
                    writer.writerow(
                        [
                            conc["xml_id"],
                            conc["year"],
                            conc["speaker"],
                            conc["domain"],
                            conc["stem"],
                            conc["left_context"],
                            conc["keyword"],
                            conc["right_context"],
                        ]
                    )

    total_concordances = sum(len(v) for v in concordances.values())
    print(
        f"Wrote: {conc_path}  ({total_concordances:,} concordance lines)",
        flush=True,
    )

    # -------------------------------------------------------------------
    # 5e. parla_yearly_summary.csv
    # -------------------------------------------------------------------
    summary_path = os.path.join(args.output_dir, "parla_yearly_summary.csv")
    with open(summary_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        # Build header
        domain_doc_cols = [f"{d['id']}_docs" for d in DOMAINS]
        domain_rate_cols = [f"{d['id']}_per1000" for d in DOMAINS]
        header = ["year", "total_docs", "total_tokens"] + domain_doc_cols + domain_rate_cols
        writer.writerow(header)
        for yr in all_years:
            total_docs = yearly_totals[yr]["docs"]
            total_tokens = yearly_totals[yr]["tokens"]
            doc_counts = [domain_year_docs[d["id"]].get(yr, 0) for d in DOMAINS]
            rates = []
            for cnt in doc_counts:
                if total_docs > 0:
                    rates.append(round(1000.0 * cnt / total_docs, 4))
                else:
                    rates.append(0.0)
            writer.writerow([yr, total_docs, total_tokens] + doc_counts + rates)

    print(f"Wrote: {summary_path}", flush=True)

    # -----------------------------------------------------------------------
    # 6.  SUMMARY TO STDOUT
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Input file       : {args.jsonl_file}")
    print(f"  Output directory : {args.output_dir}")
    print(f"  Total documents  : {doc_count:,}")
    print(f"  Years covered    : {all_years[0] if all_years else 'n/a'} – "
          f"{all_years[-1] if all_years else 'n/a'}")
    print(f"  JSON errors      : {error_count:,}")
    print()
    print(f"  {'Domain':<42} {'Total docs matched':>18}")
    print(f"  {'-'*42} {'-'*18}")
    for d in DOMAINS:
        did = d["id"]
        total_matched = sum(domain_year_docs[did].values())
        print(f"  {d['name']:<42} {total_matched:>18,}")
    print()
    print(f"  Concordance lines collected : {total_concordances:,}")
    print()
    print("Output files:")
    print(f"  {stems_by_year_path}")
    print(f"  {domains_by_year_path}")
    print(f"  {cooc_path}")
    print(f"  {conc_path}")
    print(f"  {summary_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
