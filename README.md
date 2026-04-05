DOI: 10.5281/zenodo.19429553 
# THE ICELANDIC GIGAWORD CORPUS 2 IN JSONL FORMAT
### http://hdl.handle.net/20.500.12537/364

This package contains those subcorpora of the Icelandic Gigaword Corpus, version 
22.10 and 24.10ext, that have been published with an restricted licence, in a 
JSONL format, which is suitable for LLM training.

-----------------------------------------------------------------------------
## ABOUT THE ICELANDIC GIGAWORD CORPUS (IGC):

For detailed information about The Icelandic Gigaword Corpus , please refer to 
https://igc.arnastofnun.is.

### Version IGC-2022
Version 22.10 contains text until the end of the year 2021 and can be downloaded here
in TEI-format: http://hdl.handle.net/20.500.12537/253.

### Version IGC-2024ext
Version 24.10ext contains mainly texts from the years 2022 and 2023. For IGC-Parla and 
two of the three subcorpora of IGC-Law (IGC-Law-Proposals and IGC-Law-Bills) texts from
2021 were also included since some new texts had been retrieved since the publication
of IGC-2022. For the third subcorpora, IGC-Law-Law, the whole Icelandic law corpus was
compiled since there are always some modifications to older provisions.

Version 24.10ext can be downloaded here in TEI-format: http://hdl.handle.net/20.500.12537/253


### Subcorpora and size
The Icelandic Gigaword Corpus contains 9 corpora. Some corpora contain two or more
subcorpora. 

IGC-2022 contains almost 2.4 billion words, while IGC-2024ext contains around 82.7 million
running words. The two tables below show the number of running words (millions) for
each corpus and version:

**Open licence:**

| Corpus | IGC-2022| IGC-2024ext |
| :---:   | :---: | :---: |
| IGC-Adjud|69.3 | 10.3 |
| IGC-Journals|20.9 |
| IGC-Law|53.3 | 7.3 |
| IGC-News1 | 396.7 | 53.1 |
| IGC-Parla | 254.1 | 12.0 |
| IGC-Social | 724.0 | |
| IGC-Wiki | 8.5 | |
|TOTAL | 1526.8 | 82.7 |

**Restricted licence:**
| Corpus |  IGC-2022| IGC-2024ext |
| :---:   | :---: | :---: |
| IGC-Books | 13.8 | |
| IGC-News2 | 899.8 | 79.3 |
|TOTAL | 913.6 | 79.3 |

Since we do not have the permission to distribute the data from Twitter (part of 
IGC-Social) users who download IGC have to fetch the original data themselves and 
then use special scripts to insert the text into the TEI files. Due to these 
complications, we do not include Twitter in this package.


## LICENSE:

The corpora contained in this package are published with a CC-BY license
(https://creativecommons.org/licenses/by/4.0/).


## THE HUGGINGFACE DATASET:

### The size of the dataset
The dataset  only includes texts from the 7 corpora with an open licence (see above), 
and excluding Twitter, as already mentioned. It contains around 1,457 million running words. 
Since there is some overlap for the year 2021 (as mentioned above), all duplications were removed
from IGC-Parla and IGC-Law and the subcorpus IGC-Law-Law from IGC-2024ext replaces the 
one from IGC-2022.

### The format of the dataset
Each subcorpus has been converted to one JSONL file with the "Icelandic Gigaword 
Corpus JSONL Converter" (http://hdl.handle.net/20.500.12537/332). Each jsonl-file 
belongs to one subset (configuration) in the dataset, so it's possible to load 
each subcorpus individually. 

Each line in the JSONL file contains one news article, a parliamentary session, etc.
The information and the format of a single line are the following:

{
    "document": "all text of the file, with paragraph splits shown as '\n\n'", 
    "uuid": "a randomly generated ID for the json object", 
    "metadata": 
    {
        "author": "the original file's author, if available", 
        "fetch_timestamp": "the date of the conversion", 
        "xml_id": "the ID of the original XML file", 
        "publish_timestamp": "the publishing date of the text in the original XML file", 
        "title": {"offset": None, "length": None},                                                  
             # the offset and length of the text's title
        "paragraphs": [{"offset": None, "length": None}, {"offset": None, "length": None}, ...],    
             # the offset and length of each paragraph
        "sentences": [{"offset": None, "length": None}, {"offset": None, "length": None}, ...],     
             # the offset and length of each sentence 
        "source": "the source of the original text, taken from the XML file"
    }
}

Further information about each subcorpus is found in the file info.json where each 
of the seven corpora (IGC-News1, IGC-Parla, IGC-Social ..) are a key in a dictionary 
holding information about the name and id of each subcorpora as well as its quality, 
domain, language and version)

{
    "subdirectory of the subcorpus, e.g. IGC-Adjud-Appeal": 
    {
        "path": "path to the converted corpus", 
        "quality": "quality categorization, taken from `Flokkun.tsv`, which was 
                    created by the Árni Magnússon Institute for Icelandic Studies", 
        "domain": ["a list of all relevant domains, taken from `Flokkun.tsv`"], 
        "lang": "the language of the corpus, which is 'is' for all current cases", 
        "version": "the IGC version, which is 22.10 by default"
    }
}

Further information about the domains and how the quality of the texts was assessed is 
found here below.

--------------------------------------------------------------------------------
### USAGE:

The file example.py shows how information and data can be retrieved. After writing 
the correct path to the downlaoded folder you can run it with
  python3 example.py
  
--------------------------------------------------------------------------------

### CATEGORIES - DOMAIN:

We classified the 86 subcorpora into 13 domains or genres:

Adjudications 
   Judgements from the three levels of jurisdiction in Iceland
   Subcorpus: IGC-Adjud
Blog 
   Three online blogs
   Subcorpus: IGC-Social2
News 
   Texts from general news media (online and printed) 
News - local 
   Texts from local news media (online and printed)
   Selected subcorpora from IGC-News1 and IGC-News2
News - radio
   Transcripts of news on the radio
   Selected subcorpora from IGC-News1
News - specialized 
   Texts from media (online and printed) dedicated to specific issues (business, 
     agriculture …)
   Selected subcorpora from IGC-News1 and IGC-News2
News - sport
   Texts from four websites that deliver sports news
   Selected subcorpora from IGC-News1 and IGC-News2
News - TV 
   Transcripts of news on TV
   Selected subcorpora from IGC-News1
Online forum 
   Three online forums
   Subcorpus: IGC-Social1
Parliamentary data 
   Subcorpora: IGC-Parla, IGC-Law 
   The Icelandic Law corpus, explanatory reports and observations extracted from 
     bills submitted to Althingi, and parliamentary proposals and resolutions.
Published books
   Subcorpus: IGC-Books
Scientific journals 
   Mainly printed journals but also a few online journals
   Subcorpus: IGC-Journals
Wikipedia
   Subcorpus: IGC-Wiki


### CATEGORIES - QUALITY

We selected random sentences from each subcorpora (max 50.000 tokens for the bigger 
corpora), that were then corrected using the Byte-Level Neural Error Correction Model 
for Icelandic (http://hdl.handle.net/20.500.12537/255). Each sentence was also analysed 
with Greynir (http://hdl.handle.net/20.500.12537/269) and sentences that the tool 
classified as a foreign sentence were marked specially. Finally, the ratio of sentences 
containing errors or marked as foreign to the total amount of sentences was calculated. 
We divided the texts into three groups, A - C, where A has the fewest errors/foreign 
sentences and C the most.

As expected, texts from public data, scientific journals and news from the bigger news 
media (generally proofread by professionals) mostly ranked high, and texts from the 
online forums ranked lowest, but some texts that we had expected to rank high did not. 
This is due to the fact that many of the errors have nothing to do with the quality of 
the original text but how it was processed. Texts from Morgunblaðið, which you would expect 
to rank high, often had the headlines glued to the main text, which caused errors. The 
texts from many of the scientific journals were read with OCR which can also lead to errors. 
Finally, the parliamentary speeches, usually of good quality since they have been proofread, 
go back to the beginning of the 20th century when spelling rules were different from now.
