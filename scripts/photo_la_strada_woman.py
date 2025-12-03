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

woman_photo = URIRef(rrr + "photo_la_strada_woman")
giulietta_masina = URIRef(rrr + "giulietta_masina")
la_strada_film = URIRef(rrr + "la_strada_film")

g.add((la_strada_film, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))
g.add((giulietta_masina, OWL.sameAs, URIRef("http://viaf.org/viaf/37021297")))

# MAPPING TO ONTOLOGIES

photo_df = pd.read_csv("../csv/photo_la_strada_woman.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in photo_df.iterrows():
    g.add((woman_photo, RDF.type, URIRef(schema + "Photograph")))
    g.add((woman_photo, RDFS.subClassOf, URIRef(schema + "CreativeWork")))
    g.add((woman_photo, dcterms.title, Literal(row["title"])))
    g.add((woman_photo, dcterms.alternative, Literal(row["other_title_information"])))
    g.add((woman_photo, dcterms.subject, Literal(row["depicted_event"])))
    g.add((woman_photo, dcterms.subject, Literal(row["depicted_people"])))
    g.add((woman_photo, dcterms.spatial, Literal(row["depicted_place"])))
    g.add((woman_photo, dcterms.created, Literal(row["creation_year"], datatype=XSD.gYear)))
    g.add((woman_photo, schema.colour, Literal(row["colour"])))
    g.add((woman_photo, dcterms.medium, Literal(row["material_technique"])))
    g.add((woman_photo, dcterms.isPartOf, Literal(row["collection"])))
    g.add((woman_photo, dcterms.extent, Literal(row["physical_description"])))
    g.add((woman_photo, dcterms.description, Literal(row["notes"])))
    g.add((woman_photo, dcterms.identifier, Literal(row["identifiers"])))
    g.add((woman_photo, dcterms.relation, Literal(row["related_works"])))
    g.add((woman_photo, dcterms.rights, Literal(row["rights"])))
    g.add((woman_photo, dcterms.type, Literal(row["resource_type"])))
    g.add((woman_photo, dcterms.language, Literal(row["language"])))

# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/photo_la_strada_woman.ttl")

print("CSV converted to TTL!")
