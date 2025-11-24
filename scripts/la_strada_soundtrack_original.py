# ============================================
# Base configuration
# ============================================

import csv
from rdflib import Graph, Namespace, URIRef, Literal

# Centralized namespace collection
NS = {
    "rrr": Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/"),
    "schema": Namespace("https://schema.org/"),
    "dc": Namespace("http://purl.org/dc/elements/1.1/"),
    "dcterms": Namespace("http://purl.org/dc/terms/"),
    "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
}


def init_graph():
    """
    Initialize an RDF graph and bind all predefined namespaces.
    """
    g = Graph()
    for prefix, ns in NS.items():
        g.bind(prefix, ns)
    return g


def write_graph(graph, output_path):
    """
    Serialize and export the RDF graph in Turtle format.
    """
    graph.serialize(destination=output_path, format="turtle")


# ============================================
# Data processing and RDF generation
# ============================================

# Initialize the graph
g = init_graph()

# Load metadata for the original soundtrack (single record expected)
with open("../csv/la_strada_soundtrack_original.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    row = next(reader)

# URI representing the soundtrack as a resource in the dataset
soundtrack = NS["rrr"]["la_strada_soundtrack_original"]

# Optional language tag for textual fields
language = (row.get("language") or "").strip()

# Core resource types
g.add((soundtrack, NS["rdf"]["type"], NS["schema"]["MusicRecording"]))
g.add((soundtrack, NS["rdf"]["type"], NS["schema"]["CreativeWork"]))

# Identifier
if row.get("id"):
    g.add((soundtrack, NS["dc"]["identifier"], Literal(row["id"])))

# Descriptive standard or cataloguing rule applied
if row.get("standard"):
    g.add((soundtrack, NS["dcterms"]["conformsTo"], Literal(row["standard"])))

# Title of the soundtrack
if row.get("title"):
    if language:
        g.add((soundtrack, NS["dc"]["title"], Literal(row["title"], lang=language)))
    else:
        g.add((soundtrack, NS["dc"]["title"], Literal(row["title"])))

# Composer information as a literal
if row.get("composer"):
    g.add((soundtrack, NS["dcterms"]["creator"], Literal(row["composer"])))

# ============================================
# Relationship with the film "La Strada"
# ============================================

# Link to the related film, if specified
if row.get("related_work"):
    film = NS["rrr"]["film_la_strada_1954"]

    # Basic typing and title for the related film
    g.add((film, NS["rdf"]["type"], NS["schema"]["Movie"]))
    g.add((film, NS["dc"]["title"], Literal(row["related_work"])))

    # Relation between soundtrack and film
    g.add((soundtrack, NS["dcterms"]["relation"], film))

    # Optional external URI for the film (e.g. authority record or catalog entry)
    if row.get("related_work_uri"):
        g.add((film, NS["dcterms"]["source"], URIRef(row["related_work_uri"])))

# Optional literal describing the nature of the relationship
if row.get("work_relation_type"):
    g.add((soundtrack, NS["dcterms"]["relation"], Literal(row["work_relation_type"])))

# ============================================
# Publication and production details
# ============================================

# Release year
if row.get("release_year"):
    g.add((soundtrack, NS["dcterms"]["issued"], Literal(str(row["release_year"]))))

# Soundtrack type (e.g. original soundtrack, reissue, compilation)
if row.get("soundtrack_type"):
    g.add((soundtrack, NS["schema"]["additionalType"], Literal(row["soundtrack_type"])))

# Publisher or record label as a simple literal
if row.get("publisher"):
    g.add((soundtrack, NS["dcterms"]["publisher"], Literal(row["publisher"])))

# Country of publication or production
if row.get("country"):
    g.add((soundtrack, NS["dcterms"]["spatial"], Literal(row["country"])))

# ============================================
# Location and contextual information
# ============================================

# Recording location (studio, city, etc.)
if row.get("recording_location"):
    g.add((soundtrack, NS["schema"]["locationCreated"], Literal(row["recording_location"])))

# Current location (institution or archive)
if row.get("current_location"):
    g.add((soundtrack, NS["schema"]["location"], Literal(row["current_location"])))

# Language of the work
if language:
    g.add((soundtrack, NS["dc"]["language"], Literal(language)))

# Additional notes or free-text description (if a column is available)
if row.get("notes"):
    g.add((soundtrack, NS["dcterms"]["description"], Literal(row["notes"])))


# ============================================
# Output
# ============================================

write_graph(g, "../ttl/la_strada_soundtrack_original.ttl")
