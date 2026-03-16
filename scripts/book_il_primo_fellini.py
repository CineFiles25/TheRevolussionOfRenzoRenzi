from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")

# GRAPH
g = Graph()

# Bindings
g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dc", dc)
g.bind("dcterms", dcterms)

# ENTITIES
book = URIRef(rrr + "book_il_primo_fellini")
fellini = URIRef(rrr + "federico_fellini")
renzi = URIRef(rrr + "renzo_renzi")
series = URIRef(rrr + "series_il_primo_fellini")

# FILMS referenced in the book (already defined in the dataset)
lo_sceicco = URIRef(rrr + "lo_sceicco_bianco_film")
i_vitelloni = URIRef(rrr + "i_vitelloni_film")
la_strada = URIRef(rrr + "la_strada_film")
il_bidone = URIRef(rrr + "il_bidone_film")

# LOAD CSV
df = read_csv("../csv/book_il_primo_fellini.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((book, RDF.type, schema.Book))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Identifier
    if row.get("id"):
        g.add((book, dcterms.identifier, Literal(row["id"])))

    # Title
    if row.get("title"):
        g.add((book, dcterms.title, Literal(row["title"])))

    # Alternative titles
    if row.get("other_title_information"):
        g.add((book, dcterms.alternative, Literal(row["other_title_information"])))

    # Description / notes
    if row.get("responsibility_statement"):
        g.add((book, dcterms.description, Literal(row["responsibility_statement"])))

    if row.get("notes"):
        g.add((book, dcterms.description, Literal(row["notes"])))

    # Author (resource)
    g.add((book, schema.author, fellini))

    # Contributors
    g.add((book, dcterms.contributor, renzi))

    if row.get("other_contributors"):
        g.add((book, dcterms.contributor, Literal(row["other_contributors"])))

    # Publication
    if row.get("publisher"):
        g.add((book, dcterms.publisher, Literal(row["publisher"])))

    if row.get("publication_year"):
        g.add((book, dcterms.issued, Literal(row["publication_year"], datatype=XSD.gYear)))

    # Series
    g.add((book, dcterms.isPartOf, series))

    # Physical extent
    if row.get("extent"):
        g.add((book, dcterms.extent, Literal(row["extent"])))

    # Rights
    if row.get("rights"):
        g.add((book, dcterms.rights, Literal(row["rights"])))

    # Subjects
    g.add((book, dc.subject, fellini))

    if row.get("subjects"):
        g.add((book, dc.subject, Literal(row["subjects"])))

    # Related works (resources, not literals)
    g.add((book, dcterms.relation, lo_sceicco))
    g.add((book, dcterms.relation, i_vitelloni))
    g.add((book, dcterms.relation, la_strada))
    g.add((book, dcterms.relation, il_bidone))

    # Resource type
    if row.get("resource_type"):
        g.add((book, dcterms.type, Literal(row["resource_type"])))

    # Language
    if row.get("language"):
        g.add((book, schema.inLanguage, Literal(row["language"])))

    # Cataloguing standard
    if row.get("standard"):
        g.add((book, dcterms.conformsTo, Literal(row["standard"])))


# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/book_il_primo_fellini.ttl")
print("book_il_primo_fellini.ttl generated successfully!")

