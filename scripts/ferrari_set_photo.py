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

# ENTITIES
photo = URIRef(rrr + "ferrari_set_photo")
renzi = URIRef(rrr + "renzo_renzi")
aldo_ferrari = URIRef(rrr + "aldo_ferrari")
cineteca = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
renzi_collection = URIRef(rrr + "renzi_collection")

# LOAD CSV
df = read_csv("../csv/ferrari_set_photo.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((photo, RDF.type, schema.Photograph))

# CSV → RDF MAPPING
for _, row in df.iterrows():
    # Identifier
    if row.get("inventory_number"):
        g.add((photo, schema.identifier, Literal(row["inventory_number"])))
    # Title
    if row.get("title"):
        g.add((photo, dcterms.title, Literal(row["title"])))
    # Creator (resource)
    g.add((photo, dcterms.creator, aldo_ferrari))
    # Depicted person
    g.add((photo, foaf.depicts, renzi))
    # Creation year
    if row.get("creation_year"):
        g.add((photo, schema.dateCreated, Literal(row["creation_year"], datatype=XSD.gYear)))
    # Location created (literal description)
    if row.get("depicted_event"):
        g.add((photo, dcterms.description, Literal(row["depicted_event"])))
    # Color
    if row.get("colour"):
        g.add((photo, schema.color, Literal(row["colour"])))
    # Material / technique
    if row.get("material_technique"):
        g.add((photo, dcterms.material, Literal(row["material_technique"])))
    # Physical description
    if row.get("physical_description"):
        g.add((photo, dcterms.extent, Literal(row["physical_description"])))
    # Carrier type
    if row.get("carrier_type"):
        g.add((photo, crm.P45_consists_of, Literal(row["carrier_type"])))
    # File format
    if row.get("format"):
        g.add((photo, schema.fileFormat, Literal(row["format"])))
    # Rights
    if row.get("rights"):
        g.add((photo, dcterms.rights, Literal(row["rights"])))
    # Notes
    if row.get("notes"):
        g.add((photo, dcterms.description, Literal(row["notes"])))

    # Authority files — VIAF
    if row.get("viaf_uri"):
        g.add((photo, owl.sameAs, URIRef(row["viaf_uri"])))
    # Authority files — Wikidata
    if row.get("wikidata_uri"):
        g.add((photo, owl.sameAs, URIRef(row["wikidata_uri"])))
    # Authority files — LCNAF / altre authority
    if row.get("authority_uri"):
        g.add((photo, owl.sameAs, URIRef(row["authority_uri"])))
    # Concetto SKOS
    if row.get("skos_concept_uri"):
        g.add((photo, skos.closeMatch, URIRef(row["skos_concept_uri"])))

    # COLLECTION & LOCATION
    g.add((photo, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, photo))
    g.add((photo, crm.P52_has_current_owner, cineteca))
    g.add((photo, schema.location, bologna))

# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/ferrari_set_photo.ttl")
print("ferrari_set_photo.ttl generated successfully!")
