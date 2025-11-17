import pandas as pd
from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# NAMESPACES

renzi = Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
fiaf = Namespace("https://fiaf.github.io/film-related-materials/objects/")

# GRAPH CREATION

g = Graph()

nsDict = { 
    "renzi": renzi,   
    "rdf": rdf,
    "rdfs": rdfs,
    "owl": owl,
    "schema": schema,
    "dc": dc,
    "dcterms": dcterms,
    "crm": crm,
    "foaf": foaf,
    "fiaf": fiaf
}

def graph_bindings():
    for prefix, ns in nsDict.items():
        g.bind(prefix, ns)
    return g

# ENTITIES

documentary = URIRef(renzi + "quandoIlPoèDolce")
renzoRenzi = URIRef(renzi + "renzoRenzi") 

# g.add((renzoRenzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))

# MAPPING TO ONTOLOGIES

quandoIlPoèDolce = pd.read_csv("../csv/documentary.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for _, row in quandoIlPoèDolce.iterrows():
    g.add((documentary, RDF.type, URIRef(schema + "Movie")))
    g.add((documentary, dc.title, Literal(row["Title"])))
    g.add((documentary, schema.alternateName, Literal(row["Alt Title"])))
    g.add((documentary, schema.director, Literal(row["Director"])))
    g.add((documentary, schema.author, Literal(row["Screenwriter"])))
    g.add((documentary, schema.edition, Literal(row["Edition"])))
    g.add((documentary, schema.genre, Literal(row["Type"])))
    g.add((documentary, schema.countryOfOrigin, Literal(row["Country"])))    
    g.add((documentary, schema.productionCompany, Literal(row["Production Company"])))    
    g.add((documentary, schema.datePublished, Literal(row["Year"], datatype=XSD.gYear)))
    g.add((documentary, schema.duration, Literal(row["Running Time"])))
    g.add((documentary, schema.color, Literal(row["Color"])))
    g.add((documentary, schema.encodingFormat, Literal(row["Film Type"])))
    g.add((documentary, schema.frameRate, Literal(row["Frame Rate"])))
    g.add((documentary, schema.contentSize, Literal(row["Film Length"])))    
    g.add((documentary, schema.sound, Literal(row["Sound"])))
    g.add((documentary, schema.inLanguage, Literal(row["Language"])))
    g.add((documentary, schema.about, Literal(row["Subject"])))
    g.add((documentary, schema.spatialCoverage, Literal(row["Filming Location"])))
    g.add((documentary, schema.musicBy, Literal(row["Music Composer"])))
    g.add((documentary, schema.contentRating, Literal(row["Certificate"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/documentary.ttl")

print("CSV converted and serialized to ../ttl/documentary.ttl")