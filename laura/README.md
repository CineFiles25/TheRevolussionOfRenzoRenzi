Renzi Sub-Collection — Knowledge Organization & Information Science

Semester Project, Information Science & Cultural Heritage (Tomasi & Daquino)
Master’s Degree in Digital Humanities & Digital Knowledge — University of Bologna

Overview

This module contains the work related to five cultural heritage items from the Cineteca di Bologna, selected and curated by Laura Bortoli.
These items belong to the Renzo Renzi archival context and are used to explore metadata standards, conceptual modeling, TEI encoding, and Linked Data representation.

Selected Items

Book — “Il primo Fellini” → ISBD(G)

TEI-encoded excerpt of Sequence I from La Strada

Photograph “Fulgor” → Scheda F

Caricature of Renzo Renzi by Federico Fellini → OA

Video interview: Renzo Renzi & Columbus Film (2000) → FIAF

Soundtrack of “La Strada” → ISBD(NBM)

Objectives

This sub-collection aims to produce:

A conceptual model (Graffoo) describing the relationships among all items

A coherent CSV dataset, used as the project’s authoritative data source

A Python pipeline that automatically generates an RDF/Turtle representation

A final Turtle file (renzi.ttl) to be integrated into the group's global knowledge graph

A TEI → HTML transformation, showcasing textual encoding and digital publication

This workflow ensures transparency, reproducibility, and alignment with Linked Open Data principles.

Folder Structure
renzi/
│── entities_renzi.csv            # Authority list of entities
│── triples_renzi.csv             # Semantic relationships between entities
│── build_renzi_rdf.py            # Main Python script (rdflib)
│── compare_ttl.py                # Compares two Turtle graphs
│── renzi.ttl                     # Automatically generated RDF output
│
│── book_Il_primo_Fellini/
│   │── TEI/
│   │   └── lastrada.xml
│   │── HTML/
│   │   └── lastrada.html
│   │── XSLT/
│   │   └── tei2html_lastrada.xsl
│   └── scripts/
│       └── tei_to_html.py

RDF Generation

To generate the RDF/Turtle representation:

python build_renzi_rdf.py


The resulting file will be:

renzi.ttl


This file is always produced automatically from the CSV files, ensuring data consistency and avoiding manual edits.

TEI → HTML Transformation

The TEI excerpt of La Strada (Sequence I) can be transformed into HTML using:

python tei_to_html.py


The XSLT stylesheet (tei2html_lastrada.xsl) defines the transformation and layout.

The resulting file is saved as:

book_Il_primo_Fellini/HTML/lastrada.html

Notes

This sub-collection will be integrated into the global knowledge graph created by the group.

All metadata choices follow the recommendations and standards discussed during the course.

No Turtle file is ever edited manually: the workflow is CSV → Python → RDF for full reproducibility.

Author

Laura Bortoli
Master’s Degree in Digital Humanities & Digital Knowledge
University of Bologna — a.y. 2024/2025