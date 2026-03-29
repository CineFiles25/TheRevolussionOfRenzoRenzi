# The "Revolussion" of Renzo Renzi  
*A Digital Humanities & Linked Open Data Project*  
**Information Science and Cultural Heritage – University of Bologna (2024–2025)**

---

## Overview  

The *"Revolussion" of Renzo Renzi* is a digital humanities project dedicated to exploring the archival and cultural ecosystem built by **Renzo Renzi** (1919–2004): film critic, curator, writer, and one of the key figures behind the creation of the **Cineteca di Bologna**.

The project investigates Renzi's analogue "web of cinema knowledge" by studying **15 heterogeneous cultural heritage items** conserved at — or connected to — the **Renzo Renzi Collection**.
The project integrates:

- **TEI/XML scholarly encoding** of a textual item
- **XSLT transformation** for online publication
- **CSV-based metadata extraction** from institutional standards
- **Semantic modelling and LOD / RDF production**
- **Reuse of CH standards and ontologies**
- **Unified web interface** published with GitHub Pages

The goal is to transform an analogue archive into a **Linked Open Data ecosystem**, while documenting the methodological steps behind data modelling in DH.

---

## Project Structure  
```
csv/                  → Metadata tables for all items + authority entity registry
scripts/              → Python scripts (CSV → RDF transformation and merging)
tei_xslt/             → TEI XML + XSLT stylesheet
ttl/                  → Individual RDF files + full_dataset.ttl
html/                 → Transformed TEI HTML
img/                  → Photographs, stills, visual materials
index.html            → Website home
project-documentation.html
style.css
README.md
```

A full explanation of the workflow is provided in **Project-Documentation.md**.

---

## Objectives

1. **Define a coherent thematic scope** (Renzo Renzi and his network around *La Strada* and the Renzo Renzi Collection).  
2. **Extract metadata** using authoritative CH standards:
   - ISBD(G), ISBD(NBM)
   - ICCD Scheda F, ICCD Scheda OA
   - FIAF rules for audiovisual items
   - ISAD(G) for archival documents  
3. **Encode a text item in TEI P5** and publish it through **XSLT**.
4. **Develop a conceptual model** by reusing:
   - Dublin Core Terms
   - Schema.org
   - FOAF
   - SKOS
   - OWL
     (*RiC-O and CIDOC CRM used as conceptual references*)
5. **Generate an integrated RDF dataset** (`full_dataset.ttl`).  
6. **Publish the whole project on the web** via GitHub Pages.

---

## Selected Cultural Heritage Items

The dataset includes **15 items**, structured as:

- **Book / full text** — *Il primo Fellini* (ISBD(G))
- **TEI-encoded screenplay excerpt**
- **4 photographs** (ICCD Scheda F)
- **2 drawings / caricatures** (ICCD Scheda OA)
- **Sound recording** — *La Strada soundtrack* (ISBD NBM)
- **Audiovisual interview** (FIAF)
- **Documentary film** — *Quando il Po è dolce* (ISBD NBM + FIAF)
- **Renzo Renzi Library** (ICCU / ISIL identification)
- **Family photo / set photo** (Scheda F)

For each item, the project includes:

- CSV metadata
- Source standard
- Holding institution
- URI references (VIAF/Wikidata), centralised in `rrr_entities.csv`
- RDF representation
- Links to related items (interlinking)

---

## Standards & Ontologies

### **Metadata Standards**
- ISBD(G), ISBD(NBM)
- ICCD Scheda F
- ICCD Scheda OA
- FIAF Cataloguing Rules
- ISAD(G)

### **Reused Models / Ontologies**
- **Dublin Core Terms**
- **Schema.org**
- **FOAF**
- **SKOS**
- **OWL** (for `owl:sameAs` authority linking)
- *RiC-O and CIDOC CRM referenced for conceptual modelling*

### **Technologies Used**
- TEI P5
- XSLT 1.0
- RDF/Turtle
- Python, RDFLib
- GitHub Pages 

---

## Scripts

### `scripts/`  
This folder contains all Python scripts used to transform CSV metadata into RDF/Turtle files and to produce the unified dataset.

### Item-level scripts  
Each script converts a single CSV file into a corresponding Turtle file in `ttl/`.  
Examples:  
- `po_documentary.py`  
- `drawing_gelsomina_lastrada.py`  
- `photo_la_strada_fighter.py`  
- `book_il_primo_fellini.py`

### Core scripts
- `base.py`  
  Template and shared namespace definitions reused across item scripts.
- `merging.py`  
  Merges all individual Turtle files into a unified RDF graph (`full_dataset.ttl`). Also reads `rrr_entities.csv` to inject `owl:sameAs` triples linking project entities to external authority files (VIAF, Wikidata, GeoNames, SBN).
- `xml_to_html.py`  
  Transforms TEI XML into HTML using the project's XSLT stylesheet.
- `xml_to_rdf.py`  
  Converts TEI XML materials into RDF triples, extracting persons, places, scenes, and speeches.

### Authority linking pipeline  
External authority URIs (VIAF, Wikidata, GeoNames, OPAC SBN) are centralised in `csv/rrr_entities.csv`, in the `sameAs` column. During merging, `merging.py` reads this file and automatically generates `owl:sameAs` triples for all entities that have an external URI. This ensures a single point of truth for authority references across the entire dataset.

---

## RDF Dataset

The RDF dataset is composed of modular Turtle files, each representing a single cultural heritage item, person, place, or institutional entity.  
All files are stored in the `ttl/` directory:

→ https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/tree/main/ttl

Alongside the modular files, the project includes a unified graph:

- **`full_dataset.ttl`** — the complete integrated RDF dataset, including all `owl:sameAs` authority links  
  (generated automatically via `merging.py`)

This structure reflects the distributed nature of the archive while ensuring transparency, modularity, and ease of reuse.

---

## Website  
The website presents:

- The TEI edition of the selected text
- All metadata tables
- Complete RDF dataset
- Explanations of standards, modelling choices, and workflow
- Image gallery
- Downloadable files and scripts

→ https://cinefiles25.github.io/TheRevolussionOfRenzoRenzi/

---

## Contributors  

The project was developed by:

- **Laura Bortoli**  
  laura.bortoli@studio.unibo.it  
  GitHub: https://github.com/lauraaa13

- **Claudia Romanello**  
  claudia.romanello@studio.unibo.it  
  GitHub: https://github.com/claudiarom

- **Qinghao Chen**  
  qinghao.chen@studio.unibo.it  
  GitHub: https://github.com/River-Qinghao

All project members contributed collaboratively to metadata extraction, TEI encoding, RDF modelling, Python scripting, and interface development.

---

## Acknowledgments
The authors warmly thank **Anna Fiaccarini**, Head of the Cineteca di Bologna Library since 1997, for her guidance, availability, and support throughout the project.
Her expertise and historical knowledge of the Renzo Renzi Collection were essential to shaping the research and ensuring its cultural accuracy.

---

## References  

- **Renzo Renzi (Wikipedia)** – https://it.wikipedia.org/wiki/Renzo_Renzi
- **Cineteca di Bologna – Renzi Fund** – https://cinetecadibologna.it/biblioteca/
- **Metadata Standards** – ISBD, ICCD, ISAD(G), FIAF
- **Ontologies** – DCTerms, Schema.org, FOAF, SKOS, OWL, RiC-O, CIDOC CRM

---

## License  
This project is released under a **CC BY-SA 4.0** license.
