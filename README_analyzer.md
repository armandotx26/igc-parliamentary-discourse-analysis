# IGC Parliamentary Discourse Analyzer

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19429553.svg)](https://doi.org/10.5281/zenodo.19429553)

**A corpus-assisted discourse analysis toolkit for the Icelandic Gigaword Corpus (IGC), covering parliamentary debates from 1909 to 2023.**

This repository contains the Python scripts, lexicons, and replication materials for the study:

> [Author Name]. (2026). The Discursive Production of the Migration-Security Nexus in Iceland: A Corpus-Assisted Analysis of the Icelandic Gigaword Corpus, 1909–2023. *[Journal]*.

---

## Overview

This toolkit analyzes 19,502 parliamentary speeches from the Icelandic Alþingi (1909–2023), extracted from the Icelandic Gigaword Corpus (IGC; Steingrímsdóttir et al., 2022). It provides:

- **15-domain discursive classification** of parliamentary debates across immigration, security, housing, morality, poverty, labour, racial terms, military, gender, and more
- **World country and region mention analysis** using a 307-entry Icelandic-language gazetteer covering all UN member states, territories, and supranational organizations
- **Temporal trend analysis** across 114 years of parliamentary records
- **Co-occurrence matrices** showing how discursive domains and country mentions intersect

## Requirements

- Python 3.10+
- Standard library only for core analysis (`json`, `re`, `csv`, `collections`, `argparse`)
- `pandas` and `matplotlib` for visualization
- `geopandas` for world map generation (optional)

```bash
pip install pandas matplotlib geopandas
```

## Data Access

The IGC is available from the Árni Magnússon Institute for Icelandic Studies:
- **Website**: https://igc.arnastofnun.is
- **Version used**: IGC-2022 + IGC-2024ext (JSONL format)
- **Citation**: Steingrímsdóttir, S., Ingason, A.K., & Loftsson, H. (2022). Risamálheild: A Very Large Icelandic Text Corpus. *Proceedings of LREC 2022*, 2400–2407. https://aclanthology.org/2022.lrec-1.254/

The IGC-Parla subcorpus contains parliamentary debates from 1909 to 2023 in JSONL format, where each line is a JSON object:

```json
{"document": "speech text...", "metadata": {"xml_id": "IGC-Parla_1943-02-15-lower-23", "publish_timestamp": "1943-02-15"}}
```

## Scripts

### `parla_full_genealogy.py` — 15-Domain Parliamentary Analyzer

Classifies each parliamentary speech across 15 discursive domains using Icelandic-language stem matching with Unicode-aware word boundaries.

```bash
python parla_full_genealogy.py /path/to/igc_parla.jsonl --output-dir parla_results
```

**Output** (5 files):

| File | Description |
|------|-------------|
| `parla_domain_stems_by_year.csv` | Raw count per stem per year across all 15 domains |
| `parla_domains_by_year.csv` | Document-level counts per domain per year |
| `parla_domain_cooccurrence.csv` | 15×15 symmetric co-occurrence matrix |
| `parla_concordances.tsv` | KWIC concordance lines (±20 tokens, 50 per stem cap) |
| `parla_yearly_summary.csv` | Total docs, tokens, domain counts, normalised rates |

**Expected output**: 19,502 documents, 0 JSON errors, years 1909–2023.

### `igc_country_analyzer.py` — World Country & Region Mention Analyzer

Counts mentions of every country, territory, and world region across the corpus using a comprehensive Icelandic-language gazetteer.

```bash
# Single file
python igc_country_analyzer.py /path/to/igc_parla.jsonl --output-dir country_results

# All subcorpora
python igc_country_analyzer.py --dir /path/to/converted-corpora/ --output-dir country_results
```

**Output** (5 files):

| File | Description |
|------|-------------|
| `country_mentions_by_year.csv` | Year × country document count matrix |
| `country_mentions_total.csv` | Ranked list of all entities by total mentions |
| `region_mentions_by_year.csv` | Year × world region matrix |
| `country_cooccurrence_top50.csv` | 50×50 co-occurrence matrix for top countries |
| `country_concordances.tsv` | KWIC concordance lines (20 per country cap) |

## Lexicon Files

### `igc_world_gazetteer.json`

A 307-entry gazetteer mapping countries, territories, and regions to their Icelandic names, spelling variants, and demonym stems. Covers:
- 250 countries and territories (all 193 UN member states + Palestine, Taiwan, Kosovo, Greenland, Faroe Islands, etc.)
- 32 world regions (continents, subregions)
- 25 supranational organizations (EU/ESB, NATO, UN/SÞ, EEA/EES, etc.)

### `parla_lexicon_15domains.md`

Complete documentation of the 15 discursive domains, including every Icelandic search stem, English gloss, regex pattern, and analytical rationale.

## The 15 Discursive Domains

| # | Domain | Stems | Total docs |
|---|--------|-------|-----------|
| D01 | Immigration / movement | innflytjend, aðflutning, búseta erlend | 2,931 |
| D02 | Foreigners / alterity | útlending, erlend ríkisborgari | 3,668 |
| D03 | Asylum / refuge | hælisleit, flóttafólk, alþjóðleg vernd | 839 |
| D04 | Border / legal governance | landamær, dvalarleyf, brottvísun | 1,690 |
| D05 | Security / policing | almannaöryggi, lögreglu, glæp, hryðjuverk | 6,979 |
| D06 | Integration / welfare | aðlögun, samþætting, tungumálanám | 5,220 |
| D07 | Housing / quartering | húsnæði, niðursetning, friðhelgi heimil | 8,276 |
| D08 | Morality / Ástandið | siðferðis, lauslát, varnarlaus, Kleppjárnsreyk | 10,646 |
| D09 | Poverty / poor law | fátæk, framfærslu, heimilislaus | 9,196 |
| D10 | Labour discipline | gengislög, dýrtíð, verkfall, gerðardóm | 8,593 |
| D11 | Racial terms | negri, svertingi, blámaður, kynþátt, múslim | 1,779 |
| D12 | Military / occupation | setulið, hernám, varnarsvæð, Keflavík | 4,162 |
| D13 | Women / gender / sexuality | kvenréttind, kvenna, stúlk, launabarn | 6,781 |
| D14 | National identity / belonging | þjóðleg, þjóðlíkam, hreinleik, kynstofn | 5,236 |
| D15 | Welfare state / social services | tryggingastofnun, almannatrygging, lífeyri | 6,465 |

## Technical Notes

### Word Boundary Handling

Standard `\b` word boundaries in Python regex fail with Icelandic characters (ð, þ, æ, ö, á, é, í, ó, ú, ý). All scripts use a Unicode-safe left-word-boundary lookbehind instead:

```python
pattern = re.compile(r'(?<![^\W_])' + re.escape(stem), re.IGNORECASE | re.UNICODE)
```

Multi-word stems (containing spaces) use case-folded substring matching.

### Input Format Compatibility

Scripts handle both `"document"` and `"text"` as the JSON key for speech content, and extract years from `metadata.publish_timestamp` (first 4 characters).

## Replication

A detailed step-by-step replication protocol, including validation checksums and expected output values, is provided in `replication_protocol.docx`.

To verify your installation produces correct results:
- Total Parla documents: **19,502**
- Years covered: **1909–2023** (114 unique years)
- Largest domain: Morality/Ástandið = **10,646** documents
- Smallest domain: Asylum/refuge = **839** documents
- JSON errors: **0**
- Concordance lines: **6,018**

## Citation

If you use this software in your research, please cite:

```bibtex
@software{igc_discourse_analyzer_2026,
  author       = {[Author Name]},
  title        = {{IGC Parliamentary Discourse Analyzer: 15-Domain 
                   Classification and Country Mention Analysis}},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.19429553},
  url          = {https://doi.org/10.5281/zenodo.19429553}
}
```

Please also cite the IGC corpus:

```bibtex
@inproceedings{steingrimsdottir2022,
  author    = {Steingrímsdóttir, Steinunn and Ingason, Anton Karl and Loftsson, Hrafn},
  title     = {Risamálheild: A Very Large Icelandic Text Corpus},
  booktitle = {Proceedings of the 13th Language Resources and Evaluation Conference (LREC 2022)},
  year      = {2022},
  pages     = {2400--2407},
  publisher = {European Language Resources Association},
  url       = {https://aclanthology.org/2022.lrec-1.254/}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

The author gratefully acknowledges the Árni Magnússon Institute for Icelandic Studies for maintaining and providing access to the Icelandic Gigaword Corpus (IGC).
