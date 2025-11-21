# The “Revolussion” of Renzo Renzi  
*A Digital Humanities & Linked Open Data Project*  
**Information Science and Cultural Heritage – University of Bologna (2024–2025)**

---

## Overview  

*The “Revolussion” of Renzo Renzi* is a digital humanities project that explores the archival universe of **Renzo Renzi** (1919-2004), an exemplary figure in Italy as a film critic, writer, cultural communicator, and organizer. We approached his figure, important yet often known only to "insiders" of the Bologna film world, through the mediation of Anna Fiaccarini, director of the Bologna Film Archive: in fact, Renzi was one of the founders of the Cinema Commission of the city of Bologna, which later gave rise to the Cineteca and its cultural archive.

The project integrates:

- **TEI/XML scholarly text encoding**  
- **XSLT transformation for web publication**  
- **CSV-based metadata extraction and analysis**  
- **Linked Open Data modelling (RDF/Turtle)**  
- **Reuse of major cultural heritage standards**  
- **A conceptual model inspired by existing ontologies (DC, Schema.org, FOAF)**  
- **A web interface presenting all deliverables**

The dataset includes **15 heterogeneous cultural heritage items** (books, photographs, drawings, sound recordings, interviews, documents) described, encoded, and semantically linked.

---

## Project Structure  

```
csv/                  → CSV metadata for all items  
html/                 → HTML pages (incl. TEI-to-HTML edition)
img/                  → Photographs, stills and visual materials
scripts/              → Python scripts for dataset generation
tei_xslt/             → TEI XML + XSLT transformation
ttl/                  → RDF dataset (rrr.ttl)
project-documentation.html
readme.html           → HTML export of this README
index.html            → Website home
style.css             → Website stylesheet
```

A detailed, step-by-step description of the entire workflow is available in **Project-Documentation.md**.

---

## Objectives

1. Build a structured dataset starting from a coherent cultural theme (Renzo Renzi and the “Revolussion” around *La Strada*).  

2. Convert descriptive metadata into CSV using institutional standards (ISBD(G), ISBD(NBM), Scheda F, Scheda OA, FIAF rules, ISAD).  

3. Encode one major item using **TEI P5** and publish it through **XSLT**.

4. Build a **conceptual model** aligned with: Dublin Core Terms, Schema.org, FOAF, RiC-O, CIDOC CRM.  

5. Produce a complete **RDF dataset** for all selected objects.

6. Publish all deliverables in an accessible **website** built with GitHub Pages.

---

## Data Types Included

- **Book / full text** – *Il primo Fellini*  
- **Photographs** (Scheda F, ICCD)  
- **Caricatures / Drawings** (Scheda OA, ICCD)  
- **Audiovisual interview** (FIAF rules)  
- **Sound recording / soundtrack** (ISBD NBM)  
- **Screenplays, documents, and film material**
- **Architectural / institutional item** – Renzo Renzi Library

Each object is documented with:

•&nbsp;descriptive metadata  
•&nbsp;provider & holding institution  
•&nbsp;reference standard  
•&nbsp;CSV entry  
•&nbsp;RDF representation  
•&nbsp;inter-entity links  
•&nbsp;authority identifiers (VIAF/Wikidata)

---

## Technologies & Standards

### **Metadata Standards**
- ISBD(G), ISBD(NBM)  
- ICCD Scheda F, ICCD Scheda OA  
- ISAD(G) – archival description  
- FIAF Cataloguing Rules for film & audiovisual materials  

### **Ontologies & Vocabularies**
- **Dublin Core Terms (DCTerms)**  
- **Schema.org**  
- **FOAF**  
- **RiC-O** (Records in Contexts, for archival context)  
- **CIDOC-CRM** (reference for museum-domain thinking)
- **SKOS** for controlled values  

### **Languages & Tools**
- TEI P5  
- XSLT 1.0  
- RDF/Turtle  
- Python + RDFLib  
- GitHub Pages  

---

## Scripts Included

### ```build_rrr_rdf.py```  
Transforms the CSV metadata into a structured RDF graph using RDFLib, generating ```rrr.ttl```.

### ```compare_ttl.py```  
Compares two Turtle serializations to detect differences or validate updates.

### ```tei2html_lastrada.xsl```  
Transforms the TEI edition of *La Strada* into HTML.

---

## Website  
The website includes:

•&nbsp;TEI-encoded *La Strada* edition
•&nbsp;Metadata & analysis
•&nbsp;RDF dataset (Turtle)
•&nbsp;Photo gallery
•&nbsp;Team & supervision
•&nbsp;Documentation & downloads

→ https://cinefiles25.github.io/TheRevolussionOfRenzoRenzi/

---

## Contributors  

The project was developed by:

- **Laura Bortoli** – TEI edition, XSLT, RDF generation, CSV metadata creation  
- **Claudia Romanello** – Photographs, documentary metadata, screenplays  
- **Chen Qinghao** – Additional items, film metadata, interface work  

Full per-member breakdown available in *Project-Documentation.md*.

---

## References  

- **Renzo Renzi (Wikipedia):** https://it.wikipedia.org/wiki/Renzo_Renzi  
- **Cineteca di Bologna – Renzi Fund:** https://cinetecadibologna.it/biblioteca/  
- **Metadata standards & ontologies:** ISBD, ICCD, FIAF, DCTerms, Schema.org, FOAF, RiC-O, CIDOC CRM
---

## License  
This project is released under a **CC BY-SA 4.0** license.

---
