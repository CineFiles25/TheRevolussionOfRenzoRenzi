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

premiere_photo = URIRef(rrr + "photo_lastrada_01")
la_strada_film = URIRef(rrr + "la_strada_film")
federico_fellini = URIRef(rrr + "federico_fellini")
cinema_fulgor = URIRef(rrr + "cinema_fulgor")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
giulietta_masina = URIRef(rrr + "giulietta_masina")
bologna = URIRef(rrr + "bologna")

g.add((la_strada_film, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))
g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((giulietta_masina, OWL.sameAs, URIRef("http://viaf.org/viaf/96166248")))
g.add((cinema_fulgor, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q36839368")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# MAPPING TO ONTOLOGIES

photo_lastrada_01 = read_csv("../csv/photo_lastrada_01.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in photo_lastrada_01.iterrows():
    g.add((premiere_photo, RDF.type, schema.Photograph))
    g.add((schema.Photograph, RDFS.subClassOf, schema.CreativeWork))
    g.add((premiere_photo, dc.identifier, Literal(row["id"])))
    g.add((premiere_photo, dcterms.conformsTo, Literal(row["standard"])))
    g.add((premiere_photo, dcterms.title, Literal(row["title"])))
    g.add((premiere_photo, dcterms.type, Literal(row["object_type"])))
    g.add((premiere_photo, dcterms.description, Literal(row["inscription"], lang=row["language"])))
    g.add((premiere_photo, dcterms.creator, Literal(row["creator"])))
    g.add((premiere_photo, foaf.depicts, federico_fellini))
    g.add((premiere_photo, foaf.depicts, giulietta_masina))
    g.add((premiere_photo, schema.contentLocation, cinema_fulgor))
    g.add((cinema_fulgor, RDF.type, schema.MovieTheater))
    g.add((cinema_fulgor, schema.location, bologna))
    g.add((premiere_photo, dcterms.created, Literal(row["creation_year"], datatype=XSD.gYear)))
    g.add((premiere_photo, schema.color, Literal(row["colour"])))
    g.add((premiere_photo, dcterms.medium, Literal(row["material_technique"])))
    g.add((premiere_photo, dc.identifier, Literal(row["inventory_number"])))
    g.add((premiere_photo, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((premiere_photo, dcterms.isPartOf, Literal(row["collection"])))
    g.add((premiere_photo, schema.artform, Literal(row["physical_description"])))
    g.add((premiere_photo, dcterms.description, Literal(row["notes"])))
    g.add((premiere_photo, dcterms.rights, Literal(row["rights"])))
    g.add((premiere_photo, dcterms.relation, la_strada_film))
    g.add((premiere_photo, schema.about, la_strada_film))

# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/photo_lastrada_01.ttl")

print("CSV converted to TTL!")
