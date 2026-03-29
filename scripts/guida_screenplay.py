from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES
rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
owl = Namespace("http://www.w3.org/2002/07/owl#")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")

# GRAPH
g = Graph()

# Bindings
g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)
g.bind("dc", dc)
g.bind("crm", crm)
g.bind("owl", owl)
g.bind("skos", skos)

# ENTITIES
manuscript = URIRef(rrr + "guida_per_camminare_all_ombra")
renzi = URIRef(rrr + "renzo_renzi")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")
cineteca = URIRef(rrr + "cineteca_di_bologna")

# LOAD CSV
df = read_csv("../csv/guida_screenplay.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((manuscript, RDF.type, schema.Manuscript))

# CSV → RDF MAPPING
for _, row in df.iterrows():
    # Title
    if row.get("title"):
        g.add((manuscript, dcterms.title, Literal(row["title"])))
    # Alternative title
    if row.get("other_title_information"):
        g.add((manuscript, dcterms.alternative, Literal(row["other_title_information"])))
    # Creation date
    if row.get("date"):
        g.add((manuscript, dcterms.created, Literal(row["date"], datatype=XSD.gYearMonth)))
    # Description fields
    if row.get("level_of_description"):
        g.add((manuscript, dcterms.description, Literal(row["level_of_description"])))
    if row.get("scope"):
        g.add((manuscript, dcterms.description, Literal(row["scope"])))
    if row.get("content"):
        g.add((manuscript, dcterms.description, Literal(row["content"])))
    # Extent
    if row.get("extent"):
        g.add((manuscript, dcterms.extent, Literal(row["extent"])))
    # Medium
    if row.get("medium"):
        g.add((manuscript, dcterms.medium, Literal(row["medium"])))
    # Provenance
    if row.get("archival_description"):
        g.add((manuscript, dcterms.provenance, Literal(row["archival_description"])))
    # Writer (resource)
    g.add((manuscript, schema.creator, renzi))
    # Rights
    if row.get("rights"):
        g.add((manuscript, dcterms.rights, Literal(row["rights"])))
    # Access conditions
    if row.get("conditions_governing_access"):
        g.add((manuscript, dcterms.accessRights, Literal(row["conditions_governing_access"])))
    if row.get("conditions_governing_reproduction"):
        g.add((manuscript, dcterms.accessRights, Literal(row["conditions_governing_reproduction"])))
    # Language
    if row.get("language"):
        g.add((manuscript, dcterms.language, Literal(row["language"])))
    # Related works (literal description only)
    if row.get("related_works"):
        g.add((manuscript, dcterms.relation, Literal(row["related_works"])))

    # Authority files — VIAF
    if row.get("viaf_uri"):
        g.add((manuscript, owl.sameAs, URIRef(row["viaf_uri"])))
    # Authority files — Wikidata
    if row.get("wikidata_uri"):
        g.add((manuscript, owl.sameAs, URIRef(row["wikidata_uri"])))
    # Authority files — LCNAF / altre authority
    if row.get("authority_uri"):
        g.add((manuscript, owl.sameAs, URIRef(row["authority_uri"])))
    # Concetto SKOS
    if row.get("skos_concept_uri"):
        g.add((manuscript, skos.closeMatch, URIRef(row["skos_concept_uri"])))

    # COLLECTION & LOCATION
    g.add((manuscript, dcterms.isPartOf, renzi_collection))
    g.add((renzi_collection, dcterms.hasPart, manuscript))
    g.add((manuscript, schema.location, renzi_library))
    g.add((manuscript, crm.P52_has_current_owner, cineteca))

# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/guida_screenplay.ttl")
print("guida_screenplay.ttl generated successfully!")
