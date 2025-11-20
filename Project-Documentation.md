# Project Documentation  
## The “Revolussion” of Renzo Renzi  
*Information Science and Cultural Heritage – University of Bologna (2024–2025)*

---

## TO DO LIST

✓ choose 15 objects from different institutions and types  
✓ identify metadata standards used by providers  
✓ list all objects + standards  
✓ contact Cineteca di Bologna for object information  
✓ divide the work across team members  
✓ decide modelling practices  
✓ create all CSV files  
✓ produce TEI/XML sample + XSLT  
✓ convert CSV to RDF (Python)  
✓ produce RDF dataset for all items  
✓ build the website  

---

# GOAL OF THE PROJECT  

**Create structured, interoperable data starting from a cultural idea and a curated set of items related to it.**

The final deliverables must include:  
- CSV metadata for each item  
- TEI/XML encoding + HTML transformation  
- XML/TEI → RDF transformation  
- RDF dataset of the entire collection  
- A conceptual model based on existing ontologies  
- A website documenting the whole process

---

# INSTRUCTIONS (from course requirements)

### 1. **Find the idea**  
We chose **Renzo Renzi**, critic, filmmaker, archivist and great promoter of film culture in Bologna, one of the key figures who enabled the growth and development of the Cineteca after its founding in 1962. The Cineteca's library is in fact named after him..

### 2. **Select 10+ items**  
Requirements:  
- different object types (books, photographs, drawings, audiovisuals, sound, documents)  
- at least one **full-text** item  
- possibly from different institutions  

### 3. **Metadata Analysis**  
Identify the metadata standards used by the institutions holding each item.

### 4. **Theoretical Model**  
Describe all features of the selected items *in natural language*, starting from institutional metadata + additional contextual knowledge (authors, subjects, authority control, classifications).

### 5. **Conceptual Model**  
Create a *formal* presentation of the domain using **existing ontologies**:  
- RDF / RDFS  
- OWL  
- SKOS  
- DCTerms, Schema.org, FOAF  
- CIDOC-CRM (for museum logic)  
- RiC-O (for archival logic)  
- IFLA LRM (bibliographic thinking)

The conceptual model must be expressed with a **graphical representation** (Grafoo-like diagram).

### 6. **Create the Deliverables**
- ✓ CSV files (one table per item)  
- ✓ TEI/XML sample  
- ✓ XML→HTML transformation (XSLT)  
- ✓ XML→RDF transformation (Python)  
- ✓ RDF dataset for all items  
- ✓ Website

---

# USEFUL INFOS (project conventions)

- **Case:** `snake_case`  
- **Name of the project:** **The “Revolussion” of Renzo Renzi**  
- **Prefix:** `rrr:`  
- **Institutions involved:** primarily **Cineteca di Bologna**, ICCU, IMDb, Renzi family archives  
- **Authority files used:** VIAF, Wikidata, TGN  

### Description text used on the website  
*Long before Linked Open Data entered the vocabulary of Digital Humanities, Renzo Renzi was already building it by hand...*  
> Renzi assembled books, scripts, drawings, photographs, interviews, and film documents into an interconnected archive where each object illuminated the others. His method created a **network of film knowledge**: themes, stories, production histories, anecdotes, materials, and memories woven together with the instinct of someone who understood that cinema is not linear – it is relational.  
> For this reason, the Cineteca di Bologna, and particularly the Renzo Renzi Collection, can be read as an analogue prototype of Linked Open Data.

---

# AUTHORITY FILES (people, places, institutions)

| Entity | Authority link |
|--------|----------------|
| Renzo Renzi | VIAF: http://viaf.org/viaf/40486517 — Wikidata: https://www.wikidata.org/wiki/Q56179169 |
| Federico Fellini | VIAF: http://viaf.org/viaf/76315386 — Wikidata: https://www.wikidata.org/wiki/Q7371 |
| Cineteca di Bologna | VIAF: http://viaf.org/viaf/124960346 — Wikidata: https://www.wikidata.org/wiki/Q1092493 |
| Bologna (place) | VIAF: http://viaf.org/viaf/257723025 — Wikidata: https://www.wikidata.org/wiki/Q1891 |

---

# USEFUL LINKS (for documentation + project)

- **GitHub repo:** https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi  
- **Drive folder with the original items:** (internal link)  

---

# METADATA STANDARDS USED  

### **Bibliographic (Books, Textual Items)**  
- **ISBD(G)**  
- **ISBD(NBM)** for non-book material  

### **Archival**  
- **ISAD(G)**  

### **Museum / Artistic / Visual Items**  
- **Scheda F** (ICCD) – photographs  
- **Scheda OA** (ICCD) – drawings, caricatures  

### **Audiovisual / Film**  
- **FIAF Cataloguing Rules**  

---

# ONTOLOGIES REUSED  
- **Dublin Core Terms (DCTerms)**  
- **FOAF**  
- **Schema.org**  
- **RiC-O**  
- **CIDOC CRM**  
- **IFLA LRM**  
- **SKOS** (for types, roles)

These were used only *for conceptual modelling and semantic alignment*, not for creating a brand-new ontology.

---

# WHAT OTHER STUDENTS SAID (important for grading)

- Tomasi cares about **organisation, justification, and modelling choices**  
- Every selected object must have a **URI**  
- One object must be a **full text**  
- CSV files must be produced manually if institutions do not provide them  
- Tomasi wants **analysis**, not alignment  
- The team does **not** need to build a new ontology  

---

# FLOW OF THE PROJECT

# 1. Choosing the objects    

Color code used internally:  
- **Laura → orange**  
- **Claudia → purple**  
- **Chen → blue**

<img width="600" height="632" alt="Screenshot 2025-11-20 001157" src="https://github.com/user-attachments/assets/bdead909-2afe-4346-946a-b0e3540a7a42" />


### Final selection of 15 objects (for Tomasi)

1. *Il primo Fellini* – Book — **ISBD(G)**  
2. *Guida per camminare all’ombra* — Screenplay — **ISAD**  
3. Photo 1 — **Scheda F**  
4. Drawing “Gelsomina” — **Scheda OA**  
5. Drawing caricature of Renzo Renzi — **Scheda OA**  
6. Photo 2 (Aldo Ferrari) — **Scheda F**  
7. Photo 3 “La Strada 01” — **Scheda F**  
8. Photo 4 “La Strada 004” — **Scheda F**  
9. Videointerview Renzo Renzi (2000) — **FIAF**  
10. Film *La Strada* — **FIAF (ISBD NBM)**  
11. Soundtrack *La Strada* — **ISBD (NBM)**  
12. Family photo — **Scheda F**  
13. Documentary *Quando il Po è dolce* — **ISBD(NBM)**  
14. Renzo Renzi Library (building) — **ICCU cataloguing rules**  
15. Letter — **FIAF (document)**  

---

# 2. Metadata Analysis

## LAURA’S ITEMS  

| Object | Type | Provider | Metadata Standard |
|-------|------|----------|-------------------|
| 1. *Il primo Fellini* | Book / Text | Cineteca di Bologna | ISBD(G) |
| 2. Photo 1 “Prima de *La Strada* al Fulgor” | Photograph | Cineteca di Bologna | Scheda F |
| 3. “Perché Federico non fa la rivolussione?” | Drawing / Caricature | Cineteca di Bologna | Scheda OA |
| 4. Videointerview Renzo Renzi (2000) | Audiovisual | Cineteca di Bologna | FIAF Rules |
| 5. *La Strada* Soundtrack | Sound Recording | Cineteca di Bologna | ISBD(NBM) |

## CLAUDIA’S ITEMS  

| Object | Type | Provider | Metadata Standard |
|-------|------|----------|-------------------|
| 2. *Guida per camminare all’ombra* | Printed screenplay | Cineteca di Bologna | ISAD(G) |
| 6. Photo from set | Photo | Renzi family | Scheda F |
| 12. Family photo | Photo | Renzi family | Scheda F |
| 13. Documentary *Quando il Po è dolce* | Documentary | Cineteca / IMDb | ISBD(NBM) |
| 14. Renzo Renzi Library | Building | ICCU | REICAT / ISBD(NBM) |

*(We have to add River's!!)*

---

# 3. Theoretical Model  
*A natural-language description of the domain.*

The objects in the Renzi collection form an interconnected network of entities:
- **People** (Renzo Renzi, Federico Fellini, Aldo Ferrari, Nino Rota…)  
- **Works** (book, screenplay, documentaries, film, soundtrack…)  
- **Images** (photographs, caricatures, drawings…)  
- **Events** (interviews, film production, documentary creation…)  
- **Places** (Bologna, Cineteca di Bologna…)  
- **Institutions** (Renzi Library, Cineteca, ICCU…)  

Relationships include:
- creation, authorship  
- depiction  
- performance/contribution  
- production  
- documentation  
- archival holding  

This natural-language model is the basis for the conceptual model.

---

# 4. Conceptual Model (Formal)

The modelling reuses:

### **Classes**
- `schema:CreativeWork`  
- `schema:Photograph`  
- `schema:Person`  
- `schema:AudioObject`  
- `foaf:Agent`  
- `dcterms:Location`  
- `rico:Record`  
- `cidoc:E21_Person`, `cidoc:E22_Man-Made_Object` (concept inspiration)

### **Properties**
- `dcterms:creator`  
- `dcterms:subject`  
- `schema:dateCreated`  
- `schema:locationCreated`  
- `schema:isPartOf`  
- `foaf:depiction`  
- `rico:heldBy`  

A final diagram (Grafoo style) is included in `/docs/conceptual_model.png`.

---

# 5. CSV → RDF Transformation

Python scripts include:

### `build_rrr_rdf.py`
- reads `rrr_entities.csv` + `rrr_triples.csv`  
- constructs a graph using RDFLib  
- serializes as `rrr.ttl`  

### `compare_ttl.py`
- compares two RDF dumps  
- useful for debugging ontology changes  

---

# 6. TEI → HTML Transformation  
The TEI edition of *La Strada* (`tei/lastrada.xml`) is transformed into HTML through  
`tei2html_lastrada.xsl`.  
Output: `site/lastrada.html`.

---

# 7. Website Structure  

The website includes:
- landing page  
- about the project  
- list of items  
- TEI → HTML section  
- RDF download page  
- conceptual model  
- team section  

Published via GitHub Pages.

---

# 8. Team Roles

### **Laura**
- Metadata creation (book, photograph, caricature, interview, soundtrack)  
- TEI encoding  
- XSLT transformation  
- RDF generation scripts  
- Entity and triples modelling  
- Website content (La Strada edition)

*(Claudia and River, add yours!!)*

---

# END OF DOCUMENTATION  

This file is intended for instructor evaluation and internal transparency about the project workflow.






