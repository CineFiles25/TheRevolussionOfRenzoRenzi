import csv
from rdflib import Graph, Namespace, URIRef, Literal, RDF, XSD, OWL

nsDict = {
    "renzi" = Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage")    
    "owl": Namespace("http://www.w3.org/2002/07/owl#")    
    "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#")
    "schema" = Namespace("https://schema.org/")
    "dc" = Namespace("http://purl.org/dc/elements/1.1/")
    "dcterms" = Namespace("http://purl.org/dc/terms/")
    "crm" = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
    "foaf" = Namespace("http://xmlns.com/foaf/0.1/")
    # "edm": Namespace("http://www.europeana.eu/schemas/edm/")
    # "skos": Namespace("http://www.w3.org/2004/02/skos/core#")
    # "wd": Namespace("https://www.wikidata.org/wiki/")
}

def init_graph():
    g = Graph()
    for prefix, ns in nsDict.items():
        g.bind(prefix, ns)
    return g

def serialize_graph(graph, output_path):
    graph.serialize(destination=output_path, format="turtle")