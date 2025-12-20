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

po_documentary = URIRef(rrr + "quando_il_po_è_dolce")
renzo_renzi = URIRef(rrr + "renzo_renzi")
enzo_masetti = URIRef(rrr + "enzo_masetti")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
delta_po_river = URIRef(rrr + "delta_po_river")
columbus_film = URIRef(rrr + "columbus_film")

# SAMEAS 

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((delta_po_river, OWL.sameAs, URIRef("http://viaf.org/viaf/316432038")))
g.add((enzo_masetti, OWL.sameAs, URIRef("http://viaf.org/viaf/56806835")))

# MAPPING

quando_il_po_è_dolce = read_csv("../csv/po_documentary.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in quando_il_po_è_dolce.iterrows():
    g.add((po_documentary, RDF.type, schema.Movie))
    g.add((schema.Movie, RDFS.subClassOf, schema.CreativeWork))
    g.add((po_documentary, dc.title, Literal(row["title"])))
    g.add((po_documentary, schema.alternateName, Literal(row["other_title_information"])))
    g.add((po_documentary, dc.date, Literal(row["edition"], datatype=XSD.gYear)))
    g.add((po_documentary, schema.director, renzo_renzi))
    g.add((po_documentary, dbo.writer, renzo_renzi))
    g.add((po_documentary, schema.countryOfOrigin, Literal(row["country"])))    
    g.add((po_documentary, schema.inLanguage, Literal(row["language"])))
    g.add((po_documentary, schema.productionCompany, columbus_film))    
    g.add((po_documentary, schema.datePublished, Literal(row["publication_year"], datatype=XSD.gYear)))
    g.add((po_documentary, schema.contentSize, Literal(row["length"])))   
    g.add((po_documentary, schema.duration, Literal(row["duration"], datatype=XSD.duration)))
    g.add((po_documentary, schema.color, Literal(row["colour"])))
    g.add((po_documentary, schema.encodingFormat, Literal(row["film_type"])))
    g.add((po_documentary, schema.frameRate, Literal(row["format"])))
    g.add((po_documentary, schema.sound, Literal(row["sound"])))
    g.add((po_documentary, schema.about, delta_po_river))
    g.add((po_documentary, schema.location, delta_po_river))
    g.add((po_documentary, schema.musicBy, enzo_masetti))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/po_documentary.ttl")

print("CSV converted to TTL!!")
