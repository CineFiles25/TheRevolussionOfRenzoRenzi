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

po_documentary = URIRef(rrr + "quando_il_po_è_dolce")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
columbus_film = URIRef(rrr + "columbus_film")

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))

# MAPPING TO ONTOLOGIES

quando_il_po_è_dolce = pd.read_csv("../csv/po_documentary.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

for idx, row in quando_il_po_è_dolce.iterrows():
    g.add((po_documentary, RDF.type, URIRef(schema + "Movie")))
    g.add((po_documentary, RDFS.subClassOf, URIRef(schema + "CreativeWork")))
    g.add((po_documentary, dc.title, Literal(row["Title"])))
    g.add((po_documentary, schema.alternateName, Literal(row["Alt Title"])))
    g.add((po_documentary, schema.director, renzo_renzi))
    g.add((po_documentary, schema.author, renzo_renzi))
    g.add((po_documentary, schema.edition, Literal(row["Edition"])))
    g.add((po_documentary, schema.genre, Literal(row["Type"])))
    g.add((po_documentary, schema.countryOfOrigin, Literal(row["Country"])))    
    g.add((po_documentary, schema.productionCompany, columbus_film))    
    g.add((po_documentary, schema.datePublished, Literal(row["Year"], datatype=XSD.gYear)))
    g.add((po_documentary, schema.duration, Literal(row["Running Time"])))
    g.add((po_documentary, schema.color, Literal(row["Color"])))
    g.add((po_documentary, schema.encodingFormat, Literal(row["Film Type"])))
    g.add((po_documentary, schema.frameRate, Literal(row["Frame Rate"])))
    g.add((po_documentary, schema.contentSize, Literal(row["Film Length"])))    
    g.add((po_documentary, schema.sound, Literal(row["Sound"])))
    g.add((po_documentary, schema.inLanguage, Literal(row["Language"])))
    g.add((po_documentary, schema.about, Literal(row["Subject"])))
    g.add((po_documentary, schema.spatialCoverage, Literal(row["Filming Location"])))
    g.add((po_documentary, schema.musicBy, Literal(row["Music Composer"])))
    g.add((po_documentary, schema.contentRating, Literal(row["Certificate"])))
    
# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/po_documentary.ttl")

print("CSV converted to TTL!")
