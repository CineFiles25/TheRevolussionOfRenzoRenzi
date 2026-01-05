from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS

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

guida_screenplay = URIRef(rrr + "guida_per_camminare_all_ombra")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")
bologna = URIRef(rrr + "bologna")

# SAMEAS 

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# MAPPING

guida_per_camminare_all_ombra = read_csv("../csv/guida_screenplay.csv", keep_default_na=False, encoding="utf-8")

for idx, row in guida_per_camminare_all_ombra.iterrows():
    g.add((guida_screenplay, RDF.type, schema.Manuscript))
    g.add((guida_screenplay, schema.additionalType, schema.ArchiveComponent))
    g.add((schema.Manuscript, RDFS.subClassOf, schema.CreativeWork))
    g.add((schema.ArchiveComponent, RDFS.subClassOf, schema.CreativeWork))
    g.add((guida_screenplay, dcterms.title, Literal(row["title"])))
    g.add((guida_screenplay, dcterms.alternative, Literal(row["other_title_information"])))
    g.add((guida_screenplay, dcterms.created, Literal(row["date"], datatype=XSD.gYearMonth)))
    g.add((guida_screenplay, dcterms.description, Literal(row["level_of_description"])))
    g.add((guida_screenplay, dcterms.extent, Literal(row["extent"])))
    g.add((guida_screenplay, dcterms.medium, Literal(row["medium"])))
    g.add((guida_screenplay, dbo.writer, renzo_renzi))   
    g.add((guida_screenplay, dcterms.provenance, Literal(row["archival_description"])))
    g.add((guida_screenplay, crm.P52_has_current_owner, Literal(row["owner"])))
    g.add((renzi_collection, dcterms.hasPart, guida_screenplay))
    g.add((renzi_collection, RDF.type, dcterms.Collection))
    g.add((renzi_collection, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((guida_screenplay, schema.itemLocation, renzi_library))
    g.add((guida_screenplay, schema.holdingArchive, cineteca_di_bologna))
    g.add((cineteca_di_bologna, schema.location, bologna))
    g.add((guida_screenplay, dcterms.description, Literal(row["scope"])))
    g.add((guida_screenplay, dcterms.description, Literal(row["content"])))
    g.add((guida_screenplay, dcterms.accessRights, Literal(row["conditions_governing_access"])))
    g.add((guida_screenplay, dcterms.accessRights, Literal(row["conditions_governing_reproduction"])))
    g.add((guida_screenplay, dcterms.language, Literal(row["language"], datatype=XSD.language)))    
    g.add((guida_screenplay, dcterms.relation, Literal(row["related_works"])))
    g.add((guida_screenplay, dcterms.rights, Literal(row["rights"])))
    g.add((guida_screenplay, dcterms.subject, Literal(row["subject"])))

# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/guida_screenplay.ttl")

print("CSV converted to TTL!")