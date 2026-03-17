from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

# GRAPH
g = Graph()

# Bindings
g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)
g.bind("dc", dc)

# ENTITIES
soundtrack = URIRef(rrr + "la_strada_soundtrack_original")
film = URIRef(rrr + "la_strada_film")
nino_rota = URIRef(rrr + "nino_rota")

# LOAD CSV
df = read_csv("../csv/la_strada_soundtrack_original.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((soundtrack, RDF.type, schema.MusicRecording))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Identifiers
    if row.get("id"):
        g.add((soundtrack, dcterms.identifier, Literal(row["id"])))

    if row.get("identifiers"):
        g.add((soundtrack, dcterms.identifier, Literal(row["identifiers"])))

    if row.get("catalogue_number"):
        g.add((soundtrack, dcterms.identifier, Literal(row["catalogue_number"])))

    # Standard
    if row.get("standard"):
        g.add((soundtrack, dcterms.conformsTo, Literal(row["standard"])))

    # Titles
    if row.get("title"):
        g.add((soundtrack, dcterms.title, Literal(row["title"])))

    if row.get("other_title_information"):
        g.add((soundtrack, schema.alternateName, Literal(row["other_title_information"])))

    # Description
    if row.get("responsibility_statement"):
        g.add((soundtrack, dcterms.description, Literal(row["responsibility_statement"])))

    if row.get("notes"):
        g.add((soundtrack, dcterms.description, Literal(row["notes"])))

    # Composer (resource)
    g.add((soundtrack, schema.composer, nino_rota))

    # Performers (literal)
    if row.get("performers"):
        g.add((soundtrack, dcterms.contributor, Literal(row["performers"])))

    # Publication place
    if row.get("publication_place"):
        g.add((soundtrack, schema.location, Literal(row["publication_place"])))

    # Publisher / label
    if row.get("publisher"):
        g.add((soundtrack, dcterms.publisher, Literal(row["publisher"])))

    if row.get("label"):
        g.add((soundtrack, schema.publisher, Literal(row["label"])))

    # Publication year (kept as string)
    if row.get("publication_year"):
        g.add((soundtrack, dcterms.issued, Literal(row["publication_year"])))

    # Carrier type / physical description
    if row.get("carrier_type"):
        g.add((soundtrack, dcterms.medium, Literal(row["carrier_type"])))

    if row.get("physical_description"):
        g.add((soundtrack, dcterms.extent, Literal(row["physical_description"])))

    # Subjects
    if row.get("subjects"):
        g.add((soundtrack, dc.subject, Literal(row["subjects"])))

    # Link to La Strada
    g.add((soundtrack, schema.about, film))

    # Related works (resources)
    if row.get("related_works"):
        for work_id in [w.strip() for w in row["related_works"].split(";") if w.strip()]:
            g.add((soundtrack, dcterms.relation, URIRef(rrr + work_id)))

    # Rights
    if row.get("rights"):
        g.add((soundtrack, dcterms.rights, Literal(row["rights"])))

    # Resource type
    if row.get("resource_type"):
        g.add((soundtrack, dcterms.type, Literal(row["resource_type"])))

    # Language
    if row.get("language"):
        g.add((soundtrack, schema.inLanguage, Literal(row["language"])))


# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/la_strada_soundtrack_original.ttl")
print("la_strada_soundtrack_original.ttl generated successfully!")

