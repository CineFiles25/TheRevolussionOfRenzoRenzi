from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES
rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
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
g.bind("foaf", foaf)
g.bind("owl", owl)
g.bind("skos", skos)

# ENTITIES (to be customized per script)
item = URIRef(rrr + "ITEM_ID_HERE")

# Common entities already defined in the main dataset
renzi = URIRef(rrr + "renzo_renzi")
renzi_collection = URIRef(rrr + "renzi_collection")
cineteca = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")

# LOAD CSV (customize filename)
df = read_csv("../csv/ITEM_CSV_FILENAME.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE (customize)
g.add((item, RDF.type, schema.CreativeWork))

# CSV → RDF MAPPING
for _, row in df.iterrows():
    # Identifier
    if row.get("id"):
        g.add((item, dcterms.identifier, Literal(row["id"])))
    # Title
    if row.get("title"):
        g.add((item, dcterms.title, Literal(row["title"])))
    # Alternative title
    if row.get("other_title_information"):
        g.add((item, dcterms.alternative, Literal(row["other_title_information"])))
    # Creator (example)
    g.add((item, dcterms.creator, renzi))
    # Description
    if row.get("description"):
        g.add((item, dcterms.description, Literal(row["description"])))
    # Date
    if row.get("date"):
        g.add((item, dcterms.created, Literal(row["date"], datatype=XSD.date)))
    # Language
    if row.get("language"):
        g.add((item, dcterms.language, Literal(row["language"])))
    # Rights
    if row.get("rights"):
        g.add((item, dcterms.rights, Literal(row["rights"])))

    # Authority files — VIAF
    if row.get("viaf_uri"):
        g.add((item, owl.sameAs, URIRef(row["viaf_uri"])))
    # Authority files — Wikidata
    if row.get("wikidata_uri"):
        g.add((item, owl.sameAs, URIRef(row["wikidata_uri"])))
    # Authority files — LCNAF / altre authority
    if row.get("authority_uri"):
        g.add((item, owl.sameAs, URIRef(row["authority_uri"])))
    # Concetto SKOS
    if row.get("skos_concept_uri"):
        g.add((item, skos.closeMatch, URIRef(row["skos_concept_uri"])))

    # COLLECTION & LOCATION
    g.add((item, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, item))
    g.add((item, crm.P52_has_current_owner, cineteca))
    g.add((item, schema.location, bologna))

# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/ITEM_OUTPUT_FILENAME.ttl")
print("TTL file generated successfully!")
