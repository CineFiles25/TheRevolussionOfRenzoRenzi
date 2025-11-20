# The “Revolussion” of Renzo Renzi  
*A Digital Humanities & Linked Open Data Project*  
**Information Science and Cultural Heritage – University of Bologna (2024–2025)**

---

## Overview  

*The “Revolussion” of Renzo Renzi* is a digital humanities project that explores the archival universe of **Renzo Renzi** (1919-2004), filmmaker, critic, researcher and co-founder of the **Cineteca di Bologna**.

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
/data/ → CSV descriptions of all CH items
/tei/ → TEI XML edition + XSLT transformation
/rdf/ → Generated RDF dataset (rrr.ttl)
/scripts/ → XML→HTML and CSV→RDF Python scripts
/site/ → HTML pages for web publication
/docs/ → Additional project documentation (conceptual model, diagrams)
```

A detailed, step-by-step description of the entire workflow is available in **Project-Documentation.md**.

---

## Objectives

1. Build a structured dataset starting from a coherent cultural theme (Renzo Renzi and the “Revolussion” around *La Strada*).  

2. Convert descriptive metadata into CSV using institutional standards (ISBD(G), ISBD(NBM), Scheda F, Scheda OA, FIAF rules, ISAD).  

3. Encode one full-text item in **TEI/XML** and transform it into **HTML** via XSLT.

4. Create a **conceptual model** reusing existing ontologies (Dublin Core Terms, Schema.org, FOAF, RiC-O, CIDOC CRM).  

5. Produce a complete **RDF dataset** for all selected objects.

6. Present the results in an accessible **website** built for publication.

---

## Data Types Included

- **Book / full text** – *Il primo Fellini*  
- **Photographs** (Scheda F, ICCD)  
- **Caricatures / Drawings** (Scheda OA, ICCD)  
- **Audiovisual interview** (FIAF rules)  
- **Sound recording / soundtrack** (ISBD NBM)  
- **Screenplays, documents, and film material**

Each object is documented with:

- description  
- provider and reference institution  
- metadata standard used  
- CSV representation  
- RDF serialization  
- connections to related entities  
- external authority links (VIAF, Wikidata, TGN)

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
Compares two RDF serializations to track differences across versions (graph integrity checking).

### ```tei2html_lastrada.xsl```  
Transforms the TEI edition of *La Strada* into HTML.

---

## Website  
The website presents:

- the TEI-encoded text of *La Strada*  
- descriptive metadata  
- RDF dataset  
- conceptual / theoretical model  
- diagrams  
- item pages for each cultural object  

*(Insert website link once published)*

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
- **Metadata standards & ontologies:**  
  - Dublin Core Terms  
  - FOAF  
  - Schema.org  
  - RiC-O  
  - CIDOC CRM  
  - FIAF, ISBD, ICCD  

---

## License  
This project is released under a **CC BY-SA 4.0** license.

---
