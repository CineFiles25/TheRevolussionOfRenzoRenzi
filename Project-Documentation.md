# Project Documentation
## The "Revolussion" of Renzo Renzi
*Information Science and Cultural Heritage – University of Bologna (2024–2025)*
*Instructors: Marilena Daquino and Francesca Tomasi*

---

# Part I — Study of the Domain

## 1. Idea

*The "Revolussion" of Renzo Renzi* is a Digital Humanities and Linked Open Data project centred on **Renzo Renzi** (1919–2004), a central figure in Italian film culture: critic, filmmaker, researcher, and long-time curator of the Cineteca di Bologna.

Renzi's work produced an analogue network of interrelated objects — books, drawings, photographs, interviews, film materials — that anticipates the logic of Linked Open Data. His collection, held at the **Cineteca di Bologna**, is the institutional ground for this project.

The project goal is to **model, encode, and publish** a selection of these materials using cultural heritage standards, TEI/XML, RDF, and a public web interface, turning analogue archival materials into a structured, interoperable digital dataset aligned with LODLAM best practices.

---

## 2. Items

The project selects **15 heterogeneous items** from the Renzo Renzi Collection and related holdings at the Cineteca di Bologna, mixing archival documents, bibliographic records, photographs, drawings, moving images, and sound recordings. One item (*La Strada*, Sequence I) is a full-text document encoded in TEI.

| # | Item | Type | Holding Institution | Institutional Standard | Encoding Format |
|---|------|------|---------------------|------------------------|-----------------|
| 1 | *Il primo Fellini* (Renzo Renzi) | Book | Cineteca di Bologna / Biblioteca Renzo Renzi | ISBD(G) / SBN-MARC | MODS |
| 2 | Sceneggiatura manoscritta di *Guida per camminare all'ombra* | Screenplay / archival record | Cineteca di Bologna / Renzo Renzi Library | ISAD(G) | EAD |
| 3 | Bologna. Cinema Fulgor. Premiere of *La Strada* | Photograph | Cineteca di Bologna / Fondo Iniziative Cineteca | ICCD Scheda F | VRA Core |
| 4 | *La Strada*: Gelsomina col tamburo | Drawing | Cineteca di Bologna / Renzo Renzi Collection | ICCD Scheda OA | VRA Core |
| 5 | Caricature "Perché Federico non fa la rivolussione?" | Drawing / caricature | Cineteca di Bologna / Renzo Renzi Fund | ICCD Scheda OA | VRA Core |
| 6 | Set photograph from *Le notti del Melodramma* | Photograph | Cineteca di Bologna | ICCD Scheda F | VRA Core |
| 7 | Circus performance scene from *La Strada* | Photograph | Cineteca di Bologna / Fondo Fotografie Cineteca | ICCD Scheda F | VRA Core |
| 8 | Gelsomina eating bread in rural landscape | Photograph | Cineteca di Bologna / Fondo Fotografie Cineteca | ICCD Scheda F | VRA Core |
| 9 | *Il cinema a Bologna: Renzo Renzi e la Columbus film* (2000) | Video interview | Cineteca di Bologna | FIAF Cataloguing Rules | MODS |
| 10 | *La strada* (1954), Federico Fellini | Film | Cineteca di Bologna | ISBD(NBM) / FIAF | MODS |
| 11 | *La strada: musique du film* (Nino Rota) | Sound recording | Cineteca di Bologna | ISBD(NBM) / SBN-MARC | MODS |
| 12 | Portrait of Renzo Renzi | Photograph | Cineteca di Bologna / Renzo Renzi Fund | ICCD Scheda F | VRA Core |
| 13 | *Quando il Po è dolce* (1952) | Documentary film | Cineteca di Bologna | ISBD(NBM) / FIAF | MODS |
| 14 | Biblioteca Renzo Renzi | Institution / Library | Cineteca di Bologna | ICCU / ISBD(G) / SBN-MARC | Schema.org (JSON-LD) |
| 15 | Letter to his father (24 July 1942) | Letter / archival record | Cineteca di Bologna / Renzo Renzi Library | ISAD(G) | EAD |

---

# Part II — Knowledge Organization: Elaborate Models

## 3. Metadata Analysis

For each item we identified the descriptive standard adopted by the holding institution and used it as the starting point of our analysis.

### Bibliographic standards:
- **ISBD(G)** — general bibliographic description (book)
- **ISBD(NBM)** — non-book materials (film, soundtrack, documentary)
- **SBN-MARC** — Italian national bibliography (book, sound recording, library)

### Archival standards:
- **ISAD(G)** — general archival description (screenplay manuscript, letter)

### Visual / museum standards:
- **ICCD Scheda F** — photographs
- **ICCD Scheda OA** — drawings and caricatures

### Audiovisual standards:
- **FIAF Cataloguing Rules** — film-related materials (film, documentary, video interview)

### Encoding formats used to produce the metadata files:
- **MODS** — bibliographic items, sound recordings, films, documentary, video interview
- **EAD** — archival records (screenplay, letter)
- **VRA Core** — photographs, drawings, caricatures
- **Schema.org (JSON-LD)** — institution (Biblioteca Renzo Renzi)

---

## 4. Theoretical Model

Each item was described in natural language starting from the original institutional description, enriched with additional relevant information including authority control and subject/classification data.

For each object the analysis identifies:
- **Intrinsic features**: title, date, format, technique, language, extent…
- **Roles and agents**: creators, performers, contributors, editors, directors…
- **Relationships to other entities**: about, depicts, documents, is part of, was produced during…
- **Institutional context**: holding institution, collection, physical location, shelf mark…
- **Authority control**: VIAF, Wikidata, ISIL, ISNI…

This analysis maps the domain narrative connecting the following entity types:
- **People**: Renzo Renzi, Federico Fellini, Giulietta Masina, Nino Rota, Anthony Quinn…
- **Works**: film, documentary, book, soundtrack, screenplay, video interview…
- **Images**: photographs, drawings, caricatures…
- **Events**: film premiere at Cinema Fulgor, documentary production along the Po, military trial…
- **Institutions**: Cineteca di Bologna, Biblioteca Renzo Renzi…
- **Places**: Bologna, Po River Delta, Cinema Fulgor…

The theoretical model is represented as an interactive diagram (Miro board) available on the project website.

---

## 5. Conceptual Model

The conceptual model formally represents the theoretical model by reusing existing schemas, vocabularies, and ontologies — no new ontology was created.

### Ontologies and vocabularies reused:
- **Dublin Core** — general metadata (creator, title, date, subject, publisher…)
- **Schema.org** — creative works, agents, places, events
- **FOAF** — agents and depictions
- **SKOS** — subject classification and authority control
- **CIDOC CRM** — conceptual reference model for cultural heritage


### Core classes:
- `schema:CreativeWork`, `schema:ImageObject`, `schema:VideoObject`, `schema:MusicRecording`
- `schema:Person`, `schema:Organization`, `schema:Place`, `schema:Event`

### Core properties:
- `dcterms:creator`, `dcterms:contributor`, `dcterms:subject`, `dcterms:date`, `dcterms:publisher`
- `schema:about`, `schema:locationCreated`, `schema:hasPart`
- `foaf:depicts`

The conceptual model is represented with as an interactive diagram (Miro board), available on the project website (interactive Miro board).

### Authority URIs used:
- Renzo Renzi — VIAF: <http://viaf.org/viaf/40486517> · Wikidata: <https://www.wikidata.org/wiki/Q56179169>
- Federico Fellini — VIAF: <http://viaf.org/viaf/76315386>
- Cineteca di Bologna — VIAF: <http://viaf.org/viaf/124960346>
- Bologna — Wikidata: <https://www.wikidata.org/wiki/Q1891>
- Cinema Fulgor — Wikidata: <https://www.wikidata.org/wiki/Q36839368>

---

# Part III — Knowledge Representation: Create Data

## 6. CSV Files

A dedicated CSV file was created for each of the 15 items, structuring metadata according to the relevant institutional standard and placing items in dialogue through shared entities and relationships.

Two global files handle the semantic layer:
- `rrr_entities.csv` — all domain entities (people, places, works, institutions…) with their identifiers and authority URIs
- `rrr_triples.csv` — explicit relationships between entities, expressed as subject–predicate–object triples

All local identifiers use the shared project prefix `rrr` (namespace: `https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/`).

The CSV files are the starting point for the RDF generation performed by the dedicated Python scripts.

---

## 7. XML/TEI Document

One item — Sequence I of the screenplay of *La Strada*, taken from the book *Il primo Fellini* — was encoded as a full-text document using **TEI P5**.

The TEI file (`tei_xslt/lastrada.xml`) includes:
- a complete `<teiHeader>` with bibliographic and archival metadata (title, author, editor, publisher, date, language)
- a `<particDesc>` listing all named characters with their actors linked to VIAF authority records
- a `<settingDesc>` with all places appearing in the sequence
- semantic tagging of dialogues, stage directions, characters, and places within the text body
- logical structuring of scenes into labelled segments

---

## 8. XML to HTML Transformation

The TEI file is transformed into a web-publishable HTML edition through an **XSLT** pipeline:

- The stylesheet `tei_xslt/tei2html_lastrada.xsl` defines the transformation rules from TEI elements to HTML.
- The Python script `scripts/xml_to_html.py` applies the stylesheet using the `lxml` library (`etree.XSLT`), parsing both the XML source and the XSL stylesheet and writing the result to `html/lastrada.html`.

The resulting HTML edition can be consulted at: [html/lastrada.html](html/lastrada.html)

---

## 9. XML/TEI to RDF Transformation

The TEI file is also transformed into RDF using a dedicated **Python** script:

- `scripts/xml_to_rdf.py` uses `xml.etree.ElementTree` to parse the TEI/XML source and extract structured metadata: title, author, editor, publisher, date, language, characters (with actor VIAF links), and places.
- Extracted data is mapped to RDF triples using **RDFLib**, reusing Schema.org, Dublin Core Terms, FOAF, and CIDOC-CRM vocabularies.
- The output is serialized as a Turtle file (`tei_xslt/lastrada_screenplay.ttl`) and also as RDF/XML (`tei_xslt/lastrada_screenplay.rdf`).

---

## 10. RDF Dataset (CSV → RDF via Python)

The full RDF dataset is produced as a **set of modular Turtle files** (`ttl/*.ttl`), one per cultural heritage item.

Dedicated Python scripts in `scripts/` (one per item, e.g. `la_strada_film.py`, `renzi_portrait.py`, etc.) each:
1. Read the item-specific CSV file.
2. Map the CSV fields to RDF triples according to the conceptual model, using **RDFLib**.
3. Serialize the output as an individual Turtle file in the `ttl/` directory.

The script `scripts/merging.py` merges all individual Turtle files into `ttl/full_dataset.ttl` for easier inspection and evaluation.

The dataset as a whole integrates:
- creative works (books, films, drawings, photographs, sound recordings…)
- agents and institutions (Renzi, Fellini, Masina, Rota, Cineteca di Bologna…)
- events (premiere, documentary production, film-related activities…)
- links to external authority files (VIAF, Wikidata, GeoNames)
- inter-item relationships expressed as RDF triples

The dataset is modular by design: files can be loaded as separate named graphs or merged into a single RDF graph for SPARQL querying.

**Downloads:**
- Full dataset: [ttl/full_dataset.ttl](ttl/full_dataset.ttl)
- TTL directory: <https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/tree/main/ttl>

---

# Part IV — Project Information

## 11. Website

The full project is published as a **GitHub Pages website** at:
➞ <https://cinefiles25.github.io/TheRevolussionOfRenzoRenzi/>

The site includes: project overview, item list with metadata, conceptual and theoretical graphs, TEI-based HTML edition, RDF dataset downloads, photo gallery, team, and full documentation.

---

## 12. Team

The project was developed within the course *Information Science and Cultural Heritage* (a.y. 2024–2025), University of Bologna – DHDK.

- **Laura Bortoli** — Metadata for book, caricature, photograph, soundtrack and interview; TEI/XML encoding and XSLT transformation; website. 
- **Claudia Romanello** — Metadata for documentary, Renzo Renzi Library, additional photographs and screenplay; conceptual graph; TEI/XML to RDF transformation; contribution to website content. 
- **Qinghao (River) Chen** — Metadata for film, family photos and additional visual materials; theoretical graph; contribution to site structure and RDF checks.

**Supervision:**
- *Text Encoding & Semantic Representation*: Marilena Daquino
- *Knowledge Organization in Libraries & Archives*: Francesca Tomasi
