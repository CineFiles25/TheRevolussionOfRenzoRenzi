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
artwork = URIRef(rrr + "drawing_gelsomina_lastrada")
la_strada = URIRef(rrr + "la_strada_film")
renzi = URIRef(rrr + "renzo_renzi")
masina = URIRef(rrr + "giulietta_masina")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")
cineteca = URIRef(rrr + "cineteca_di_bologna")

# LOAD CSV
df = read_csv("../csv/drawing_gelsomina_lastrada.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((artwork, RDF.type, schema.VisualArtwork))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Title
    if row.get("title"):
        g.add((artwork, dcterms.title, Literal(row["title"])))

    # Creator (resource)
    g.add((artwork, schema.creator, renzi))

    # Depicted person
    g.add((artwork, foaf.depicts, masina))

    # Creation date
    if row.get("creation_date"):
        g.add((artwork, dcterms.created, Literal(row["creation_date"], datatype=XSD.gYear)))

    # Technique / material
    if row.get("technique"):
        g.add((artwork, dcterms.medium, Literal(row["technique"])))

    if row.get("material"):
        g.add((artwork, dcterms.material, Literal(row["material"])))

    # Dimensions
    if row.get("dimensions"):
        g.add((artwork, dcterms.extent, Literal(row["dimensions"])))

    # Rights
    if row.get("rights"):
        g.add((artwork, dcterms.rights, Literal(row["rights"])))

    # Description
    if row.get("description"):
        g.add((artwork, dcterms.description, Literal(row["description"])))

    # Link to La Strada
    g.add((artwork, schema.about, la_strada))

    # COLLECTION & LOCATION
    g.add((artwork, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, artwork))
    g.add((artwork, schema.location, renzi_library))
    g.add((artwork, crm.P52_has_current_owner, cineteca))


# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/drawing_gelsomina_lastrada.ttl")
print("drawing_gelsomina_lastrada.ttl generated successfully!")
