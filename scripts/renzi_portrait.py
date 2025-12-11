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

renzi_portrait = URIRef(rrr + "portrait_of_renzo_renzi")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
renzi_collection = URIRef(rrr + "renzo_renzi_collection")

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))

# MAPPING TO ONTOLOGIES

portrait_of_renzo_renzi = read_csv("../csv/renzi_portrait.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in portrait_of_renzo_renzi.iterrows():
    g.add((renzi_portrait, RDF.type, schema.Photograph))
    g.add((schema.Photograph, RDFS.subClassOf, schema.CreativeWork))
    g.add((renzi_portrait, dc.title, Literal(row["title"])))
    g.add((renzi_portrait, dcterms.creator, Literal(row["creator"])))
    g.add((renzi_portrait, FOAF.depicts, renzo_renzi))
    g.add((renzi_portrait, schema.about, Literal(row["depicted_event"])))
    g.add((renzi_portrait, schema.color, Literal(row["colour"], datatype=XSD.string)))
    g.add((renzi_portrait, schema.material, Literal(row["material_technique"])))
    g.add((renzi_portrait, schema.artform, Literal(row["physical_description"])))
    g.add((renzi_portrait, crm.P45_consists_of, Literal(row["carrier_type"])))
    g.add((renzi_portrait, schema.fileFormat, Literal(row["format"])))
    g.add((renzi_portrait, dcterms.isPartOf, Literal(row["collection"])))
    g.add((renzi_portrait, crm.P52_has_current_owner, Literal(row["owner"])))
    g.add((renzi_portrait, dcterms.isPartOf, renzi_collection))
    g.add((renzi_portrait, crm.P50_has_current_keeper, cineteca_di_bologna))
    g.add((renzi_collection, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((renzi_portrait, schema.description, Literal(row["notes"])))
    g.add((renzi_portrait, dcterms.rights, Literal(row["rights"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/renzi_portrait.ttl")
print("CSV converted to TTL!")
