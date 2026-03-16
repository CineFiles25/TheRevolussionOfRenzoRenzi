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

# ENTITIES ALREADY DEFINED IN THE MAIN DATASET
artwork = URIRef(rrr + "caricature_fellini_renzi")
fellini = URIRef(rrr + "federico_fellini")
renzi = URIRef(rrr + "renzo_renzi")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")
cineteca = URIRef(rrr + "cineteca_di_bologna")

# LOAD CSV
df = read_csv("../csv/caricature_fellini_renzi.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((artwork, RDF.type, schema.VisualArtwork))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Identifier
    if row.get("id"):
        g.add((artwork, dcterms.identifier, Literal(row["id"])))

    # Titles
    if row.get("title"):
        g.add((artwork, dcterms.title, Literal(row["title"])))

    if row.get("other_title_information"):
        g.add((artwork, schema.alternateName, Literal(row["other_title_information"])))

    # Description / inscription
    if row.get("inscription"):
        g.add((artwork, dcterms.description, Literal(row["inscription"])))

    if row.get("description"):
        g.add((artwork, dcterms.description, Literal(row["description"])))

    # Creator (resource)
    g.add((artwork, schema.creator, renzi))

    # Depicted person
    g.add((artwork, schema.about, fellini))

    # Creation date
    if row.get("creation_date"):
        g.add((artwork, dcterms.created, Literal(row["creation_date"])))

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

    # Language
    if row.get("language"):
        g.add((artwork, schema.inLanguage, Literal(row["language"])))

    # Standard
    if row.get("standard"):
        g.add((artwork, dcterms.conformsTo, Literal(row["standard"])))

    # COLLECTION & LOCATION (resources)
    g.add((artwork, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, artwork))
    g.add((artwork, schema.location, renzi_library))
    g.add((artwork, crm.P52_has_current_owner, cineteca))


# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/caricature_fellini_renzi.ttl")
print("caricature_fellini_renzi.ttl generated successfully!")
