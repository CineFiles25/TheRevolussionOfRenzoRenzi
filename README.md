# The “Revolussion” of Renzo Renzi  
*A Digital Humanities & Linked Open Data Project*  
**Information Science and Cultural Heritage – University of Bologna (2024–2025)**

---

## Overview  

The *“Revolussion” of Renzo Renzi* is a digital humanities project dedicated to exploring the archival and cultural ecosystem built by **Renzo Renzi** (1919–2004): film critic, curator, writer, and one of the key figures behind the creation of the **Cineteca di Bologna**.

The project investigates Renzi’s analogue “web of cinema knowledge” by studying **15 heterogeneous cultural heritage items** conserved at — or connected to — the **Renzo Renzi Collection**.
The project integrates:

It integrates:

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
csv/                  → Metadata tables for all items
script/               → Python scripts (CSV → RDF transformation)
tei_xslt/             → TEI XML + XSLT stylesheet
ttl/                  → RDF dataset (rrr.ttl)
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
     (RiC-O and CIDOC CRM used as conceptual references)
5. **Generate an integrated RDF dataset** (rrr.ttl).  
6. **Publish the whole project on the web** via GitHub Pages.

---

## Selected Cultural Heritage Items

The dataset includes **15 items**, structured as:

- **Book / full text** — *Il primo Fellini* (ISBD(G))
- **TEI-encoded screenplay excerpt**
- **4 photographs** (ICCD Scheda F)
- **2 drawings / caricatures** (ICCD Scheda OA)
- **Sound recording: La Strada soundtrack** (ISBD NBM)
- **Audiovisual interview** (FIAF)
- **Documentary film “Quando il Po è dolce”** (ISBD NBM + FIAF)
- **Renzo Renzi Library** (ICCU / ISIL identification)
- **Family photo / set photo** (Scheda F)

For each item, the project includes:

- CSV metadata
- Source standard
- Holding institution
- URI references (VIAF/Wikidata)
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
- *RiC-O and CIDOC CRM referenced for conceptual modelling*

### **Technologies Used**
- TEI P5
- XSLT 1.0
- RDF/Turtle
- Python, RDFLib
- GitHub Pages 

---

## Scripts Included

### `scripts/`  
This folder contains all Python scripts used to transform CSV metadata into RDF/Turtle files and to validate the resulting dataset.

### `*_item.py` (one per cultural heritage item)  
Each script converts a single CSV file into a corresponding Turtle file.  
Examples:  
- `po_documentary.py`  
- `drawing_gelsomina_lastrada.py`  
- `photo_la_strada_fighter.py`  
- `portrait_of_renzo_renzi.py`  

### `merging.py`  
Merges all individual Turtle files into a unified RDF graph (`full_dataset.ttl`).

### `test_sparql.py`  
Runs technical validation tests (types, missing properties, duplicates, non-numeric years).

### `test_sparql_C.py`  
Runs conceptual and narrative validation tests (coherence of relations, temporal logic, place modelling, entity completeness).

These scripts ensure that the final RDF dataset is both **technically valid** and **semantically coherent**.

---

## RDF Dataset

The RDF dataset is composed of modular Turtle files, each representing a single cultural heritage item, person, place, or institutional entity.  
All files are stored in the `ttl/` directory:

→ https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/tree/main/ttl

Alongside the modular files, the project includes a unified graph:

- **`full_dataset.ttl`** — the complete integrated RDF dataset  
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

- **Laura Bortoli** – TEI encoding, XSLT design, RDF generation, CSV creation, metadata harmonization
- **Claudia Romanello** – Photograph metadata, documentary and screenplay analysis, Python scripts
- **Qinghao Chen** – Additional metadata extraction, interface work, RDF validation

Full breakdown in **Project-Documentation.md**.

---

## References  

- **Renzo Renzi (Wikipedia)** – https://it.wikipedia.org/wiki/Renzo_Renzi
- **Cineteca di Bologna – Renzi Fund** – https://cinetecadibologna.it/biblioteca/
- **Metadata Standards** – ISBD, ICCD, ISAD(G), FIAF
- **Ontologies** – DCTerms, Schema.org, FOAF, SKOS, RiC-O, CIDOC CRM

---

## License  
This project is released under a **CC BY-SA 4.0** license.

---
