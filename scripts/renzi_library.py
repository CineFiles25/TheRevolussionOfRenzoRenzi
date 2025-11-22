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

renzi_library = URIRef(rrr + "renzo_renzi_library")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))

# MAPPING TO ONTOLOGIES 

renzo_renzi_library = pd.read_csv("../csv/renzi_library.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in renzo_renzi_library.iterrows():
    g.add((renzi_library, RDF.type, URIRef(schema + "Library")))
    g.add((renzi_library, RDFS.subClassOf, URIRef(schema + "CivicStructure")))
    g.add((renzi_library, OWL.sameAs, URIRef("https://isni.org/isni/0000000459141457")))
    g.add((renzi_library, dc.identifier, Literal(row["Id ISIL"])))
    g.add((renzi_library, schema.name, Literal(row["Name"])))
    g.add((renzi_library, schema.alternateName, Literal(row["Alt Title"])))
    g.add((renzi_library, schema.additionalType, Literal(row["Original Function"])))
    g.add((renzi_library, crm.P52_has_current_owner,cineteca_di_bologna))
    g.add((renzi_library, schema.date, Literal(row["Completion Of Work"], datatype=XSD.gYear)))
    g.add((renzi_library, schema.foundingDate, Literal(row["Library Foundation"], datatype=XSD.gYear)))
    g.add((renzi_library, schema.address, Literal(row["Address"])))
    g.add((renzi_library, schema.addressLocality, bologna))
    g.add((renzi_library, schema.addressCountry, Literal(row["Country"])))
    g.add((renzi_library, schema.geo, Literal(row["Coordinates"])))
    g.add((renzi_library, schema.url, Literal(row["Website"], datatype=XSD.anyURI)))
    g.add((renzi_library, schema.additionalType, Literal(row["Structure Type"])))
    g.add((renzi_library, schema.floorSize, Literal(row["Area"], datatype=XSD.float)))
    g.add((renzi_library, schema.seatingCapacity, Literal(row["Seats"], datatype=XSD.integer)))
    g.add((renzi_library, dc.description, Literal(row["Audio System"])))
    g.add((renzi_library, dc.description, Literal(row["Video System"])))
    g.add((renzi_library, dbo.dedicatedTo, renzo_renzi))

# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/renzi_library.ttl") 

print("CSV converted to TTL!")
