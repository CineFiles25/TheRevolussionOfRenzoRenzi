from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")

# GRAPH

g = Graph()

g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)
g.bind("dc", dc)
g.bind("foaf", foaf)

# ENTITIES

po_documentary = URIRef(rrr + "quando_il_po_è_dolce")
renzo_renzi = URIRef(rrr + "renzo_renzi")
enzo_masetti = URIRef(rrr + "enzo_masetti")
delta_po_river = URIRef(rrr + "delta_po_river")

# LOAD CSV

df = read_csv("../csv/po_documentary.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE

g.add((po_documentary, RDF.type, schema.Movie))

# CSV → RDF MAPPING

for _, row in df.iterrows():

    # Titles
    if row.get("title"):
        g.add((po_documentary, dcterms.title, Literal(row["title"])))

    if row.get("other_title_information"):
        g.add((po_documentary, dcterms.alternative, Literal(row["other_title_information"])))

    # Edition / publication year
    if row.get("edition"):
        g.add((po_documentary, dcterms.issued, Literal(row["edition"], datatype=XSD.gYear)))

    if row.get("publication_year"):
        g.add((po_documentary, dcterms.issued, Literal(row["publication_year"], datatype=XSD.gYear)))

    # Director / creator
    g.add((po_documentary, schema.director, renzo_renzi))
    g.add((po_documentary, dcterms.creator, renzo_renzi))

    # Country
    if row.get("country"):
        g.add((po_documentary, schema.countryOfOrigin, Literal(row["country"])))

    # Language
    if row.get("language"):
        g.add((po_documentary, schema.inLanguage, Literal(row["language"])))

    # Production company
    if row.get("production_company"):
        g.add((po_documentary, dcterms.publisher, Literal(row["production_company"])))

    # Length / duration
    if row.get("length"):
        g.add((po_documentary, dcterms.extent, Literal(row["length"])))

    if row.get("duration"):
        g.add((po_documentary, schema.duration, Literal(row["duration"])))

    # Color
    if row.get("colour"):
        g.add((po_documentary, schema.color, Literal(row["colour"])))

    # Film type / format
    if row.get("film_type"):
        g.add((po_documentary, dcterms.medium, Literal(row["film_type"])))

    if row.get("format"):
        g.add((po_documentary, dcterms.format, Literal(row["format"])))

    # Sound
    if row.get("sound"):
        g.add((po_documentary, schema.sound, Literal(row["sound"])))

    # About / place
    g.add((po_documentary, schema.about, delta_po_river))

    # Music
    g.add((po_documentary, schema.musicBy, enzo_masetti))

# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/po_documentary.ttl")
print("po_documentary.ttl generated successfully!")
