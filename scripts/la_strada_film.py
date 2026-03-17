from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES
rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")

# GRAPH
g = Graph()

# Bindings
g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)

# ENTITY
film = URIRef(rrr + "la_strada_film")
fellini = URIRef(rrr + "federico_fellini")

# LOAD CSV
df = read_csv("../csv/la_strada_film.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((film, RDF.type, schema.Movie))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Title
    if row.get("title"):
        g.add((film, dcterms.title, Literal(row["title"])))

    # Alternative title
    if row.get("other_title_information"):
        g.add((film, dcterms.alternative, Literal(row["other_title_information"])))

    # Director (resource)
    g.add((film, schema.director, fellini))

    # Production company
    if row.get("production_company"):
        g.add((film, schema.productionCompany, Literal(row["production_company"])))

    # Country of origin → FIX HERE (schema.location)
    if row.get("country"):
        g.add((film, schema.location, Literal(row["country"])))

    # Language
    if row.get("language"):
        g.add((film, schema.inLanguage, Literal(row["language"])))

    # Year of release
    if row.get("publication_year"):
        g.add((film, dcterms.issued, Literal(row["publication_year"], datatype=XSD.gYear)))

    # Length / duration
    if row.get("length"):
        g.add((film, dcterms.extent, Literal(row["length"])))

    if row.get("duration"):
        g.add((film, schema.duration, Literal(row["duration"])))

    # Color
    if row.get("colour"):
        g.add((film, schema.color, Literal(row["colour"])))

    # Sound
    if row.get("sound"):
        g.add((film, schema.sound, Literal(row["sound"])))

    # Resource type
    if row.get("resource_type"):
        g.add((film, dcterms.type, Literal(row["resource_type"])))

    # Notes / description
    if row.get("notes"):
        g.add((film, dcterms.description, Literal(row["notes"])))

# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/la_strada_film.ttl")
print("la_strada_film.ttl generated successfully!")
