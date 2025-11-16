# Renzi Sub-Collection  
### *Knowledge Organization & Information Science — Semester Project*  
**Information Science & Cultural Heritage (Tomasi & Daquino)**  
*Master’s Degree in Digital Humanities & Digital Knowledge — University of Bologna*

---

## Overview
This module contains the work related to five cultural heritage items from the **Cineteca di Bologna**, selected and curated by **Laura Bortoli**.  
These items belong to the *Renzo Renzi* archival context and are used to explore:

- metadata standards  
- conceptual modeling  
- TEI encoding  
- Linked Data representation  
- RDF graph generation from CSV  

---

## Selected Items

- **Book — “Il primo Fellini”** → *ISBD(G)*  
- **TEI-encoded excerpt** from *La Strada* (Sequence I)  
- **Photograph “Fulgor”** → *Scheda F*  
- **Caricature of Renzo Renzi by Federico Fellini** → *OA*  
- **Video interview “Renzo Renzi & Columbus Film” (2000)** → *FIAF*  
- **Soundtrack of “La Strada”** → *ISBD(NBM)*  

---

## Objectives
This sub-collection aims to produce:

1. **A conceptual model (Graffoo)** describing relationships among all items  
2. **A coherent CSV dataset** as the authoritative metadata source  
3. **A Python pipeline** that automatically generates RDF/Turtle  
4. **A final Turtle file (`renzi.ttl`)** integrated into the group knowledge graph  
5. **A TEI → HTML transformation**, demonstrating textual encoding and publication

This workflow ensures transparency, reproducibility, and alignment with Linked Open Data principles.

---

## Folder Structure



renzi/
│── entities_renzi.csv # Authority list of entities
│── triples_renzi.csv # Semantic relationships between entities
│── build_renzi_rdf.py # Main Python script (rdflib)
│── compare_ttl.py # Compares two Turtle graphs
│── renzi.ttl # Automatically generated RDF output
│
│── book_Il_primo_Fellini/
│ │── TEI/
│ │ └── lastrada.xml
│ │── HTML/
│ │ └── lastrada.html
│ │── XSLT/
│ │ └── tei2html_lastrada.xsl
│ └── scripts/
│ └── tei_to_html.py


---

## RDF Generation

Run the following command to generate the RDF/Turtle representation:

```bash
python build_renzi_rdf.py


The output will be:

renzi.ttl


Note: The Turtle file is always generated automatically from the CSV source.
No manual edits are performed to ensure reproducibility.

TEI → HTML Transformation

The TEI excerpt of La Strada can be transformed into HTML using:

python tei_to_html.py


The XSLT stylesheet (tei2html_lastrada.xsl) defines the transformation rules.

The resulting file is saved as:

book_Il_primo_Fellini/HTML/lastrada.html

Notes

This sub-collection will be integrated into the group’s global knowledge graph.

All metadata choices follow the standards and methodologies discussed during the course.

The workflow always follows: CSV → Python → RDF, never the opposite.

Author

Laura Bortoli
Master’s Degree in Digital Humanities & Digital Knowledge
University of Bologna — a.y. 2024/2025
