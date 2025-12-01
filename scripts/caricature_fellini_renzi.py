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

caricature_fellini_renzi = URIRef(rrr + "caricature_fellini_renzi")
federico_fellini = URIRef(rrr + "federico_fellini")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")

g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# MAPPING TO ONTOLOGIES

caricature_df = read_csv("../csv/caricature_fellini_renzi.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in caricature_df.iterrows():
    g.add((caricature_fellini_renzi, RDF.type, schema.VisualArtwork))
    g.add((schema.VisualArtwork, RDFS.subClassOf, schema.CreativeWork))
    g.add((caricature_fellini_renzi, dcterms.conformsTo, Literal(row["standard"])))
    g.add((caricature_fellini_renzi, dcterms.title, Literal(row["title"])))
    g.add((caricature_fellini_renzi, dcterms.type, Literal(row["object_type"])))
    g.add((caricature_fellini_renzi, dcterms.description, Literal(row["inscription"], lang="it")))
    g.add((caricature_fellini_renzi, dcterms.creator, renzo_renzi))
    g.add((caricature_fellini_renzi, schema.about, federico_fellini))
    g.add((caricature_fellini_renzi, dcterms.created, Literal(row["creation_date"])))
    g.add((caricature_fellini_renzi, dcterms.medium, Literal(row["technique"])))
    g.add((caricature_fellini_renzi, dcterms.material, Literal(row["material"])))
    g.add((caricature_fellini_renzi, dcterms.format, Literal(row["dimensions"])))
    g.add((caricature_fellini_renzi, dcterms.description, Literal(row["notes"])))
    g.add((caricature_fellini_renzi, schema.owner, cineteca_di_bologna))
    g.add((renzi_collection, dcterms.hasPart, caricature_fellini_renzi))
    g.add((caricature_fellini_renzi, dcterms.location, renzi_library))    
    g.add((renzi_library, schema.location, cineteca_di_bologna))
    g.add((caricature_fellini_renzi, dcterms.description, Literal(row["description"])))
    g.add((caricature_fellini_renzi, schema.language, Literal(row["language"])))
    

# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/caricature_fellini_renzi.ttl")

print("CSV converted to TTL!")
