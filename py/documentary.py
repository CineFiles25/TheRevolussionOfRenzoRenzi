import pandas as pd
from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# NAMESPACES

renzi = Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage")
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")

# GRAPH CREATION

g = Graph()

nsDict = { 
    "renzi": renzi,
    "schema": schema,
    "dc": dc,
    "dcterms": dcterms,
    "crm": crm,
    "foaf": foaf
}

def graph_bindings():
    for prefix, ns in nsDict.items():
        g.bind(prefix, ns)
    return g

# ENTITIES

quandoIlPoèDolce = URIRef(renzi + "quandoIlPoèDolce")
renzoRenzi = URIRef(renzi + "renzoRenzi")

# g.add((renzoRenzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))

# MAPPING TO ONTOLOGIES

quandoIlPoèDolce = pd.read_csv("../csv/documentary.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for _, row in quandoIlPoèDolce.iterrows():
    g.add((quandoIlPoèDolce, RDF.type, URIRef(schema.Movie)))
    g.add((quandoIlPoèDolce, dc.title, Literal(row["Title"])))
    g.add((quandoIlPoèDolce, schema.alternateName, Literal(row["Alt Title"])))
    g.add((quandoIlPoèDolce, schema.director, Literal(row["Director"])))
    g.add((quandoIlPoèDolce, schema.author, Literal(row["Screenwriter"])))
    g.add((quandoIlPoèDolce, schema.edition, Literal(row["Edition"])))
    g.add((quandoIlPoèDolce, schema.genre, Literal(row["Type"])))
    g.add((quandoIlPoèDolce, schema.countryOfOrigin, Literal(row["Country"])))    
    g.add((quandoIlPoèDolce, schema.productionCompany, Literal(row["Production Company"])))    
    g.add((quandoIlPoèDolce, schema.datePublished, Literal(row["Year"], datatype=XSD.gYear)))
    g.add((quandoIlPoèDolce, schema.duration, Literal(row["Running Time"])))
    g.add((quandoIlPoèDolce, schema.color, Literal(row["Color"])))
    g.add((quandoIlPoèDolce, schema.encodingFormat, Literal(row["Film Type"])))
    g.add((quandoIlPoèDolce, schema.frameRate, Literal(row["Frame Rate"])))
    g.add((quandoIlPoèDolce, schema.contentSize, Literal(row["Film Length"])))    
    g.add((quandoIlPoèDolce, schema.sound, Literal(row["Sound"])))
    g.add((quandoIlPoèDolce, schema.inLanguage, Literal(row["Language"])))
    g.add((quandoIlPoèDolce, schema.about, Literal(row["Subject"])))
    g.add((quandoIlPoèDolce, schema.spatialCoverage, Literal(row["Filming Location"])))
    g.add((quandoIlPoèDolce, schema.musicBy, Literal(row["Music Composer"])))
    g.add((quandoIlPoèDolce, schema.contentRating, Literal(row["Certificate"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/quandoIlPoèDolce.ttl")

print("CSV converted to RDF/XML!")