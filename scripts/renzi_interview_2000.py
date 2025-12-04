from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

from scripts import renzi_library

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

renzi_interview = URIRef(rrr + "renzi_interview_2000")
renzo_renzi = URIRef(rrr + "renzo_renzi")
bologna = URIRef(rrr + "bologna")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzi_library")

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# MAPPING TO ONTOLOGIES

renzi_interview_2000 = read_csv("../csv/renzi_interview_2000.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in renzi_interview_2000.iterrows():
    g.add((renzi_interview, RDF.type, schema.Interview))
    g.add((schema.Interview, RDFS.subClassOf, schema.CreativeWork))
    g.add((renzi_interview, dc.identifier, Literal(row["id"])))
    g.add((renzi_interview, dcterms.conformsTo, Literal(row["standard"])))
    g.add((renzi_interview, dcterms.title, Literal(row["title"])))
    g.add((renzi_interview, dc.title, Literal(row["other_title_information"])))
    g.add((renzi_interview, dcterms.type, Literal(row["resource_type"])))
    g.add((renzi_interview, foaf.depicts, renzo_renzi))
    g.add((renzi_interview, dcterms.contributor, Literal(row["interviewer"])))
    g.add((renzi_interview, schema.publisher, cineteca_di_bologna))
    g.add((renzi_interview, schema.location, bologna))
    g.add((renzi_interview, dcterms.created, Literal(row["production_year"], datatype=XSD.gYear)))
    g.add((renzi_interview, schema.duration, Literal(row["duration"])))
    g.add((renzi_interview, schema.color, Literal(row["colour"])))
    g.add((renzi_interview, schema.sound, Literal(row["sound"])))
    g.add((renzi_interview, dcterms.format, Literal(row["format"])))
    g.add((renzi_interview, dcterms.isPartOf, renzi_collection))
    g.add((renzi_interview, schema.location, renzi_library))
    g.add((renzi_interview, dcterms.rights, URIRef(row["rights"])))
    g.add((renzi_interview, dc.language, Literal(row["language"])))
    g.add((renzi_interview, dcterms.description, Literal(row["description"])))
    g.add((renzi_interview, dcterms.description, Literal(row["notes"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/renzi_interview_2000.ttl")

print("CSV converted to TTL!")
