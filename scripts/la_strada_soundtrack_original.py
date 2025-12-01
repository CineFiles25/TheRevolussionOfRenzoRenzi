# ============================================
# Base configuration
# ============================================

import csv
from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
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

# GRAPH CREATION

g = Graph()

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
    "fiaf": fiaf
}

def graph_bindings():
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

# ENTITIES 

soundtrack = URIRef(rrr + "la_strada_soundtrack_original")
film_la_strada = URIRef(rrr + "la_strada_film")
nino_rota = URIRef(rrr + "nino_rota")
federico_fellini = URIRef(rrr + "federico_fellini")

g.add((nino_rota, OWL.sameAs, URIRef("http://viaf.org/viaf/88980189")))
g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((film_la_strada, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))

# MAPPING TO ONTOLOGIES

la_strada_soundtrack = read_csv("../csv/la_strada_soundtrack_original.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in la_strada_soundtrack.iterrows():
    g.add((soundtrack, RDF.type, URIRef(schema + "MusicRecording")))
    g.add((soundtrack, RDFS.subClassOf, URIRef(schema + "CreativeWork")))
    g.add((soundtrack, dc.title, Literal(row["Title"])))
    g.add((soundtrack, schema.alternateName, Literal(row["Alt Title"])))
    g.add((soundtrack, dcterms.creator, nino_rota))
    g.add((soundtrack, schema.composer, nino_rota))
    g.add((soundtrack, schema.byArtist, nino_rota))
    g.add((soundtrack, schema.additionalType, Literal(row["Soundtrack Type"])))
    g.add((soundtrack, dcterms.relation, film_la_strada))
    g.add((soundtrack, schema.about, film_la_strada))
    g.add((soundtrack, schema.datePublished, Literal(row["Release Year"], datatype=XSD.gYear)))    
    g.add((soundtrack, dcterms.publisher, Literal(row["Publisher"])))
    g.add((soundtrack, schema.countryOfOrigin, Literal(row["Country"])))
    g.add((soundtrack, schema.locationCreated, Literal(row["Recording Location"])))
    g.add((soundtrack, schema.contentLocation, Literal(row["Current Location"])))
    g.add((soundtrack, schema.inLanguage, Literal(row["Language"])))
    g.add((soundtrack, dcterms.conformsTo, Literal(row["Standard"])))
    g.add((soundtrack, dc.identifier, Literal(row["ID"])))
    g.add((soundtrack, dcterms.description, Literal(row["Notes"])))

# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/la_strada_soundtrack_original.ttl")

print("CSV converted to TTL!")


