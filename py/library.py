from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# NAMESPACES

renzi = Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage")
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

# GRAPH BINDINGS 

g = Graph()

nsDict = { 
    "renzi": renzi,
    "schema": schema,
    "dc": dc,
    "dcterms": dcterms,
    "crm": crm
} # dict makes it easier to manage multiple namespaces and modify them

def graph_bindings():
    for prefix, ns in nsDict.items(): # items to iterate over key-value pairs
        g.bind(prefix, ns)
    return g

# ENTITIES 

renzoRenzi = URIRef(renzi + "renzoRenzi")
g.add((renzoRenzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))


# DATA INGESTION

library = URIRef(renzi + "renziLibrary")
renziLibrary = read_csv("library.csv", keep_default_na=False, encoding="utf-8")

for _, row in renziLibrary.iterrows():
    g.add((library, dc.identifier, Literal(row["Id ISIL"], datatype=XSD.string)))
    g.add((library, schema.name, Literal(row["Name"], datatype=XSD.string)))
    g.add((library, schema.alternateName, Literal(row["Alt Title"], datatype=XSD.string)))
    g.add((library, RDF.type, URIRef()))
    g.add((library, schema.additionalType, Literal(row["Original Function"], datatype=XSD.string)))
    g.add((library, schema.owner, Literal(row["Owner"], datatype=XSD.string)))
    g.add((library, schema.date, Literal(row["Completion Of Work"], datatype=XSD.gYear)))
    g.add((library, schema.foundingDate, Literal(row["Library Founded"], datatype=XSD.gYear)))
    g.add((library, schema.address, Literal(row["Address"], datatype=XSD.string)))
    g.add((library, schema.addressLocality, Literal(row["City"], datatype=XSD.string)))
    g.add((library, schema.addressCountry, Literal(row["Country"], datatype=XSD.string)))
    g.add((library, schema.geo, Literal(row["Coordinates"], datatype=XSD.string)))
    g.add((library, schema.url, Literal(row["Website"], datatype=XSD.anyURI)))
    g.add((library, schema.additionalType, Literal(row["Structure Type"], datatype=XSD.string)))
    g.add((library, schema.floorSize, Literal(row["Area"], datatype=XSD.float)))
    g.add((library, dc.description, Literal(row["Seats"], datatype=XSD.integer)))
    g.add((library, dc.description, Literal(row["Audio System"], datatype=XSD.string)))
    g.add((library, dc.description, Literal(row["Video System"], datatype=XSD.string)))
    g.add((library, schema.honorificPrefix, Literal(row["Named After"], datatype=XSD.string))) # da modificare forse 
    
# SERIALIZATION

g.serialize(format="turtle", destination="renziLibrary.ttl") 
# for serializing the graph into a turtle file bc graphs are objects that get lost if not stored