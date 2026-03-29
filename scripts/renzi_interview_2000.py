from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES
rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
owl = Namespace("http://www.w3.org/2002/07/owl#")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")

# GRAPH
g = Graph()

# Bindings
g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)
g.bind("dc", dc)
g.bind("crm", crm)
g.bind("owl", owl)
g.bind("skos", skos)

# ENTITIES
interview = URIRef(rrr + "renzi_interview_2000")
renzi = URIRef(rrr + "renzo_renzi")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")
cineteca = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")

# LOAD CSV
df = read_csv("../csv/renzi_interview_2000.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((interview, RDF.type, schema.Interview))

# CSV → RDF MAPPING
for _, row in df.iterrows():
    # Identifier
    if row.get("id"):
        g.add((interview, dcterms.identifier, Literal(row["id"])))
    # Standard
    if row.get("standard"):
        g.add((interview, dcterms.conformsTo, Literal(row["standard"])))
    # Resource type
    if row.get("resource_type"):
        g.add((interview, dcterms.type, Literal(row["resource_type"])))
    # Titles
    if row.get("title"):
        g.add((interview, dcterms.title, Literal(row["title"])))
    if row.get("other_title_information"):
        g.add((interview, dcterms.alternative, Literal(row["other_title_information"])))
    # Interviewee (resource)
    g.add((interview, schema.interviewee, renzi))
    g.add((interview, schema.about, renzi))
    # Interviewee (literal)
    if row.get("interviewee"):
        g.add((interview, dc.subject, Literal(row["interviewee"])))
    # Director (literal only)
    if row.get("director"):
        g.add((interview, schema.director, Literal(row["director"])))
    # Interviewer
    if row.get("interviewer"):
        g.add((interview, schema.interviewer, Literal(row["interviewer"])))
        g.add((interview, dcterms.contributor, Literal(row["interviewer"])))
    # Production company
    if row.get("production_company"):
        g.add((interview, dcterms.publisher, Literal(row["production_company"])))
    # Production place (literal)
    if row.get("production_place"):
        g.add((interview, schema.location, Literal(row["production_place"])))
    # Production place (resource)
    g.add((interview, schema.location, bologna))
    # Production year
    if row.get("production_year"):
        g.add((interview, dcterms.created, Literal(row["production_year"], datatype=XSD.gYear)))
    # Duration
    if row.get("duration"):
        g.add((interview, schema.duration, Literal(row["duration"])))
    # Color
    if row.get("colour"):
        g.add((interview, schema.color, Literal(row["colour"])))
    # Sound
    if row.get("sound"):
        g.add((interview, dcterms["format"], Literal(row["sound"])))
    # Format
    if row.get("format"):
        g.add((interview, dcterms["format"], Literal(row["format"])))
    # Language
    if row.get("language"):
        g.add((interview, schema.inLanguage, Literal(row["language"])))
    # Rights
    if row.get("rights"):
        g.add((interview, dcterms.rights, Literal(row["rights"])))
    # Description
    if row.get("description"):
        g.add((interview, dcterms.description, Literal(row["description"])))
    if row.get("notes"):
        g.add((interview, dcterms.description, Literal(row["notes"])))

    # Authority files — VIAF
    if row.get("viaf_uri"):
        g.add((interview, owl.sameAs, URIRef(row["viaf_uri"])))
    # Authority files — Wikidata
    if row.get("wikidata_uri"):
        g.add((interview, owl.sameAs, URIRef(row["wikidata_uri"])))
    # Authority files — LCNAF / altre authority
    if row.get("authority_uri"):
        g.add((interview, owl.sameAs, URIRef(row["authority_uri"])))
    # Concetto SKOS
    if row.get("skos_concept_uri"):
        g.add((interview, skos.closeMatch, URIRef(row["skos_concept_uri"])))

    # COLLECTION & LOCATION
    g.add((interview, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, interview))
    g.add((interview, crm.P52_has_current_owner, cineteca))
    g.add((interview, schema.location, renzi_library))

# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/renzi_interview_2000.ttl")
print("renzi_interview_2000.ttl generated successfully!")
