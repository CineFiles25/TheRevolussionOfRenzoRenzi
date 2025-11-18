# The “Revolussion” of Renzo Renzi — Sub-Collection (Laura Bortoli)  
### *Information Science and Cultural Heritage Project*   
*Master’s Degree in Digital Humanities & Digital Knowledge — University of Bologna*

---

## Overview
This sub-collection gathers five cultural heritage items held by the **Cineteca di Bologna**, selected and curated by **Laura Bortoli** as part of the group project *The “Revolussion” of Renzo Renzi*.

These items belong to the **Renzo Renzi Collection**, an archival corpus that reflects Renzi’s pioneering approach to interlinking film-related materials — a pre-digital analogue of **Linked Open Data**.

The work encompasses:

- metadata standard analysis
- theoretical and conceptual modeling (Graffoo)
- TEI encoding and transformation
- dataset creation through CSV
- RDF graph generation through Python
- integration into the group’s global knowledge graph

---

## Selected Items

  **1a.  Book — Il primo Fellini** → ISBD(G)   
  **1b.  TEI-encoded excerpt — La Strada, Sequence I**   
  **2.   Photograph “Fulgor” (Fellini & Masina at the premiere)** → Scheda F    
  **3.   Caricature of Renzo Renzi by Federico Fellini** → Scheda OA   
  **4.   Video interview: Renzo Renzi & Columbus Film (2000)** → FIAF  
  **5.   Soundtrack of La Strada** → ISBD(NBM)

---

## Objectives
This sub-collection aims to produce:

1. **A complete theoretical model (natural language)** for each item, based on the standards above
2. **A conceptual model (Graffoo)** mapping entities, relationships, and linking principles across the Renzi Collection  
3. **A structured CSV dataset** 
        •  ```entities_renzi.csv``` → authority entities
        •  ```triples_renzi.csv``` → semantic relationships  
4. **An automatic RDF generation pipeline** using **rdflib**, following the workflow: **CSV** → **Python** → **Turtle (.ttl)**  
5. **TEI Encoding + Transformation**
        •  TEI XML of the *La Strada* Sequence I
        •  XSLT + Python transformation to HTML
6. **Integration into the team’s knowledge graph** using the shared project prefix **rrr**: ```https://example.org/rrr/```

This workflow ensures transparency, reproducibility, and alignment with Linked Open Data principles.

---

## Folder Structure

```

renzi/
│── entities_renzi.csv
│── triples_renzi.csv
│── ttl/
│   └── rrr.ttl
│
├── book_il_primo_fellini/
│   ├── la_strada_sequence1.md
│   ├── TEI/
│   │   └── lastrada.xml
│   ├── HTML/
│   │   └── lastrada.html
│   └── XSLT/
│       └── tei2html_lastrada.xsl
│
└── scripts/
    ├── build_rrr_rdf.py
    ├── compare_ttl.py
    └── tei_to_html.py


```

---

## RDF Generation

To generate or update the Turtle dataset:
```
python scripts/build_rrr_rdf.py
```
This produces:
```
ttl/rrr.ttl
```
The Turtle file is **never edited manually**.
All updates occur through the CSV → Python pipeline for reproducibility.

---

## TEI → HTML Transformation

The TEI excerpt of *La Strada* can be transformed into HTML using:
```
python scripts/tei_to_html.py
```
This applies the XSLT stylesheet:
```
book_il_primo_fellini/XSLT/tei2html_lastrada.xsl
```
And outputs:
```
book_il_primo_fellini/HTML/lastrada.html
```
---

## Project Context

Renzo Renzi anticipated LOD principles long before Digital Humanities adopted them.  
Through his curatorial practice, he built a **networked film archive** where books, scripts, reviews, drawings, photographs, and interviews were meaningfully interconnected.  
The **Renzi Collection** is thus an analogue precursor of Linked Open Data — structured by intellectual relationships rather than digital infrastructure.  
This sub-collection extends that idea into a modern semantic framework.

---

## Author

**Laura Bortoli**  
Master’s Degree in Digital Humanities & Digital Knowledge  

University of Bologna — a.y. 2025/2026
