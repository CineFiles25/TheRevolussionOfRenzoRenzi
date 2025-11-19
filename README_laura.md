# The “Revolussion” of Renzo Renzi — Sub-Collection (Laura Bortoli)  
### *Information Science and Cultural Heritage Project*   
*Master’s Degree in Digital Humanities & Digital Knowledge — University of Bologna*

---

## 1. Overview
This sub-collection gathers **five cultural heritage objects** preserved by the **Cineteca di Bologna**, curated and modeled by **Laura Bortoli** as part of the group project *The “Revolussion” of Renzo Renzi*.

All items come from (or relate to) the **Renzo Renzi Collection**, an archival body that embodies Renzi’s analogue, pre-digital idea of **interlinked film knowledge** — an intuitive precursor of today’s *Linked Open Data*.

This individual contribution includes:

• metadata standard analysis (ISBD(G), Scheda F, Scheda OA, FIAF, ISBD(NBM))  
• theoretical and conceptual modeling (including Graffoo diagrams)  
• TEI encoding and XSLT transformation  
• CSV-based data preparation  
• Python-based RDF generation  
• integration into the team’s shared knowledge graph using the prefix ```rrr```:  

---

## 2. Items Included in This Sub-Collection

| ID  | Item                                   | Standard     | Type                |
|-----|-----------------------------------------|--------------|---------------------|
| 1a  | Il primo Fellini                        | ISBD(G)      | Book                |
| 1b  | La Strada, Sequence I (TEI excerpt)     | TEI P5       | Screenplay segment  |
| 2   | Premiere photograph (Fulgor)            | Scheda F     | Archival photograph |
| 3   | Fellini → Renzi caricature              | Scheda OA    | Visual artwork      |
| 4   | Renzo Renzi & Columbus Film (2000 interview) | FIAF     | Video interview     |
| 5   | La Strada soundtrack (original release) | ISBD(NBM)    | Music recording     |

All objects are linked through shared entities (Renzo Renzi, Federico Fellini, Giulietta Masina, Nino Rota, etc.) and consolidated within the global project graph.

---

## 3. Objectives  
This work aims to:  
## 3.1. Metadata & Conceptual Modeling  
• produce **theoretical models** (natural language) for each object  
• construct a **Graffoo conceptual model** describing entities and relationships across the Renzi sub-collection  
## 3.2. Dataset Creation
• build a structured CSV dataset:  
&nbsp;&nbsp;• ```rrr_entities.csv``` → list of entities and authorities  
&nbsp;&nbsp;• ```rrr_triples.csv``` → semantic relationships  
## 3.3. RDF / LOD Pipeline  
• implement an **automatic RDF pipeline** (CSV → Python → Turtle) using ```rdflib```  
• generate a clean, human-readable, and standards-compliant **Turtle graph**
## 3.4. TEI Encoding & Transformation
• encode *La Strada*, Sequence I in **TEI P5**  
• transform it into **HTML** using a dedicated **XSLT stylesheet**  
## 3.5. Integration  
• integrate all results into the group project using the shared prefix:  
```
https://cinefiles25.github.io/renzi/
```
ensuring consistency with LOD practices and the overall group ontology.

---

## 4. Folder Structure  
```
renzi/
│── rrr_entities.csv
│── rrr_triples.csv
│── ttl/
│   └── rrr.ttl
│
├── book_il_primo_fellini/
│   ├── TEI/
│   │   └── lastrada.xml
│   ├── XSLT/
│   │   └── tei2html_lastrada.xsl
│   └── HTML/
│       └── lastrada.html
│
└── scripts/
    ├── build_rrr_rdf.py
    ├── compare_ttl.py
    └── tei_to_html.py
```

---

## 5. RDF Generation
The Turtle file is **never edited manually**.  
Reproducibility is ensured by the pipeline:  
```
python scripts/build_rrr_rdf.py
```
Output:  
```
ttl/rrr.ttl
```
The script reads both CSV files (```entities``` and ```triples```), resolves authorities (VIAF, Wikidata), and produces a coherent RDF graph aligned with Schema.org, DC Terms, FOAF, SKOS, and PROV.

---

## 6. TEI → HTML Pipeline  
Transform the TEI excerpt using:  
```  
python scripts/tei_to_html.py
```
This applies:  
```  
book_il_primo_fellini/HTML/lastrada.html
```
and outputs an accessible HTML version:  
```  
book_il_primo_fellini/HTML/lastrada.html
```

The TEI encoding includes:  
• cast list (role vs. actor, with VIAF IDs)  
• structured stage directions  
• page breaks (```<pb>```)  
• scene segmentation (```<div type="scene">```)  
• semantic markup of setting, speech, transitions

---

## 7. Context and Rationale  
Renzo Renzi’s archival practice — linking books, scripts, images, interviews, and memories — anticipates LOD by decades.  
This project **translates Renzi’s analogue network** into a digital semantic framework, combining:  

• descriptive cataloguing  
• TEI text encoding  
• authority control  
• RDF & LOD principles  
• conceptual modeling

The sub-collection demonstrates how heterogeneous film heritage objects can be integrated into a unified, queryable knowledge graph.

---

## 8. Author  
**Laura Bortoli**  
Master’s Degree in Digital Humanities & Digital Knowledge  
University of Bologna — a.y. 2025/2026
