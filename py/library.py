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

library = URIRef(renzi + "renziLibrary")
renzoRenzi = URIRef(renzi + "renzoRenzi")

# g.add((renzoRenzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))

# MAPPING TO ONTOLOGIES 

renziLibrary = pd.read_csv("../csv/library.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for _, row in renziLibrary.iterrows():
    g.add((library, RDF.type, URIRef(schema.Library)))
    g.add((library, dc.identifier, Literal(row["Id ISIL"])))
    g.add((library, schema.name, Literal(row["Name"])))
    g.add((library, schema.alternateName, Literal(row["Alt Title"])))
    g.add((library, schema.additionalType, Literal(row["Original Function"])))
    g.add((library, schema.owner, Literal(row["Owner"])))
    g.add((library, schema.date, Literal(row["Completion Of Work"], datatype=XSD.gYear)))
    g.add((library, schema.foundingDate, Literal(row["Library Foundation"], datatype=XSD.gYear)))
    g.add((library, schema.address, Literal(row["Address"])))
    g.add((library, schema.addressLocality, Literal(row["City"])))
    g.add((library, schema.addressCountry, Literal(row["Country"])))
    g.add((library, schema.geo, Literal(row["Coordinates"])))
    g.add((library, schema.url, Literal(row["Website"], datatype=XSD.anyURI)))
    g.add((library, schema.additionalType, Literal(row["Structure Type"])))
    g.add((library, schema.floorSize, Literal(row["Area"], datatype=XSD.float)))
    g.add((library, schema.seatingCapacity, Literal(row["Seats"], datatype=XSD.integer)))
    g.add((library, dc.description, Literal(row["Audio System"])))
    g.add((library, dc.description, Literal(row["Video System"])))
    g.add((renzoRenzi, schema.honorificPrefix, Literal(row["Named After"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/renziLibrary.ttl") 

print("CSV converted to RDF/XML!")