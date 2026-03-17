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
photo = URIRef(rrr + "photo_la_strada_fighter")
film = URIRef(rrr + "la_strada_film")
masina = URIRef(rrr + "giulietta_masina")
cineteca = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
renzi_collection = URIRef(rrr + "renzi_collection")

# LOAD CSV
df = read_csv("../csv/photo_la_strada_fighter.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((photo, RDF.type, schema.Photograph))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Title
    if row.get("title"):
        g.add((photo, dcterms.title, Literal(row["title"])))

    # Alternative title
    if row.get("other_title_information"):
        g.add((photo, dcterms.alternative, Literal(row["other_title_information"])))

    # Depicted person (resource)
    g.add((photo, foaf.depicts, masina))

    # Depicted event (literal)
    if row.get("depicted_event"):
        g.add((photo, dc.subject, Literal(row["depicted_event"])))
        
    # Depicted place (literal description)
    if row.get("depicted_place"):
        g.add((photo, schema.location, Literal(row["depicted_place"])))


    # Creation year
    if row.get("creation_year"):
        g.add((photo, dcterms.created, Literal(row["creation_year"], datatype=XSD.gYear)))

    # Color
    if row.get("colour"):
        g.add((photo, schema.color, Literal(row["colour"])))

    # Material / technique
    if row.get("material_technique"):
        g.add((photo, dcterms.medium, Literal(row["material_technique"])))

    # Physical description
    if row.get("physical_description"):
        g.add((photo, dcterms.extent, Literal(row["physical_description"])))

    # Notes
    if row.get("notes"):
        g.add((photo, dcterms.description, Literal(row["notes"])))

    # Identifiers
    if row.get("identifiers"):
        g.add((photo, dcterms.identifier, Literal(row["identifiers"])))

    # Related works (literal description)
    if row.get("related_works"):
        g.add((photo, dcterms.relation, Literal(row["related_works"])))

    # Rights
    if row.get("rights"):
        g.add((photo, dcterms.rights, Literal(row["rights"])))

    # Resource type
    if row.get("resource_type"):
        g.add((photo, dcterms.type, Literal(row["resource_type"])))

    # Language
    if row.get("language"):
        g.add((photo, dcterms.language, Literal(row["language"])))

    # Link to La Strada (resource)
    g.add((photo, schema.about, film))

    # COLLECTION & LOCATION
    g.add((photo, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, photo))
    g.add((photo, crm.P52_has_current_owner, cineteca))
    g.add((photo, schema.location, bologna))


# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/photo_la_strada_fighter.ttl")
print("photo_la_strada_fighter.ttl generated successfully!")
