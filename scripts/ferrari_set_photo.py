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

ferrari_set_photo = URIRef(rrr + "ferrari_set_photo")
renzo_renzi = URIRef(rrr + "renzo_renzi")
aldo_ferrari = URIRef(rrr + "aldo_ferrari")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((aldo_ferrari, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q3609208")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))

# MAPPING 

ferrari_set_photo = pd.read_csv("../csv/ferrari_set_photo.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in ferrari_set_photo.iterrows():
    g.add((ferrari_set_photo, RDF.type, schema.Photograph))
    g.add((schema.Photograph, RDFS.subClassOf, schema.CreativeWork))
    g.add((ferrari_set_photo, dc.title, Literal(row["title"])))
    g.add((ferrari_set_photo, dcterms.creator, aldo_ferrari))
    g.add((ferrari_set_photo, schema.locationCreated, Literal(row["depicted_event"])))    
    g.add((ferrari_set_photo, foaf.depicts, renzo_renzi)) 
    g.add((cineteca_di_bologna, schema.location, bologna))
    g.add((ferrari_set_photo, schema.dateCreated, Literal(row["creation_year"], datatype=XSD.gYear)))
    g.add((ferrari_set_photo, schema.color, Literal(row["colour"], datatype=XSD.string)))
    g.add((ferrari_set_photo, schema.material, Literal(row["material_technique"])))
    g.add((ferrari_set_photo, schema.identifier, Literal(row["inventory_number"])))
    g.add((ferrari_set_photo, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((ferrari_set_photo, dcterms.isPartOf, Literal(row["collection"])))    
    g.add((ferrari_set_photo, schema.identifier, Literal(row["identifiers"], datatype=XSD.anyURI)))
    g.add((ferrari_set_photo, schema., Literal(row["carrier_type"])))
    g.add((ferrari_set_photo, schema.artform, Literal(row["physical_description"]))) 
    g.add((ferrari_set_photo, schema.description, Literal(row["notes"], datatype=XSD.string)))
    g.add((ferrari_set_photo, schema.width, Literal(row["dimensions"], datatype=XSD.integer)))
    g.add((ferrari_set_photo, schema.fileFormat, Literal(row["format"])))
    g.add((ferrari_set_photo, schema.license, Literal(row["rights"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/ferrari_set_photo.ttl")

print("CSV converted to TTL!")

