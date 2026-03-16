from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

# GRAPH
g = Graph()

# Bindings
g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)
g.bind("dc", dc)
g.bind("crm", crm)

# ENTITIES
letter = URIRef(rrr + "renzi_letter_1942")
renzi = URIRef(rrr + "renzo_renzi")
renzi_collection = URIRef(rrr + "renzi_collection")
cineteca = URIRef(rrr + "cineteca_di_bologna")

# LOAD CSV
df = read_csv("../csv/renzi_letter_1942.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((letter, RDF.type, schema.CreativeWork))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Identifiers
    if row.get("id"):
        g.add((letter, dcterms.identifier, Literal(row["id"])))

    if row.get("identifiers"):
        g.add((letter, dcterms.identifier, Literal(row["identifiers"])))

    # Standard
    if row.get("standard"):
        g.add((letter, dcterms.conformsTo, Literal(row["standard"])))

    # Titles
    if row.get("title"):
        g.add((letter, dcterms.title, Literal(row["title"])))

    if row.get("other_title_information"):
        g.add((letter, dcterms.alternative, Literal(row["other_title_information"])))

    # Creator
    g.add((letter, dcterms.creator, renzi))

    # Other contributors
    if row.get("other_creators"):
        g.add((letter, dcterms.contributor, Literal(row["other_creators"])))

    # Date
    if row.get("date"):
        g.add((letter, dcterms.created, Literal(row["date"], datatype=XSD.date)))

    # Level of description
    if row.get("level_of_description"):
        g.add((letter, dcterms.type, Literal(row["level_of_description"])))

    # Extent
    if row.get("extent"):
        g.add((letter, dcterms.extent, Literal(row["extent"])))

    # Scope and content
    if row.get("scope_and_content"):
        g.add((letter, dcterms.description, Literal(row["scope_and_content"])))

    # Physical description
    if row.get("physical_description"):
        g.add((letter, dcterms.medium, Literal(row["physical_description"])))

    # Material type
    if row.get("material_type"):
        g.add((letter, dcterms.medium, Literal(row["material_type"])))

    # Language
    if row.get("language"):
        g.add((letter, dcterms.language, Literal(row["language"])))

    # Number of pages
    if row.get("pages"):
        g.add((letter, schema.numberOfPages, Literal(row["pages"], datatype=XSD.integer)))

    # Page URIs (resources)
    if row.get("page_uris"):
        for uri in row["page_uris"].split("|"):
            cleaned = uri.strip()
            if cleaned:
                g.add((letter, schema.associatedMedia, URIRef(cleaned)))

    # Holding archive
    g.add((letter, crm.P52_has_current_owner, cineteca))

    # Collection
    g.add((letter, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, letter))

    # Current location (literal)
    if row.get("current_location"):
        g.add((letter, dcterms.spatial, Literal(row["current_location"])))

    # Access conditions
    if row.get("conditions_governing_access"):
        g.add((letter, dcterms.accessRights, Literal(row["conditions_governing_access"])))

    # Reproduction conditions
    if row.get("conditions_governing_reproduction"):
        g.add((letter, dcterms.rights, Literal(row["conditions_governing_reproduction"])))

    # Related works (literal)
    if row.get("related_works"):
        g.add((letter, dcterms.relation, Literal(row["related_works"])))

    # Rights
    if row.get("rights"):
        g.add((letter, dcterms.rights, Literal(row["rights"])))

# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/renzi_letter_1942.ttl")
print("renzi_letter_1942.ttl generated successfully!")
