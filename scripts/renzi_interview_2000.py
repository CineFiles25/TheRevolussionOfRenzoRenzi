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

renzi_interview = URIRef(rrr + "renzi_interview_2000")
renzo_renzi = URIRef(rrr + "renzo_renzi")
bologna = URIRef(rrr + "bologna")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzi_collection = URIRef(rrr + "renzi_collection")
renzi_library = URIRef(rrr + "renzo_renzi_library")

# Base types
g.add((renzi_interview, RDF.type, schema.Interview))
g.add((schema.Interview, RDFS.subClassOf, schema.CreativeWork))

g.add((renzo_renzi, RDF.type, foaf.Person))
g.add((bologna, RDF.type, schema.Place))
g.add((cineteca_di_bologna, RDF.type, schema.Organization))
g.add((renzi_collection, RDF.type, dcterms.Collection))
g.add((renzi_library, RDF.type, schema.Library))

# Authority links
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# CSV LOADING
# N.B. run this script from the `scripts/` directory

interview_df = read_csv(
    "../csv/renzi_interview_2000.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# MAPPING TO RDF

for _, row in interview_df.iterrows():

    # IDENTIFIER, STANDARD, TYPE
    if row.get("id"):
        g.add((renzi_interview, dcterms.identifier, Literal(row["id"])))

    if row.get("standard"):
        g.add((renzi_interview, dcterms.conformsTo, Literal(row["standard"])))

    if row.get("resource_type"):
        g.add((renzi_interview, dcterms.type, Literal(row["resource_type"])))

    # TITLES
    if row.get("title"):
        g.add((renzi_interview, dcterms.title, Literal(row["title"])))

    if row.get("other_title_information"):
        g.add((renzi_interview, schema.alternateName, Literal(row["other_title_information"])))

    # PEOPLE (INTERVIEWEE / DIRECTOR / INTERVIEWER)

    g.add((renzi_interview, schema.interviewee, renzo_renzi))
    g.add((renzi_interview, schema.about, renzo_renzi))

    if row.get("interviewee"):
        g.add((renzi_interview, dc.subject, Literal(row["interviewee"])))

    if row.get("interviewee_uri"):
        g.add((renzi_interview, dcterms.relation, Literal(row["interviewee_uri"], datatype=XSD.anyURI)))

    if row.get("director"):
        g.add((renzi_interview, schema.director, Literal(row["director"])))
    if row.get("director_uri"):
        g.add((renzi_interview, dcterms.relation, Literal(row["director_uri"], datatype=XSD.anyURI)))

    if row.get("interviewer"):
        g.add((renzi_interview, dcterms.contributor, Literal(row["interviewer"])))
        g.add((renzi_interview, schema.interviewer, Literal(row["interviewer"])))
    if row.get("interviewer_uri"):
        g.add((renzi_interview, dcterms.relation, Literal(row["interviewer_uri"], datatype=XSD.anyURI)))

    # PRODUCTION COMPANY / PLACE / YEAR

    if row.get("production_company"):
        g.add((renzi_interview, schema.productionCompany, Literal(row["production_company"])))
        g.add((renzi_interview, dcterms.publisher, Literal(row["production_company"])))

    if row.get("production_company_uri"):
        g.add((renzi_interview, dcterms.relation, Literal(row["production_company_uri"], datatype=XSD.anyURI)))

    if row.get("production_place"):
        g.add((renzi_interview, dcterms.spatial, Literal(row["production_place"])))

    g.add((renzi_interview, schema.locationCreated, bologna))

    if row.get("production_place_uri"):
        g.add((renzi_interview, dcterms.relation, Literal(row["production_place_uri"], datatype=XSD.anyURI)))

    if row.get("production_year"):
        g.add((renzi_interview, dcterms.created, Literal(row["production_year"], datatype=XSD.gYear)))

    # TECHNICAL FEATURES

    if row.get("duration"):
        g.add((renzi_interview, schema.duration, Literal(row["duration"])))

    if row.get("colour"):
        g.add((renzi_interview, schema.color, Literal(row["colour"])))

    if row.get("sound"):
        g.add((renzi_interview, dcterms["format"], Literal(row["sound"])))

    if row.get("format"):
        g.add((renzi_interview, dcterms["format"], Literal(row["format"])))

    if row.get("language"):
        g.add((renzi_interview, schema.inLanguage, Literal(row["language"])))

    # INSTITUTION / COLLECTION / CURRENT LOCATION

    g.add((renzi_interview, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((renzi_collection, dcterms.hasPart, renzi_interview))
    g.add((renzi_interview, dcterms.location, renzi_library))

    if row.get("institution"):
        g.add((renzi_interview, dcterms.publisher, Literal(row["institution"])))

    if row.get("collection"):
        g.add((renzi_collection, dcterms.title, Literal(row["collection"])))

    if row.get("current_location"):
        g.add((renzi_interview, dcterms.location, Literal(row["current_location"])))

    if row.get("institution_uri"):
        g.add((renzi_interview, dcterms.relation, Literal(row["institution_uri"], datatype=XSD.anyURI)))

    # RIGHTS, DESCRIPTION, NOTES

    if row.get("rights"):
        g.add((renzi_interview, dcterms.rights, Literal(row["rights"])))

    if row.get("description"):
        g.add((renzi_interview, dcterms.description, Literal(row["description"])))

    if row.get("notes"):
        g.add((renzi_interview, dcterms.description, Literal(row["notes"])))


# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/renzi_interview_2000.ttl")
print("CSV converted to TTL!")
