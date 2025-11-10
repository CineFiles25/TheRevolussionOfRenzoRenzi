from pandas import read_csv
from rdflib import Namespace, RDF, OWL, Literal, XSD, RDFS, URIRef, Graph, FOAF

renzi = Namespace()
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

g = Graph()

g.bind("renzi", renzi)
g.bind("schema", schema)
g.bind("dc", dc)
g.bind("dcterms", dcterms)
g.bind("crm", crm)

# RenzoRenzi = URIRef(renzi + "RenzoRenzi")

# g.add((RenzoRenzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))

library = URIRef(renzi + "RenziLibrary")

RenziLibrary = read_csv(".../csv_files/library.csv"keep_default_na=False, encoding="utf-8")

for _, row in RenziLibrary.iterrows():
    g.add((library, RDF.type, URIRef()))
    g.add((library,))
# g.serialize(format="turtle", destination="DianaHerTrueStory.ttl") 
# -> for serializing the graph into a turtle file bc graphs are objects that get lost if not stored
