from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")

# GRAPH
g = Graph()

# Bindings
g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)
g.bind("dc", dc)
g.bind("crm", crm)
g.bind("foaf", foaf)

# ENTITIES
portrait = URIRef(rrr + "portrait_of_renzo_renzi")
renzi = URIRef(rrr + "renzo_renzi")
cineteca = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")

# LOAD CSV
df = read_csv("../csv/renzi_portrait.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((portrait, RDF.type, schema.Photograph))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Title
    if row.get("title"):
        g.add((portrait, dcterms.title, Literal(row["title"])))

    # Creator (literal)
    if row.get("creator"):
        g.add((portrait, dcterms.creator, Literal(row["creator"])))

    # Depicted person (resource)
    g.add((portrait, foaf.depicts, renzi))

    # Depicted event (literal)
    if row.get("depicted_event"):
        g.add((portrait, dc.subject, Literal(row["depicted_event"])))

    # Color
    if row.get("colour"):
        g.add((portrait, schema.color, Literal(row["colour"])))

    # Material / technique
    if row.get("material_technique"):
        g.add((portrait, dcterms.medium, Literal(row["material_technique"])))

    # Physical description
    if row.get("physical_description"):
        g.add((portrait, dcterms.extent, Literal(row["physical_description"])))

    # Carrier type
    if row.get("carrier_type"):
        g.add((portrait, crm.P45_consists_of, Literal(row["carrier_type"])))

    # File format
    if row.get("format"):
        g.add((portrait, schema.fileFormat, Literal(row["format"])))

    # Collection (literal description only)
    if row.get("collection"):
        g.add((portrait, dcterms.relation, Literal(row["collection"])))

    # Notes
    if row.get("notes"):
        g.add((portrait, dcterms.description, Literal(row["notes"])))

    # Rights
    if row.get("rights"):
        g.add((portrait, dcterms.rights, Literal(row["rights"])))

    # COLLECTION & LOCATION
    g.add((portrait, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, portrait))
    g.add((portrait, crm.P52_has_current_owner, cineteca))
    g.add((portrait, schema.location, renzi_library))


# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/renzi_portrait.ttl")
print("renzi_portrait.ttl generated successfully!")
