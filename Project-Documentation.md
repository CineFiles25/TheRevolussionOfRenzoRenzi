# Project Documentation  
## The “Revolussion” of Renzo Renzi  
*Information Science and Cultural Heritage – University of Bologna (2024–2025)*

---

# 1. Project Overview

*The “Revolussion” of Renzo Renzi* is a Digital Humanities project focused on the archival, bibliographic, and audiovisual materials related to **Renzo Renzi** (1919–2004), a central figure in the history of film culture in Bologna.

Renzi’s work as critic, filmmaker, researcher, and curator created an analogue network of interrelated objects—books, drawings, photographs, interviews, film materials—that anticipates the logic of Linked Open Data.

The project aims to **model, encode, and publish** a selection of these materials using Cultural Heritage standards, TEI/XML, RDF, and a web interface.

---

# 2. Project Goals

The project follows the official requirements of the course:
- Select a coherent **cultural domain** (Renzo Renzi and the Renzo Renzi Collection).
- Choose **at least 10 heterogeneous items** (we selected 15).
- Identify and reuse **institutional metadata standards**.
- Describe each item through a **theoretical model** (natural language analysis).
- Develop a **conceptual model** reusing existing ontologies.
  
Produce:
- CSV metadata
- a TEI-encoded text + XSLT
- CSV → RDF transformation
- an RDF dataset (as multiple Turtle files)
- documentation and a website

The main objective is to turn a set of analogue cultural materials into a **structured, interoperable digital dataset** aligned with cultural heritage best practices.

---

# 3. Selected Items

The dataset includes 15 cultural heritage objects, chosen to represent different media, institutions, standards, and descriptive traditions:

1. *Il primo Fellini* — Book — **ISBD(G)**
2. *Guida per camminare all’ombra* — Screenplay — **ISAD(G)**
3. Photograph: “Premiere of *La Strada* at Cinema Fulgor” — **Scheda F**
4. Drawing “Gelsomina col tamburo” — **Scheda OA**
5. Caricature “Perché Federico non fa la rivolussione?” — **Scheda OA**
6. Set photograph by Aldo Ferrari — **Scheda F**
7. Photograph “La Strada 01” — **Scheda F**
8. Photograph “La Strada 004” — **Scheda F**
9. Videointerview: *Il cinema a Bologna: Renzo Renzi e la Columbus film* (2000) — **FIAF**
10. *La Strada* (1954), Federico Fellini — **ISBD(NBM) + FIAF**
11. *La Strada* soundtrack (Nino Rota) — **ISBD(NBM)**
12. Family photograph — **Scheda F**
13. Documentary *Quando il Po è dolce* (1952) — **ISBD(NBM) + FIAF**
14. Renzo Renzi Library — **ICCU / ISIL identification**
15. Letter (film-related materials) — **FIAF Film-Related Materials**

---

# 4. Metadata Standards Used

## Bibliographic:
- ISBD(G)
- ISBD(NBM)

## Archival:
- ISAD(G)

## Museums / Visual Items:
- ICCD Scheda F
- ICCD Scheda OA

## Audiovisual:
- FIAF Cataloguing Rules

These standards guided the structure of the CSV files and the descriptive granularity.

---

# 5. Theoretical Model (Natural-Language Analysis)

Each object was analysed following the descriptive logic of its reference standard, identifying:
- intrinsic features (title, date, format, technique…)
- roles and actors (creators, performers, contributors…)
- relationships to other entities (about, depicts, documents…)
- institutional context (holding institution, collection, physical location…)
- authority control (VIAF, Wikidata, ISIL, ISNI…)

This qualitative analysis established a **domain narrative** connecting:
- **People** (Renzi, Fellini, Masina, Rota…)
- **Works** (film, documentary, book, soundtrack, interview…)
- **Images** (photographs, drawings, caricatures…)
- **Events** (film premiere, documentary production…)
- **Institutions** (Cineteca di Bologna, Renzi Library…)
- **Places** (Bologna, Po River Delta, Cinema Fulgor…)

These narratives provided the foundation for the conceptual model.

---

# 6. Conceptual Model (Ontological Reuse)

The conceptual model reuses existing vocabularies without creating a new ontology.

## Ontologies and Vocabularies:
- Dublin Core Terms (DCTerms)
- Schema.org
- FOAF
- SKOS
- CIDOC CRM (conceptual reference)
- RiC-O (archival logic)
- IFLA LRM (bibliographic logic)

## Core classes and relationships reused
- `schema:CreativeWork`, `schema:ImageObject`, `schema:VideoObject`, `schema:MusicRecording`
- `schema:Person`, `schema:Organization`, `schema:Place`
- `dcterms:creator`, `dcterms:subject`, `dcterms:date`, `schema:about`, `schema:locationCreated`
- `foaf:depicts`
- `schema:hasPart`, `dcterms:hasPart`

The conceptual model is summarized in a **Grafoo-style diagram** included in the documentation.

---

# 7. Data Production

## CSV Metadata

A dedicated CSV file was created for each of the 15 items.  
Two global files structure the semantic layer:  
- `rrr_entities.csv` → entities of the domain (people, places, works…)  
- `rrr_triples.csv` → relations between those entities  

All identifiers follow **snake_case** and use a shared prefix (`rrr:`).

These CSV files are the starting point for the RDF generation performed by the Python scripts.

---

# 8. TEI Encoding & XSLT Transformation

One item (*La Strada*, sequence I) was encoded using **TEI P5**.  
The XSLT stylesheet `tei2html_lastrada.xsl` transforms the TEI file into a web-publishable HTML edition.

The TEI edition includes:
- a full `<teiHeader>` with bibliographic and archival metadata
- semantic tagging of people, places and film-specific structures
- logical structuring of scenes and segments

---

# 9. RDF Dataset

The RDF dataset is produced as a **set of modular Turtle files** (`ttl/*.ttl`), one per cultural heritage item (and related entities).

Dedicated Python scripts in the `scripts/` directory:

- read the item-specific CSV metadata (and, where relevant, the global entity and triple CSVs),
- map them to RDF triples using **RDFLib**,
- serialize each item as an individual Turtle file in the `ttl/` directory.

`compare_ttl.py` is used to:
- validate differences between Turtle serializations,
- support debugging and consistency checks during the modelling phase.

Taken together, the Turtle files integrate:
- items
- related entities
- inter-item relationships
- authority URIs
- locations, subjects, creators, collections

The dataset is modular by design: it can be loaded as separate graphs or merged into a single RDF graph for querying.

---

# 10. Website

The full project is published as a **GitHub Pages website**, including:
- project overview
- item list with metadata
- TEI → HTML edition
- RDF dataset (Turtle files)
- conceptual model
- documentation
- team

➞ https://cinefiles25.github.io/TheRevolussionOfRenzoRenzi/

---

# 11. Institutions & Authority Files

## Authority control used
- VIAF
- Wikidata
- ISIL / ICCU
- ISNI (for institutions)

## Example links
- Renzo Renzi — VIAF: <http://viaf.org/viaf/40486517>  
- Federico Fellini — VIAF: <http://viaf.org/viaf/76315386>  
- Cineteca di Bologna — VIAF: <http://viaf.org/viaf/124960346>  
- Bologna — Wikidata: <https://www.wikidata.org/wiki/Q1891>  
- Cinema Fulgor — Wikidata: <https://www.wikidata.org/wiki/Q36839368>  

---

# 12. Team Roles

The project was collaboratively developed by:
- **Laura Bortoli** — TEI encoding, XSLT, CSV metadata, RDF modelling, website content
- **Claudia Romanello** — Photographic items, documentary metadata, screenplay analysis, Python scripts
- **Qinghao (River) Chen** — Metadata extraction, item analysis, web structure, RDF validation

---

# End of Documentation

This file provides a complete, instructor-oriented description of the project workflow, methodological choices, standards, and deliverables.

