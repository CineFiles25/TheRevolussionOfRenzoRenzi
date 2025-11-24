import pandas as pd
from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# ===================== NAMESPACES =====================

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
    """Bind all namespaces to the RDF graph."""
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g


# ===================== LOCAL ENTITIES =====================

renzi_interview_2000 = URIRef(rrr + "renzi_interview_2000")

# People local resources
interviewer_res = URIRef(rrr + "interviewer_renzi_interview_2000")
interviewee_res = URIRef(rrr + "interviewee_renzi_interview_2000")

# Place
interview_place_res = URIRef(rrr + "interview_place_renzi_2000")

# Institution and collection
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzo_renzi_collection = URIRef(rrr + "renzo_renzi_collection")


# ===================== READ CSV =====================

interview_df = pd.read_csv(
    "/mnt/data/renzi_interview_2000.csv",
    keep_default_na=False,
    encoding="utf-8"
)

g = graph_bindings()


# ===================== MAP CSV → RDF =====================

for idx, row in interview_df.iterrows():

    # Language tag for literals
    language = str(row["language"]).strip() if "language" in row and str(row["language"]).strip() else None

    # --- TYPES FOR THE MAIN RESOURCE ---

    g.add((renzi_interview_2000, RDF.type, schema.Interview))
    g.add((renzi_interview_2000, RDF.type, schema.CreativeWork))
    g.add((renzi_interview_2000, RDF.type, fiaf.FilmRelatedObject))

    # Optional resource type literal
    if row.get("resource_type"):
        g.add((renzi_interview_2000, dcterms.type, Literal(row["resource_type"])))

    # --- IDENTIFIER AND STANDARD ---

    if row.get("id"):
        g.add((renzi_interview_2000, dc.identifier, Literal(row["id"])))

    if row.get("standard"):
        g.add((renzi_interview_2000, dcterms.conformsTo, Literal(row["standard"])))

    # --- TITLE ---

    if row.get("title"):
        if language:
            g.add((renzi_interview_2000, dc.title, Literal(row["title"], lang=language)))
        else:
            g.add((renzi_interview_2000, dc.title, Literal(row["title"])))

    # --- INTERVIEWER ---

    g.add((interviewer_res, RDF.type, FOAF.Person))

    if row.get("interviewer"):
        g.add((interviewer_res, FOAF.name, Literal(row["interviewer"])))
        g.add((renzi_interview_2000, schema.interviewer, interviewer_res))

    if row.get("interviewer_uri"):
        g.add((interviewer_res, OWL.sameAs, URIRef(row["interviewer_uri"])))

    # --- INTERVIEWEE ---

    g.add((interviewee_res, RDF.type, FOAF.Person))

    if row.get("interviewee"):
        g.add((interviewee_res, FOAF.name, Literal(row["interviewee"])))
        g.add((renzi_interview_2000, schema.interviewee, interviewee_res))

    if row.get("interviewee_uri"):
        g.add((interviewee_res, OWL.sameAs, URIRef(row["interviewee_uri"])))

    # --- DATE AND PLACE ---

    if row.get("date"):
        g.add((renzi_interview_2000,
               schema.datePublished,
               Literal(row["date"], datatype=XSD.date)))

    # Place of interview
    g.add((interview_place_res, RDF.type, schema.Place))

    if row.get("place"):
        if language:
            g.add((interview_place_res, schema.name, Literal(row["place"], lang=language)))
        else:
            g.add((interview_place_res, schema.name, Literal(row["place"])))

        g.add((renzi_interview_2000, schema.locationCreated, interview_place_res))

    if row.get("place_uri"):
        g.add((interview_place_res, OWL.sameAs, URIRef(row["place_uri"])))

    # --- FORMAT AND DURATION ---

    if row.get("format"):
        g.add((renzi_interview_2000, schema.encodingFormat, Literal(row["format"])))

    if row.get("duration"):
        g.add((renzi_interview_2000, schema.duration, Literal(row["duration"])))

    # --- RIGHTS, DESCRIPTION, NOTES ---

    if row.get("rights"):
        g.add((renzi_interview_2000, dcterms.rights, Literal(row["rights"])))

    if row.get("description"):
        if language:
            g.add((renzi_interview_2000, dcterms.description, Literal(row["description"], lang=language)))
        else:
            g.add((renzi_interview_2000, dcterms.description, Literal(row["description"])))

    if row.get("notes"):
        g.add((renzi_interview_2000, rdfs.comment, Literal(row["notes"])))

    # --- INSTITUTION, COLLECTION, LOCATION ---

    # Holding institution
    g.add((cineteca_di_bologna, RDF.type, FOAF.Organization))
    if row.get("institution"):
        g.add((cineteca_di_bologna, FOAF.name, Literal(row["institution"])))
        g.add((renzi_interview_2000, schema.sourceOrganization, cineteca_di_bologna))

    if row.get("institution_uri"):
        g.add((cineteca_di_bologna, OWL.sameAs, URIRef(row["institution_uri"])))

    # Collection
    g.add((renzo_renzi_collection, RDF.type, schema.Collection))
    if row.get("collection"):
        g.add((renzo_renzi_collection, schema.name, Literal(row["collection"])))
        g.add((renzi_interview_2000, dcterms.isPartOf, renzo_renzi_collection))

    if row.get("collection_uri"):
        g.add((renzo_renzi_collection, OWL.sameAs, URIRef(row["collection_uri"])))

    # Current location
    if row.get("current_location"):
        g.add((renzi_interview_2000, schema.location, Literal(row["current_location"])))

    # --- LANGUAGE ---

    if language:
        g.add((renzi_interview_2000, dc.language, Literal(language)))


# ===================== SERIALIZATION =====================

g.serialize(format="turtle", destination="../ttl/renzi_interview_2000.ttl")

print("CSV converted to TTL!")
