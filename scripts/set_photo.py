import pandas as pd
from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage/")
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

ns_dict = { 
    "renzi": rrr,
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
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

# ENTITIES

set_photo = URIRef(rrr + "ferrari_photograph")
renzo_renzi = URIRef(rrr + "renzo_renzi")
aldo_ferrari = URIRef(rrr + "aldo_ferrari")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))

# MAPPING CSV

ferrari_photograph = pd.read_csv("../csv/ferrari_set_photo.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for _, row in ferrari_photograph.iterrows():
    g.add((set_photo, RDF.type, URIRef(schema + "Photograph")))
    g.add((set_photo, RDFS.subClassOf, URIRef(schema + "CreativeWork")))
    g.add((set_photo, dc.title, Literal(row["Title"])))
    g.add((set_photo, dc.creator, aldo_ferrari))    
    g.add((set_photo, schema.dateCreated, Literal(row["Date Taken"], datatype=XSD.gYear)))
    g.add((set_photo, schema.about, renzo_renzi))    
    g.add((set_photo, schema.locationCreated, Literal(row["Location"])))
    g.add((set_photo, schema.owner, cineteca_di_bologna))
    g.add((set_photo, dcterms.isPartOf, Literal(row["Collection"])))    
    g.add((set_photo, schema.url, Literal(row["Url"], datatype=XSD.anyURI)))
    g.add((set_photo, schema.material, Literal(row["Form"])))
    g.add((set_photo, schema.artform, Literal(row["Technique"]))) 
    g.add((set_photo, schema.width, Literal(row["Dimensions"], datatype=XSD.integer)))
    g.add((set_photo, schema.contentSize, Literal(row["File Size"])))
    g.add((set_photo, schema.fileFormat, Literal(row["Format"])))
    g.add((set_photo, schema.license, Literal(row["Type Of License"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/set_photo.ttl")

print("CSV converted to TTL!")

