import pandas as pd
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
skos = Namespace("http://www.w3.org/2004/02/skos/core#")

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
    "fiaf": fiaf,
    "skos": skos
}

def graph_bindings():
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

# ENTITIES 

la_strada_film = URIRef(rrr + "la_strada_film")
federico_fellini = URIRef(rrr + "federico_fellini")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
book_il_primo_fellini = URIRef(rrr + "book_il_primo_fellini")

g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((la_strada_film, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))

# MAPPING TO ONTOLOGIES

lastrada_film = pd.read_csv("csv/la_strada_film.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in lastrada_film.iterrows():
    g.add((la_strada_film, RDF.type, schema.Movie))
    g.add((schema.Movie, RDFS.subClassOf, schema.CreativeWork))
    g.add((la_strada_film, dcterms.isPartOf, book_il_primo_fellini)) #new information
    g.add((book_il_primo_fellini, dcterms.creator, renzo_renzi))  #new information
    g.add((book_il_primo_fellini, RDF.type, schema.Book))  #new information
    g.add((schema.Book, RDFS.subClassOf, schema.CreativeWork))  #new information
    g.add((la_strada_film, dcterms.title, Literal(row["title"])))
    g.add((la_strada_film, dcterms.alternative, Literal(row["other_title_information"])))
    g.add((la_strada_film, dcterms.creator, federico_fellini))
    g.add((la_strada_film, schema.director, federico_fellini))
    g.add((la_strada_film, dcterms.publisher, Literal(row["production_company"])))
    g.add((la_strada_film, dcterms.spatial, Literal(row["country"])))
    g.add((la_strada_film, dcterms.language, Literal(row["language"])))
    g.add((la_strada_film, dcterms.issued, Literal(row["publication_year"], datatype=XSD.gYear)))
    g.add((la_strada_film, dcterms.extent, Literal(row["length"])))
    g.add((la_strada_film, schema.duration, Literal(row["duration"])))
    g.add((la_strada_film, dcterms["format"], Literal(row["format"])))
    g.add((la_strada_film, schema.color, Literal(row["colour"])))
    g.add((la_strada_film, schema.sound, Literal(row["sound"])))
    g.add((la_strada_film, dcterms.type, Literal(row["resource_type"])))
    g.add((la_strada_film, dcterms.description, Literal(row["notes"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="ttl/la_strada_film.ttl")

print("CSV converted to TTL!")
