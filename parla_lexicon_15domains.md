# IGC-Parla Genealogy Lexicon — 15 Discursive Domains

**Provenance file for `parla_full_genealogy.py`**
*Corpus: Icelandic Gigaword Corpus – Parliamentary Debates (IGC-Parla), 1909–present*
*Created: 2026-04-01*

---

## Purpose

This document records the design rationale, Icelandic lexical stems, English glosses, and analytical justification for the 15 discursive domains used in `parla_full_genealogy.py`. Each domain corresponds to a genealogical node in the Icelandic parliamentary discourse on population, movement, governance, and national identity. The lexicons are deliberately broad: stems rather than full words are matched so that inflected and derived forms (nominative, genitive, plural, verbal noun, etc.) are captured.

---

## Matching conventions

| Type | Method | Example |
|---|---|---|
| Single-word stem | `\b` + stem, `re.IGNORECASE` | `útlending` → *útlendingi, útlendinga, útlendingamál, …* |
| Multi-word phrase | Case-folded substring search | `friðhelgi heimil` → *friðhelgi heimilisins, …* |

---

## Domain 1 — Immigration / movement (D01_immigration)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `innflytjend` | immigrant(s) |
| `innflytjand` | immigrant(s) (alternate inflection) |
| `aðflutning` | in-migration, influx |
| `búseta erlend` | residence abroad / foreign residency |

### Rationale
This domain tracks the basic lexicon of voluntary population movement into Iceland. The two stem variants (`innflytjend-` / `innflytjand-`) capture the morphological alternation in Icelandic weak-noun declension. `aðflutningur` is the administrative term for documented in-migration used in parliamentary bills from the 1930s onward. Together these terms mark the primary frame through which the Althing legislated on newcomers distinct from refugees or wartime aliens.

---

## Domain 2 — Foreigners / alterity (D02_foreigners)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `útlending` | foreigner, alien |
| `utlending` | foreigner (non-accented orthographic variant) |
| `erlend ríkisborgari` | foreign national / citizen of a foreign state |
| `erlent vinnuafl` | foreign labour force |

### Rationale
`útlendingur` is the unmarked term for "foreigner" throughout the legislative record. The unaccented variant `utlending` appears in older transcripts and in some digitisation artefacts. `erlend ríkisborgari` is a legalese phrase marking formal citizenship discourse; `erlent vinnuafl` frames foreigners primarily as economic inputs. Together these stems map the alterity axis of parliamentary debate: the figure of "the foreigner" as legal subject, economic agent, and social other.

---

## Domain 3 — Asylum / refuge (D03_asylum)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `hælisleit` | asylum-seeking |
| `haelisleit` | asylum-seeking (unaccented variant) |
| `flóttafólk` | refugees (lit. "flight-people") |
| `flóttamenn` | refugees (masculine plural) |
| `flóttamaður` | refugee (masculine singular) |
| `flóttama` | refugee (stem covering all declensions) |
| `alþjóðleg vernd` | international protection |
| `umsókn um vernd` | application for protection |

### Rationale
Modern Icelandic refugee discourse is anchored in the `flótta-` compound family and the international-law phrase `alþjóðleg vernd`. The asylum-specific neologism `hælisleitandi` (asylum-seeker) emerged in the 1990s; its stem captures all inflected forms. This domain is central to post-1951 debates and to the 21st-century increase in arrivals.

---

## Domain 4 — Border / legal governance (D04_border)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `landamær` | border(s) |
| `vegabréfsáritun` | visa (lit. "passport endorsement") |
| `dvalarleyf` | residence permit |
| `útlendingastofnun` | Directorate of Immigration |
| `brottvísun` | expulsion, deportation |
| `brottvisun` | expulsion (unaccented variant) |
| `framsending` | extradition / forwarding (deportation synonym) |

### Rationale
This domain captures the administrative and coercive apparatus of border control as it appears in legislation and interpellations. `dvalarleyfi` and `vegabréfsáritun` mark the permit-regime; `brottvísun` and `framsending` mark the expulsion-regime. `Útlendingastofnun` (est. 2002) is the institutional anchor for post-devolution debates.

---

## Domain 5 — Security / policing (D05_security)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `almannaöryggi` | public safety / public order |
| `lögreglu` | police (genitive, most inflected forms) |
| `logreglu` | police (unaccented variant) |
| `ríkislögreglu` | national police |
| `glæp` | crime(s) |
| `handtek` | arrest, apprehension |
| `ógn` | threat, menace |
| `hryðjuverk` | terrorism |
| `ofbeldi` | violence |
| `fangels` | prison, imprisonment |

### Rationale
The security domain indexes moments when parliamentary debate frames migration, foreigners, or marginal populations through the lens of public order and criminal threat. `almannaöryggi` is the formal phrase in legislative preambles; `hryðjuverk` is post-9/11 discourse; `lögreglu` covers the everyday policing apparatus. This domain cross-tabs powerfully with D02 (foreigners) and D08 (morality) in moments of moral panic.

---

## Domain 6 — Integration / welfare (D06_integration)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `aðlögun` | adaptation, adjustment |
| `samþætting` | integration (lit. "unification") |
| `tungumálanám` | language learning |
| `íslenskunám` | Icelandic language instruction |
| `félagsþjónust` | social services |
| `félagslega þjónust` | social services (adjectival phrase form) |
| `vinnumarkaður` | labour market |
| `vinnumarkað` | labour market (accusative/dative) |

### Rationale
Post-1990 debates on immigrant integration cluster around language acquisition, labour-market participation, and social-service access. `samþætting` is the modern policy term (replacing earlier `aðlögun`). The labour-market stems capture the dominant economic framing of integration success/failure in Althing committees.

---

## Domain 7 — Housing / quartering (D07_housing)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `húsnæði` | housing, accommodation |
| `húsaleig` | house-rent, tenancy |
| `húsaleigufrumvarp` | rental housing bill |
| `herbergi` | room(s) |
| `íbúð` | apartment, dwelling |
| `innvistun` | quartering, billeting (wartime) |
| `húsaskipan` | housing allocation / arrangement |
| `geymsluhús` | storage building (used as lodgings) |
| `niðursetning` | placing out (of persons into households) |
| `niðursetningar` | placing-out (genitive/plural) |
| `friðhelgi heimil` | sanctity of the home |
| `heimilisfriðu` | domestic peace, inviolability of home |
| `útburðarheimild` | eviction authority |
| `utanhéraðsm` | from outside the district (persons placed out) |
| `innanhéraðsm` | within the district (placement) |

### Rationale
This domain is analytically pivotal for the wartime debates of 1940–1945. The `niðursetning` system — placing poor individuals into private households by parish obligation — intersects with British and American occupation troops' demand for billets (`innvistun`), producing a distinctive 1943 parliamentary controversy. The inviolability-of-home stems (`friðhelgi heimilis`, `heimilisfriðu`) mark constitutional resistance to billeting. This domain also spans the longer poor-law and social-housing arc from 1900 to present.

---

## Domain 8 — Morality / Ástandið (D08_morality)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `ástand` | situation, condition (also "Ástandið" = wartime moral crisis) |
| `siðferðis` | moral, ethical (genitive modifier) |
| `siðferðislögreglu` | morality police / morals enforcement |
| `lauslát` | loose morals, licentiousness |
| `varnarlaus` | defenceless, unprotected (women) |
| `kynferðis` | sexual (modifier) |
| `kynlíf` | sex life, sexuality |
| `vændi` | prostitution |
| `kleppjárnsreyk` | Kleppjárnsreykir (wartime "morality" camp site) |
| `sauðárkrók` | Sauðárkrókur (regional moral-panic flashpoint) |

### Rationale
*Ástandið* ("the Situation") is the Icelandic historiographical term for the wartime moral panic over Icelandic women's relationships with Allied troops. Parliamentary debates 1940–1946 are dense with this vocabulary. `siðferðislögreglu` refers to the women's auxiliary morality police established during the occupation. Place-names `Kleppjárnsreyk` and `Sauðárkrók` index specific regional debates. This domain cross-tabs with D13 (gender) and D05 (security).

---

## Domain 9 — Poverty / poor law (D09_poverty)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `fátæk` | poor, poverty |
| `fátækra` | of the poor (genitive) |
| `fátækling` | pauper, poor person |
| `framfærslu` | maintenance, poor relief |
| `framfærslulög` | poor-relief law |
| `framfærslusveit` | relief parish/commune |
| `heimilislaus` | homeless |
| `heimilisleysi` | homelessness |
| `urfam` | destitute, penniless |
| `ftkra` | abbreviation/OCR variant of fátækra |
| `fátækrasjóð` | poor fund |
| `ómagar` | dependents, those unable to support themselves |
| `ómögul` | impossible cases (welfare-speak for the destitute) |

### Rationale
The Icelandic poor law (`framfærslulög`) was the primary mechanism governing domestic poverty and internal mobility from 1882 to 1947. Debates over `framfærslusveit` (the parish responsible for a pauper) and `niðursetning` (D07) are the backbone of pre-welfare-state poverty governance in the Althing. This domain establishes the legal genealogy that the welfare state (D15) eventually replaced.

---

## Domain 10 — Labour discipline / emergency economy (D10_labour)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `gengislög` | exchange-rate legislation |
| `kaupgjald` | wages, wage-payment |
| `dýrtíð` | high cost of living, wartime inflation |
| `dýrtíðaruppbætur` | cost-of-living supplements |
| `verkfall` | strike |
| `verkfalls` | of the strike (genitive) |
| `gerðardóm` | arbitration court |
| `kaupmálasamning` | collective wage agreement |
| `verðtrygg` | indexation, inflation-linking |
| `launakröf` | wage demands |
| `vinnufriðu` | industrial peace |
| `verkamenn` | workers, labourers |
| `verkalýð` | working class, labour (collective) |
| `neyðarráðstaf` | emergency measures |

### Rationale
The wartime and postwar Icelandic economy was marked by intense wage-price conflict. This domain captures the parliamentary vocabulary of labour-management conflict, emergency economic legislation, and class-based mobilisation. It contextualises why the Althing repeatedly legislated on labour during the same sessions as those on aliens and morality: the occupied economy disrupted both wage structures and social order.

---

## Domain 11 — Racial terms / racialized language (D11_racial)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `negri` | N-word equivalent (Icelandic) |
| `negra` | N-word (genitive/accusative) |
| `neger` | "Negro" (older Icelandic borrowing from Danish/German) |
| `svertingi` | Black person (derogatory) |
| `svertingja` | Black person (genitive) |
| `blámaður` | "blue man" (archaic for Black African person) |
| `blámann` | "blue man" (accusative) |
| `blökkumaður` | Black person (modern, less derogatory) |
| `blökkumann` | Black person (accusative) |
| `litaður` | "coloured" (person of colour) |
| `litað` | "coloured" (neuter form) |
| `kynþátt` | race (biological/ethnic classification) |
| `þjóðern` | nationality, ethnicity, nationhood |
| `kínverj` | Chinese person/people |
| `gyðing` | Jewish person |
| `múslim` | Muslim |
| `sígaun` | Gypsy/Roma (derogatory) |

### Rationale
This domain documents racialized language in Icelandic parliamentary discourse. Historically sparse but analytically significant: the Allied occupation brought Black American soldiers to Iceland for the first time, prompting racial commentary in the Althing. Post-1990 economic migration and post-2000 Muslim immigration generate a second wave. Tracking this domain across time reveals the entry, normalisation, and (partial) delegitimation of racial vocabulary in formal political speech.

---

## Domain 12 — Military / occupation (D12_military)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `setulið` | occupation forces (lit. "stationed troops") |
| `setuliðs` | of the occupation forces (genitive) |
| `hernám` | occupation (military) |
| `hernaðar` | of war / military (genitive modifier) |
| `hersveit` | military unit, troops |
| `varnarsvæð` | defence zone/area |
| `varnarliðs` | of the defence forces (genitive) |
| `varnarliði` | defence forces (dative) |
| `keflavík` | Keflavík (NATO base location) |
| `miðnesheiði` | Miðnesheiði (Keflavík base heath) |
| `bandaríkjaher` | US Army / American military |
| `brezkur her` | British Army (older orthography) |
| `breska her` | British Army (accusative/adjective form) |

### Rationale
Iceland was occupied by Britain (1940) and then the US (1941) without formal declaration of war. Debates about the status of foreign troops, the defence agreement, and the Keflavík base span the entire 1940–2006 period. Place-names index specific geographic flashpoints. This domain grounds the corpus in its most distinctive historical context and provides the frame within which D02 (foreigners), D07 (housing), and D08 (morality) must be read.

---

## Domain 13 — Women / gender / sexuality (D13_gender)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `kvenréttind` | women's rights |
| `kvennaréttind` | women's rights (genitive compound) |
| `konur og` | women and … (common parliamentary phrase opener) |
| `kvenna` | of women (genitive) |
| `stúlk` | girl(s) |
| `mæðra` | of mothers (genitive) |
| `barnsmóðir` | mother of a child (legal term) |
| `einstæð` | single (parent), unmarried |
| `launabarn` | illegitimate child (lit. "secret child") |
| `barnshafandi` | pregnant |
| `ólögleg` | illegal, unlawful (often modifying births, relationships) |

### Rationale
Gender is a transversal domain intersecting D08 (morality), D09 (poverty: lone mothers and illegitimate children), and D15 (welfare: maternity provisions). The wartime period is central: debates about *Ástandið* were explicitly about the sexual conduct of Icelandic women. The suffrage arc (pre-1915 to 1920), the equal-pay debates (1960s–1970s), and post-2000 gender-equality legislation provide additional layers.

---

## Domain 14 — National identity / belonging (D14_identity)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `íslensk menning` | Icelandic culture |
| `íslenskri menning` | Icelandic culture (dative) |
| `þjóðleg` | national (adjective) |
| `þjóðlíkam` | the national body / body politic |
| `hreinleik` | purity (racial or cultural) |
| `kynstofn` | racial stock, lineage |
| `norræn` | Nordic |
| `norðurgerman` | North Germanic (ethnic classification) |
| `hvítra manna` | of white men (genitive phrase) |
| `hvít` | white (racial adjective) |

### Rationale
This domain captures the explicit articulation of national and racial belonging in parliamentary discourse. `þjóðlíkami` (the national body) is a key biologistic metaphor. `hreinleiki` and `kynstofn` are the clearest markers of interwar racial-hygiene language in Icelandic politics. `norrænn` positions Iceland within pan-Nordic and, in certain contexts, pan-Aryan discourses. These stems provide the ideological frame within which anxiety about foreigners, soldiers, and racial mixing was expressed.

---

## Domain 15 — Welfare state / social services (D15_welfare)

### Stems
| Icelandic stem | English gloss |
|---|---|
| `tryggingastofnun` | Social Insurance Administration |
| `almannatrygging` | social insurance / national insurance |
| `lífeyri` | pension |
| `sjúkratrygging` | health insurance |
| `barnabætur` | child benefit |
| `meðlag` | child maintenance / alimony |
| `barnavernd` | child protection |
| `félagsráðgjaf` | social worker |

### Rationale
The Icelandic welfare state was legislated primarily 1936–1956, replacing the poor-law system (D09). This domain marks the transition from punitive to entitlement-based poverty governance. `Almannatryggingar` (Social Insurance Act 1936, reformed 1946) is the legislative pivot. Tracking D15 against D09 across years reveals the chronology of welfare-state consolidation. The co-occurrence of D15 with D02 (foreigners) indexes debates about whether welfare entitlements extend to non-citizens.

---

## Cross-domain analytical clusters

| Cluster | Domains | Period of maximum salience |
|---|---|---|
| Wartime occupation complex | D02, D07, D08, D12, D13 | 1940–1946 |
| Poor-law / welfare transition | D09, D07, D15 | 1900–1960 |
| Racialised security | D02, D05, D11, D14 | 1940–1946, 2000–present |
| Post-1990 immigration regime | D01, D02, D03, D04, D06 | 1990–present |
| Labour and emergency economy | D05, D10, D14 | 1930–1950 |

---

## Source notes

The IGC-Parla corpus digitises Icelandic Althing proceedings from the founding session of 1909 onward. XML IDs follow the pattern `IGC-Parla_YYYY-MM-DD-chamber-N` where chamber is `lower` (Neðri deild), `upper` (Efri deild), or `combined` (after unicameral reform 1991). Lexical stems were developed through close reading of the 1943 parliamentary debates (Þingskjöl 1943) and extended to cover the full chronological range through iterative corpus exploration.
