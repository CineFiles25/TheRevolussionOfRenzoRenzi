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

g = graph_bindings()

# ENTITIES 

renzi_library = URIRef(rrr + "renzo_renzi_library")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
renzi_collection = URIRef(rrr + "renzi_collection")
guida_screenplay = URIRef(rrr + "guida_per_camminare_all_ombra")
book_il_primo_fellini = URIRef(rrr + "book_il_primo_fellini")

# SAMEAS

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))

# MAPPING 

renzo_renzi_library = read_csv("../csv/renzi_library.csv", keep_default_na=False, encoding="utf-8")

for idx, row in renzo_renzi_library.iterrows():
    g.add((renzi_library, RDF.type, schema.Library))
    g.add((schema.Library, RDFS.subClassOf, schema.LocalBusiness))
    g.add((renzi_library, OWL.sameAs, URIRef("https://anagrafe.iccu.sbn.it/isil/IT-BO0286")))
    g.add((renzi_library, dc.identifier, Literal(row["id_isil"])))
    g.add((renzi_library, schema.name, Literal(row["name"])))
    g.add((renzi_library, schema.alternateName, Literal(row["alt_title"])))
    g.add((renzi_library, schema.additionalType, Literal(row["original_function"])))
    g.add((renzi_library, crm.P52_has_current_owner,cineteca_di_bologna))
    g.add((renzi_library, schema.date, Literal(row["completion_year"], datatype=XSD.gYear)))
    g.add((renzi_library, schema.foundingDate, Literal(row["foundation_year"], datatype=XSD.gYear)))
    g.add((renzi_library, schema.address, Literal(row["address"])))
    g.add((renzi_library, schema.addressLocality, bologna))
    g.add((renzi_library, schema.geo, Literal(row["coordinates"])))
    g.add((renzi_library, schema.url, Literal(row["website"], datatype=XSD.anyURI)))
    g.add((renzi_library, schema.email, Literal(row["email"], datatype=XSD.anyURI)))
    g.add((renzi_library, schema.telephone, Literal(row["phone_number"], datatype=XSD.string)))
    g.add((renzi_library, schema.isAccessibleForFree, Literal(row["accessible"], datatype=XSD.boolean)))
    g.add((renzi_library, dc.description, Literal(row["structure_type"])))
    g.add((renzi_library, schema.floorSize, Literal(row["area"], datatype=XSD.string)))
    g.add((renzi_library, schema.seatingCapacity, Literal(row["seats"], datatype=XSD.integer)))
    g.add((renzi_library, dc.description, Literal(row["audio_system"])))
    g.add((renzi_library, dc.description, Literal(row["video_system"])))
    g.add((renzi_library, dbo.dedicatedTo, renzo_renzi))
    g.add((guida_screenplay, schema.location, renzi_library))
    g.add((book_il_primo_fellini, schema.location, renzi_library))
    g.add((renzi_collection, schema.location, renzi_library))
    g.add((renzi_collection, rdf.type, schema.Collection))
    g.add((renzi_collection, crm.P52_has_current_owner, cineteca_di_bologna))
    
   


# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/renzi_library.ttl") 

print("CSV converted to TTL!")
