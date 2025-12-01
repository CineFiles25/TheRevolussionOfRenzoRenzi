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
    "skos": skos,
}

def graph_bindings():
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

# ENTITIES 

drawing_gelsomina = URIRef(rrr + "drawing_gelsomina_lastrada")
la_strada_film = URIRef(rrr + "la_strada_film")
renzo_renzi = URIRef(rrr + "renzo_renzi")
giulietta_masina = URIRef(rrr + "giulietta_masina")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")

g.add((la_strada_film, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# MAPPING TO ONTOLOGIES

drawing_df = read_csv("../csv/drawing_gelsomina_lastrada.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in drawing_df.iterrows():
    g.add((drawing_gelsomina, RDF.type, schema.VisualArtwork))
    g.add((schema.VisualArtwork, RDFS.subClassOf, schema.CreativeWork))
    g.add((drawing_gelsomina, dc.title, Literal(row["title"])))
    g.add((drawing_gelsomina, dcterms.creator, renzo_renzi))
    g.add((drawing_gelsomina, foaf.depicts, giulietta_masina))
    g.add((drawing_gelsomina, schema.dateCreated, Literal(row["creation_date"], datatype=XSD.gYear)))
    g.add((drawing_gelsomina, dc.description, Literal(row["description"])))
    g.add((drawing_gelsomina, dcterms.medium, Literal(row["technique"])))
    g.add((drawing_gelsomina, dcterms.material, Literal(row["material"])))
    g.add((drawing_gelsomina, dcterms.extent, Literal(row["dimensions"])))
    g.add((drawing_gelsomina, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((renzi_collection, dcterms.hasPart, drawing_gelsomina))
    g.add((drawing_gelsomina, schema.location, renzi_library))
    g.add((drawing_gelsomina, dcterms.rights, Literal(row["rights"])))
    g.add((drawing_gelsomina, schema.description , URIRef(row["description"])))
    g.add((drawing_gelsomina, dcterms.relation, la_strada_film))

# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/drawing_gelsomina_lastrada.ttl")

print("CSV converted to TTL!")

