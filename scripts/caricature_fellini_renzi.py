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

# Load object metadata (single caricature expected)
with open("../csv/caricature_fellini_renzi.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    row = next(reader)

# URI representing the caricature as a digital object in the dataset
caricature = NS["rrr"]["caricature_fellini_renzi"]

# Assign the core resource type
g.add((caricature, NS["rdf"]["type"], NS["schema"]["VisualArtwork"]))

# Identifier
if row.get("id"):
    g.add((caricature, NS["dc"]["identifier"], Literal(row["id"])))

# Standard or cataloging guideline used
if row.get("standard"):
    g.add((caricature, NS["dcterms"]["conformsTo"], Literal(row["standard"])))

# Main title of the caricature
if row.get("title"):
    g.add((caricature, NS["dcterms"]["title"], Literal(row["title"])))

# Object type (e.g. caricature, drawing, print)
if row.get("object_type"):
    g.add((caricature, NS["dcterms"]["type"], Literal(row["object_type"])))

# Inscription or textual content associated with the object
if row.get("inscription"):
    # If a language column is available, it can be used to tag the literal
    language = (row.get("language") or "").strip()
    if language:
        g.add((caricature, NS["dcterms"]["description"], Literal(row["inscription"], lang=language)))
    else:
        g.add((caricature, NS["dcterms"]["description"], Literal(row["inscription"])))

# Creator information as a simple literal statement
if row.get("creator"):
    g.add((caricature, NS["dcterms"]["creator"], Literal(row["creator"])))

# Creation date of the caricature
if row.get("creation_date"):
    g.add((caricature, NS["dcterms"]["created"], Literal(row["creation_date"])))

# Technique or medium used (e.g. ink, pencil, mixed media)
if row.get("technique"):
    g.add((caricature, NS["dcterms"]["medium"], Literal(row["technique"])))

# Optional notes providing additional context
if row.get("notes"):
    g.add((caricature, NS["dcterms"]["description"], Literal(row["notes"])))


# ============================================
# Output
# ============================================

write_graph(g, "../ttl/caricature_fellini_renzi.ttl")
