import pandas as pd
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

# ENTITIES 

renzi_letter_1942 = URIRef(rrr + "renzi_letter_1942")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzo_renzi_collection = URIRef(rrr + "renzo_renzi_collection")

# SAMEAS

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((renzo_renzi_collection, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# CSV LOADING

renzi_letter = pd.read_csv("csv/renzi_letter_1942.csv", keep_default_na=False, encoding="utf-8")

g = graph_bindings()

# MAPPING TO ONTOLOGIES

for idx, row in renzi_letter.iterrows():
    # type
    g.add((renzi_letter_1942, RDF.type, schema.ArchiveComponent))
    g.add((schema.ArchiveComponent, RDFS.subClassOf, schema.CreativeWork))

    # identifiers
    g.add((renzi_letter_1942, dcterms.identifier, Literal(row["id"])))
    g.add((renzi_letter_1942, dcterms.identifier, Literal(row["identifiers"])))

    # standard
    g.add((renzi_letter_1942, dcterms.conformsTo, Literal(row["standard"])))

    # titles
    g.add((renzi_letter_1942, dcterms.title, Literal(row["title"])))
    g.add((renzi_letter_1942, dcterms.alternative, Literal(row["other_title_information"])))

    # creator & other creators
    g.add((renzi_letter_1942, dcterms.creator, renzo_renzi))
    g.add((renzi_letter_1942, dcterms.contributor, Literal(row["other_creators"])))

    # date
    g.add((renzi_letter_1942, dcterms.created, Literal(row["date"], datatype=XSD.date)))

    # level of description
    g.add((renzi_letter_1942, dcterms.type, Literal(row["level_of_description"])))

    # extent
    g.add((renzi_letter_1942, dcterms.extent, Literal(row["extent"])))

    # scope and content
    g.add((renzi_letter_1942, dcterms.description, Literal(row["scope_and_content"])))

    # physical description
    g.add((renzi_letter_1942, dcterms.medium, Literal(row["physical_description"])))

    # material type
    g.add((renzi_letter_1942, schema.additionalType, Literal(row["material_type"])))

    # language
    g.add((renzi_letter_1942, dcterms.language, Literal(row["language"])))

    # pages
    g.add((renzi_letter_1942, schema.numberOfPages, Literal(row["pages"], datatype=XSD.integer)))

    # page URIs (split on " | ")
    for uri in row["page_uris"].split("|"):
        g.add((renzi_letter_1942, schema.associatedMedia, URIRef(uri.strip())))

    # institution / collection / location
    g.add((renzi_letter_1942, schema.holdingArchive, cineteca_di_bologna))
    g.add((cineteca_di_bologna, dcterms.title, Literal(row["institution"])))

    g.add((renzi_letter_1942, dcterms.isPartOf, renzo_renzi_collection))
    g.add((renzo_renzi_collection, dcterms.title, Literal(row["collection"])))

    g.add((renzi_letter_1942, dcterms.spatial, Literal(row["current_location"])))

    # access & reproduction conditions
    g.add((renzi_letter_1942, dcterms.accessRights, Literal(row["conditions_governing_access"])))
    g.add((renzi_letter_1942, dcterms.rights, Literal(row["conditions_governing_reproduction"])))

    # related works
    g.add((renzi_letter_1942, dcterms.relation, Literal(row["related_works"])))

    # rights statement
    g.add((renzi_letter_1942, dcterms.rights, Literal(row["rights"])))

# SERIALIZATION

g.serialize(format="turtle", destination="ttl/renzi_letter_1942.ttl")

print("CSV converted to TTL for Renzi's 1942 letter!")
