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

# Load metadata for the photograph (single record expected)
with open("../csv/photo_lastrada_01.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    row = next(reader)

# URI representing the photo as a resource in the dataset
photo = NS["rrr"]["photo_lastrada_01"]

# Optional language tag for inscriptions or textual elements
language = (row.get("language") or "").strip()

# Resource type for still images
g.add((photo, NS["rdf"]["type"], NS["schema"]["ImageObject"]))

# Identifier
if row.get("id"):
    g.add((photo, NS["dc"]["identifier"], Literal(row["id"])))

# Descriptive standard or cataloguing guideline used
if row.get("standard"):
    g.add((photo, NS["dcterms"]["conformsTo"], Literal(row["standard"])))

# Title of the photograph
if row.get("title"):
    if language:
        g.add((photo, NS["dcterms"]["title"], Literal(row["title"], lang=language)))
    else:
        g.add((photo, NS["dcterms"]["title"], Literal(row["title"])))

# Object type (e.g., photograph, still image)
if row.get("object_type"):
    g.add((photo, NS["dcterms"]["type"], Literal(row["object_type"])))

# Inscription or caption
if row.get("inscription"):
    if language:
        g.add((photo, NS["dcterms"]["description"], Literal(row["inscription"], lang=language)))
    else:
        g.add((photo, NS["dcterms"]["description"], Literal(row["inscription"])))

# Photographer or creator (literal)
if row.get("creator"):
    g.add((photo, NS["dcterms"]["creator"], Literal(row["creator"])))

# Creation date of the photograph
if row.get("creation_date"):
    g.add((photo, NS["dcterms"]["created"], Literal(row["creation_date"])))

# Technique or photographic process
if row.get("technique"):
    g.add((photo, NS["dcterms"]["medium"], Literal(row["technique"])))

# Additional notes providing context
if row.get("notes"):
    g.add((photo, NS["dcterms"]["description"], Literal(row["notes"])))


# ============================================
# Relationship with the film "La Strada"
# ============================================

# If the photograph is related to the film, create a simple connection
if row.get("related_work"):
    film = NS["rrr"]["film_la_strada_1954"]

    # Basic typing and title of the related film
    g.add((film, NS["rdf"]["type"], NS["schema"]["Movie"]))
    g.add((film, NS["dc"]["title"], Literal(row["related_work"])))

    # Connecting the photo with the film
    g.add((photo, NS["dcterms"]["relation"], film))

    # Optional external URI (e.g., authority dataset)
    if row.get("related_work_uri"):
        g.add((film, NS["dcterms"]["source"], URIRef(row["related_work_uri"])))


# ============================================
# Output
# ============================================

write_graph(g, "../ttl/photo_lastrada_01.ttl")
