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

# Load bibliographic metadata (single record expected)
with open("../csv/book_il_primo_fellini.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    row = next(reader)

# URI representing the book as a digital object in the dataset
book = NS["rrr"]["first_fellini_book"]

# Assign the core resource type
g.add((book, NS["rdf"]["type"], NS["schema"]["Book"]))

# Identifier
if row.get("id"):
    g.add((book, NS["dc"]["identifier"], Literal(row["id"])))

# Standard or cataloging guideline used
if row.get("standard"):
    g.add((book, NS["dcterms"]["conformsTo"], Literal(row["standard"])))

# Main title
if row.get("title_proper"):
    g.add((book, NS["dcterms"]["title"], Literal(row["title_proper"])))

# Additional title information (e.g., subtitles)
if row.get("other_title_information"):
    g.add((book, NS["dcterms"]["alternative"], Literal(row["other_title_information"])))

# Responsibility statement (authors, editors, contributors)
if row.get("responsibility_statement"):
    g.add((book, NS["dcterms"]["creator"], Literal(row["responsibility_statement"])))

# Place of publication
if row.get("publication_place"):
    g.add((book, NS["dcterms"]["spatial"], Literal(row["publication_place"])))

# Publisher name
if row.get("publisher"):
    g.add((book, NS["dcterms"]["publisher"], Literal(row["publisher"])))

# Publication year
if row.get("publication_year"):
    g.add((book, NS["dcterms"]["issued"], Literal(row["publication_year"])))

# Series membership
if row.get("series"):
    g.add((book, NS["dcterms"]["isPartOf"], Literal(row["series"])))

# Physical extent (pages, illustrations, dimensions)
if row.get("extent"):
    g.add((book, NS["dcterms"]["extent"], Literal(row["extent"])))

# General notes or project-specific contextual information
if row.get("notes"):
    g.add((book, NS["dcterms"]["description"], Literal(row["notes"])))


# ============================================
# Related work: film "La Strada" (if provided)
# ============================================

if row.get("related_work"):
    film = NS["rrr"]["film_la_strada_1954"]

    # Assign basic type and title to the related film
    g.add((film, NS["rdf"]["type"], NS["schema"]["Movie"]))
    g.add((film, NS["dc"]["title"], Literal(row["related_work"])))

    # Relationship between the book and the film
    g.add((book, NS["dcterms"]["relation"], film))

    # External URI for authority or reference datasets
    if row.get("related_work_uri"):
        g.add((film, NS["dcterms"]["source"], URIRef(row["related_work_uri"])))


# ============================================
# Output
# ============================================

write_graph(g, "../ttl/book_il_primo_fellini.ttl")
