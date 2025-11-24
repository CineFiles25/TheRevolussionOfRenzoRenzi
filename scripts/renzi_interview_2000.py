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

# Load metadata for the interview (single record expected)
with open("../csv/renzi_interview_2000.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    row = next(reader)

# URI representing the interview as a resource in the dataset
interview = NS["rrr"]["renzi_interview_2000"]

# Optional language tag for textual fields
language = (row.get("language") or "").strip()

# Core resource types
g.add((interview, NS["rdf"]["type"], NS["schema"]["Interview"]))
g.add((interview, NS["rdf"]["type"], NS["schema"]["CreativeWork"]))

# Identifier
if row.get("id"):
    g.add((interview, NS["dc"]["identifier"], Literal(row["id"])))

# Descriptive standard or cataloguing rule applied
if row.get("standard"):
    g.add((interview, NS["dcterms"]["conformsTo"], Literal(row["standard"])))

# Title of the interview
if row.get("title"):
    if language:
        g.add((interview, NS["dcterms"]["title"], Literal(row["title"], lang=language)))
    else:
        g.add((interview, NS["dcterms"]["title"], Literal(row["title"])))

# Generic resource type (e.g., sound recording, video, transcript)
if row.get("resource_type"):
    g.add((interview, NS["dcterms"]["type"], Literal(row["resource_type"])))

# Short description or abstract
if row.get("description"):
    if language:
        g.add((interview, NS["dcterms"]["description"], Literal(row["description"], lang=language)))
    else:
        g.add((interview, NS["dcterms"]["description"], Literal(row["description"])))

# Additional notes
if row.get("notes"):
    g.add((interview, NS["dcterms"]["description"], Literal(row["notes"])))

# ============================================
# Agents and roles
# ============================================

# Interviewee as main creator (literal statement)
if row.get("interviewee"):
    g.add((interview, NS["dcterms"]["creator"], Literal(row["interviewee"])))

# Interviewer as contributor (literal statement)
if row.get("interviewer"):
    g.add((interview, NS["dcterms"]["contributor"], Literal(row["interviewer"])))

# ============================================
# Date, duration and format
# ============================================

# Date of the interview
if row.get("date"):
    g.add((interview, NS["dcterms"]["created"], Literal(row["date"])))

# Duration of the interview
if row.get("duration"):
    g.add((interview, NS["schema"]["duration"], Literal(row["duration"])))

# File or carrier format (e.g., audio cassette, digital file)
if row.get("format"):
    g.add((interview, NS["dcterms"]["format"], Literal(row["format"])))

# Rights statement
if row.get("rights"):
    g.add((interview, NS["dcterms"]["rights"], Literal(row["rights"])))

# ============================================
# Spatial, institutional and collection context
# ============================================

# Place of interview as a literal
if row.get("place"):
    g.add((interview, NS["dcterms"]["spatial"], Literal(row["place"])))

# Current holding institution
if row.get("institution"):
    g.add((interview, NS["dcterms"]["publisher"], Literal(row["institution"])))

# Collection name
if row.get("collection"):
    g.add((interview, NS["dcterms"]["isPartOf"], Literal(row["collection"])))

# Current physical location (e.g. archive, depot, shelfmark)
if row.get("current_location"):
    g.add((interview, NS["schema"]["location"], Literal(row["current_location"])))

# ============================================
# External references (URIs)
# ============================================

# Place authority URI
if row.get("place_uri"):
    g.add((interview, NS["dcterms"]["spatial"], URIRef(row["place_uri"])))

# Institution authority URI
if row.get("institution_uri"):
    g.add((interview, NS["dcterms"]["publisher"], URIRef(row["institution_uri"])))

# Collection authority URI
if row.get("collection_uri"):
    g.add((interview, NS["dcterms"]["isPartOf"], URIRef(row["collection_uri"])))

# ============================================
# Language
# ============================================

# Language of the interview content
if language:
    g.add((interview, NS["dc"]["language"], Literal(language)))


# ============================================
# Output
# ============================================

write_graph(g, "../ttl/renzi_interview_2000.ttl")
