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
photo = URIRef(rrr + "photo_lastrada_premiere")
film = URIRef(rrr + "la_strada_film")
fellini = URIRef(rrr + "federico_fellini")
masina = URIRef(rrr + "giulietta_masina")
cinema_fulgor = URIRef(rrr + "cinema_fulgor")
cineteca = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
renzi_collection = URIRef(rrr + "renzi_collection")

# TYPES FOR ENTITIES
g.add((cinema_fulgor, RDF.type, schema.Place))
g.add((bologna, RDF.type, schema.Place))

# LOAD CSV
df = read_csv("../csv/photo_lastrada_premiere.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((photo, RDF.type, schema.Photograph))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Identifiers
    if row.get("id"):
        g.add((photo, dcterms.identifier, Literal(row["id"])))

    if row.get("identifiers"):
        for ident in [i.strip() for i in row["identifiers"].split(";") if i.strip()]:
            g.add((photo, dcterms.identifier, Literal(ident)))

    # Standard
    if row.get("standard"):
        g.add((photo, dcterms.conformsTo, Literal(row["standard"])))

    # Resource type
    if row.get("resource_type"):
        g.add((photo, dcterms.type, Literal(row["resource_type"])))

    # Title
    if row.get("title"):
        g.add((photo, dcterms.title, Literal(row["title"])))

    # Alternative title
    if row.get("other_title_information"):
        g.add((photo, dcterms.alternative, Literal(row["other_title_information"])))

    # Notes
    if row.get("notes"):
        g.add((photo, dcterms.description, Literal(row["notes"])))

    # Creator (literal)
    if row.get("creator"):
        g.add((photo, dcterms.creator, Literal(row["creator"])))

    # Depicted persons (resources)
    g.add((photo, foaf.depicts, fellini))
    g.add((photo, foaf.depicts, masina))

    # Depicted people (literal)
    if row.get("depicted_people"):
        g.add((photo, dc.subject, Literal(row["depicted_people"])))

    # Depicted event
    if row.get("depicted_event"):
        g.add((photo, dc.subject, Literal(row["depicted_event"])))

    # Depicted place (literal)
    if row.get("depicted_place"):
        g.add((photo, schema.location, Literal(row["depicted_place"])))

    # Content location (resource)
    g.add((photo, schema.contentLocation, cinema_fulgor))
    g.add((cinema_fulgor, schema.location, bologna))

    # Creation year
    if row.get("creation_year"):
        g.add((photo, dcterms.created, Literal(row["creation_year"], datatype=XSD.gYear)))

    # Color
    if row.get("colour"):
        g.add((photo, schema.color, Literal(row["colour"])))

    # Material / technique
    if row.get("material_technique"):
        g.add((photo, dcterms.medium, Literal(row["material_technique"])))

    # Carrier type
    if row.get("carrier_type"):
        g.add((photo, dcterms.medium, Literal(row["carrier_type"])))

    # Physical description
    if row.get("physical_description"):
        g.add((photo, dcterms.extent, Literal(row["physical_description"])))

    # Inventory number
    if row.get("inventory_number"):
        g.add((photo, dcterms.identifier, Literal(row["inventory_number"])))

    # Rights
    if row.get("rights"):
        g.add((photo, dcterms.rights, Literal(row["rights"])))

    # Link to La Strada (resource)
    g.add((photo, schema.about, film))

    # COLLECTION & LOCATION
    g.add((photo, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, photo))
    g.add((photo, crm.P52_has_current_owner, cineteca))
    g.add((photo, schema.location, bologna))

    # Language
    if row.get("language"):
        g.add((photo, schema.inLanguage, Literal(row["language"])))


# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/photo_lastrada_premiere.ttl")
print("photo_lastrada_premiere.ttl generated successfully!")
