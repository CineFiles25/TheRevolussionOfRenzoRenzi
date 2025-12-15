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

caricature_fellini_renzi = URIRef(rrr + "caricature_fellini_renzi")
federico_fellini = URIRef(rrr + "federico_fellini")
renzo_renzi = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")

# Base types
g.add((caricature_fellini_renzi, RDF.type, schema.VisualArtwork))
g.add((schema.VisualArtwork, RDFS.subClassOf, schema.CreativeWork))

g.add((federico_fellini, RDF.type, foaf.Person))
g.add((renzo_renzi, RDF.type, foaf.Person))
g.add((cineteca_di_bologna, RDF.type, schema.Organization))
g.add((renzi_library, RDF.type, schema.Library))
g.add((renzi_collection, RDF.type, dcterms.Collection))

# Authority links
g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# CSV LOADING
# N.B. run this script from the `scripts/` directory

caricature_df = read_csv(
    "../csv/caricature_fellini_renzi.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# MAPPING TO RDF

for _, row in caricature_df.iterrows():

    # Identifier and standard
    if row.get("id"):
        g.add((caricature_fellini_renzi, dcterms.identifier, Literal(row["id"])))
    if row.get("standard"):
        g.add((caricature_fellini_renzi, dcterms.conformsTo, Literal(row["standard"])))

    # Titles
    if row.get("title"):
        g.add((caricature_fellini_renzi, dcterms.title, Literal(row["title"])))
    if row.get("other_title_information"):
        g.add((caricature_fellini_renzi, schema.alternateName, Literal(row["other_title_information"])))

    # Inscription and description
    if row.get("inscription"):
        g.add((caricature_fellini_renzi, dcterms.description, Literal(row["inscription"])))
    if row.get("description"):
        g.add((caricature_fellini_renzi, dcterms.description, Literal(row["description"])))

    # CREATOR AND DEPICTED

    # Literal creator (kept)
    if row.get("creator"):
        g.add((caricature_fellini_renzi, dcterms.creator, Literal(row["creator"])))

    # Resource-level creator (Renzi)
    g.add((caricature_fellini_renzi, schema.creator, renzo_renzi))

    # Creator URI as related web identifier
    if row.get("creator_uri"):
        g.add((caricature_fellini_renzi, dcterms.relation, Literal(row["creator_uri"], datatype=XSD.anyURI)))

    # Depicted people: literal + resource
    if row.get("depicted_people"):
        g.add((caricature_fellini_renzi, dc.subject, Literal(row["depicted_people"])))
    g.add((caricature_fellini_renzi, schema.about, federico_fellini))

    if row.get("depicted_people_uri"):
        g.add((caricature_fellini_renzi, dcterms.relation, Literal(row["depicted_people_uri"], datatype=XSD.anyURI)))

    # CREATION / TECHNIQUE / MATERIAL

    if row.get("creation_date"):
        g.add((caricature_fellini_renzi, dcterms.created, Literal(row["creation_date"])))
    if row.get("technique"):
        g.add((caricature_fellini_renzi, dcterms.medium, Literal(row["technique"])))
    if row.get("material"):
        g.add((caricature_fellini_renzi, dcterms.material, Literal(row["material"])))

    if row.get("dimensions"):
        g.add((caricature_fellini_renzi, dcterms.extent, Literal(row["dimensions"])))

    # INSTITUTION / COLLECTION / LOCATION (project graph links)

    g.add((caricature_fellini_renzi, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((renzi_collection, dcterms.hasPart, caricature_fellini_renzi))
    g.add((caricature_fellini_renzi, dcterms.isPartOf, renzi_collection))

    g.add((caricature_fellini_renzi, dcterms.location, renzi_library))
    g.add((renzi_library, schema.location, cineteca_di_bologna))

    # Literals from CSV (kept, but without clobbering isPartOf)
    if row.get("institution"):
        g.add((caricature_fellini_renzi, dcterms.publisher, Literal(row["institution"])))
    if row.get("collection"):
        g.add((caricature_fellini_renzi, dcterms.description, Literal(row["collection"])))
    if row.get("current_location"):
        g.add((caricature_fellini_renzi, dcterms.description, Literal(row["current_location"])))

    # External URIs
    if row.get("institution_uri"):
        g.add((caricature_fellini_renzi, dcterms.relation, Literal(row["institution_uri"], datatype=XSD.anyURI)))

    if row.get("collection_uri"):
        for uri_str in [u.strip() for u in row["collection_uri"].split("|") if u.strip()]:
            g.add((caricature_fellini_renzi, dcterms.relation, Literal(uri_str, datatype=XSD.anyURI)))

    if row.get("current_location_uri"):
        g.add((caricature_fellini_renzi, dcterms.relation, Literal(row["current_location_uri"], datatype=XSD.anyURI)))

    # RIGHTS / TYPE / LANGUAGE

    if row.get("rights"):
        g.add((caricature_fellini_renzi, dcterms.rights, Literal(row["rights"])))

    if row.get("resource_type"):
        g.add((caricature_fellini_renzi, dcterms.type, Literal(row["resource_type"])))

    if row.get("language"):
        g.add((caricature_fellini_renzi, schema.inLanguage, Literal(row["language"])))


# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/caricature_fellini_renzi.ttl")
print("CSV converted to TTL!")
