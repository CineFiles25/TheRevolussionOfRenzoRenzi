# ============================================================================
# IMPORTS
# ============================================================================
# Import pandas for CSV reading and data manipulation
# pandas is the standard library for working with tabular data in Python
import pandas as pd
from pandas import read_csv

# Import RDFLib components for creating RDF graphs and handling semantic web data
# RDFLib is the primary Python library for working with RDF (Resource Description Framework)
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# ============================================================================
# NAMESPACE DEFINITIONS
# ============================================================================
# Namespaces are like vocabularies that define the meaning of terms in RDF
# Each namespace represents a different standard or ontology
# Using multiple namespaces allows us to express concepts precisely and enable data interoperability

# Custom namespace for this project - "The Revolution of Renzo Renzi"
rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/") # This is YOUR namespace where you define your own entities and relationships
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")  
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")  
owl = Namespace("http://www.w3.org/2002/07/owl#")  
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")  
dcterms = Namespace("http://purl.org/dc/terms/")  
dbo = Namespace("http://dbpedia.org/ontology/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
fiaf = Namespace("https://fiaf.github.io/film-related-materials/objects/")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")

# ============================================================================
# ADDITIONAL RECOMMENDED NAMESPACES (currently commented out)
# ============================================================================
# Consider adding these for richer descriptions:

# BIBFRAME - Bibliographic Framework Initiative (Library of Congress)
# Modern replacement for MARC records in libraries
# bf = Namespace("http://id.loc.gov/ontologies/bibframe/")

# EDM - Europeana Data Model
# Used by European cultural heritage aggregator
# edm = Namespace("http://www.europeana.eu/schemas/edm/")

# PROV-O - Provenance Ontology
# For tracking the origin and history of resources
# prov = Namespace("http://www.w3.org/ns/prov#")

# ============================================================================
# GRAPH INITIALIZATION
# ============================================================================
# Create an empty RDF graph - this is the container for all your triples
# A triple is a subject-predicate-object statement (e.g., "Fellini directed La Strada")
g = Graph()

# Create a dictionary to store all namespaces for easy management
# This makes it easier to add/remove namespaces and bind them to the graph
ns_dict = { 
    "rrr": rrr,   
    "rdf": rdf,
    "rdfs": rdfs,
    "owl": owl,
    "schema": schema,
    "dc": dc,
    "dcterms": dcterms,
    "dbo": dbo,
    "crm": crm,
    "foaf": foaf,
    "fiaf": fiaf,
    "skos": skos
}

def graph_bindings():
    """
    Bind all namespace prefixes to the graph.
    
    This makes the output Turtle file more readable by using prefixes 
    instead of full URIs. For example:
    - With binding: schema:Movie
    - Without binding: <https://schema.org/Movie>
    
    Returns:
        Graph: The graph with all namespaces bound
    """
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)  # Bind each prefix to its namespace URI
    return g

# ============================================================================
# ENTITY DEFINITIONS
# ============================================================================
# Create URIRefs for all entities (people, places, organizations, works)
# URIRef creates a unique identifier for each resource in your knowledge graph
# These are the "nodes" in your graph that will be connected by "edges" (predicates)

# The main item you're describing (film, book, photograph, etc.)
# SUGGESTION: Make this dynamic based on what you're cataloging
item = URIRef(rrr + "item")

# Key person: Renzo Renzi (film critic, historian, archivist)
renzo_renzi = URIRef(rrr + "renzo_renzi")

# SUGGESTED ADDITIONAL ENTITIES:
# Add these as needed based on your CSV data:
# federico_fellini = URIRef(rrr + "federico_fellini")
# cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
# renzi_collection = URIRef(rrr + "renzi_collection")
# bologna = URIRef(rrr + "bologna")

# ============================================================================
# AUTHORITY CONTROL - EXTERNAL IDENTIFIERS
# ============================================================================
# Link your entities to external authority files using owl:sameAs
# This is CRUCIAL for:
# 1. Data interoperability - your data can be linked with other datasets
# 2. Disambiguation - clarifies which "Renzo Renzi" you mean
# 3. Authority - provides authoritative identification
# 4. Discovery - enables finding related information across the web

# VIAF (Virtual International Authority File) - aggregates authority records from libraries worldwide
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))

# SUGGESTED ADDITIONAL AUTHORITY LINKS:
# Consider adding links to:
# - Wikidata: Universal identifiers (e.g., "https://www.wikidata.org/wiki/Q...")
# - ISNI: International Standard Name Identifier for creative people
# - ORCID: For researchers and scholars
# - Library of Congress: lccn identifiers
# - Getty vocabularies: For art, architecture, artists
# - IMDb: For film industry

# Example:
# g.add((renzo_renzi, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q...")))
# g.add((renzo_renzi, OWL.sameAs, URIRef("https://isni.org/isni/...")))

# ============================================================================
# CSV DATA IMPORT
# ============================================================================
# Read the CSV file containing your metadata
# keep_default_na=False: Prevents pandas from converting empty strings to NaN
#   This is important because empty strings and NaN are treated differently
# encoding="utf-8": Ensures proper handling of special characters (accents, etc.)
#   Essential for Italian text: è, à, ò, ù, etc.

item_df = pd.read_csv("../csv/item.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

# ============================================================================
# CSV TO RDF TRANSFORMATION
# ============================================================================
# Iterate through each row in the CSV and convert to RDF triples
# iterrows() returns (index, Series) pairs for each row

for idx, row in item_df.iterrows():
    
    # ========================================================================
    # TYPE DECLARATIONS
    # ========================================================================
    # Declare what kind of thing this item is (its rdf:type)
    # Multiple types are allowed and recommended for richer description
    
    g.add((item, RDF.type, fiaf.FilmRelatedMaterial))    
    g.add((item, OWL.sameAs, URIRef(row["ExternalAuthority"])))   
    g.add((item, dcterms.creator, renzo_renzi))
    
    # SUGGESTED ENHANCEMENTS:
    # 1. Handle multiple creators:
    # if row.get("Creators"):
    #     for creator_name in row["Creators"].split(";"):
    #         creator_uri = URIRef(rrr[f"person/{creator_name.strip().lower().replace(' ', '_')}"])
    #         g.add((item, dcterms.creator, creator_uri))
    
    # 2. Distinguish roles:
    # g.add((item, schema.director, federico_fellini))
    # g.add((item, schema.author, renzo_renzi))
    # g.add((item, schema.editor, someone_else))
    
    
    # ========================================================================
    # RELATIONSHIPS TO OTHER RESOURCES
    # ========================================================================
    # SUGGESTED: Link to related works, collections, places
    # g.add((item, dcterms.isPartOf, renzi_collection))
    # g.add((item, schema.about, la_strada_film))
    # g.add((item, schema.locationCreated, bologna))
    # g.add((item, crm.P52_has_current_owner, cineteca_di_bologna))


# ============================================================================
# SERIALIZATION TO TURTLE FORMAT
# ============================================================================
# Save the RDF graph to a .ttl file in Turtle format
# Turtle is a human-readable RDF serialization format
# Other formats available: 'xml' (RDF/XML), 'n3' (Notation3), 'nt' (N-Triples), 'json-ld' (JSON-LD)

g.serialize(format="turtle", destination="../ttl/output_file.ttl")

print("CSV converted to TTL!")