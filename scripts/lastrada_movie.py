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

# Main audiovisual resource: the original soundtrack of "La Strada"
la_strada_soundtrack = URIRef(rrr + "la_strada_soundtrack_original")

# Composer (from the CSV)
nino_rota = URIRef(rrr + "nino_rota")

# Film it belongs to
la_strada_film = URIRef(rrr + "la_strada_1954")

# Institution and collection (likely identical to other items)
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzo_renzi_collection = URIRef(rrr + "renzo_renzi_collection")

# ===================== READ CSV =====================

soundtrack_df = pd.read_csv(
    "../csv/la_strada_soundtrack_original.csv",
    keep_default_na=False,
    encoding="utf-8"
)

g = graph_bindings()

# ===================== MAP CSV → RDF =====================

for idx, row in soundtrack_df.iterrows():

    # Language tag if present
    language = str(row["language"]).strip() if "language" in row and str(row["language"]).strip() else None

    # --- TYPE DECLARATIONS ---

    g.add((la_strada_soundtrack, RDF.type, schema.MusicRecording))
    g.add((la_strada_soundtrack, RDF.type, schema.CreativeWork))
    g.add((la_strada_soundtrack, RDF.type, fiaf.FilmRelatedObject))

    # --- IDENTIFIER ---

    if row.get("id"):
        g.add((la_strada_soundtrack, dc.identifier, Literal(row["id"])))

    # Descriptive standard (e.g., ISBD, local cataloguing rule)
    if row.get("standard"):
        g.add((la_strada_soundtrack, dcterms.conformsTo, Literal(row["standard"])))

    # --- TITLE ---

    if row.get("title"):
        if language:
            g.add((la_strada_soundtrack, dc.title, Literal(row["title"], lang=language)))
        else:
            g.add((la_strada_soundtrack, dc.title, Literal(row["title"])))

    # --- COMPOSER ---

    g.add((nino_rota, RDF.type, FOAF.Person))

    if row.get("composer"):
        g.add((nino_rota, FOAF.name, Literal(row["composer"])))
        g.add((la_strada_soundtrack, schema.creator, nino_rota))

    if row.get("composer_uri"):
        g.add((nino_rota, OWL.sameAs, URIRef(row["composer_uri"])))

    # --- FILM RELATION ---

    # The soundtrack is about the 1954 film "La Strada"
    g.add((la_strada_film, RDF.type, schema.Movie))

    if row.get("related_work"):
        g.add((la_strada_film, dc.title, Literal(row["related_work"])))
        g.add((la_strada_soundtrack, schema.about, la_strada_film))

    if row.get("related_work_uri"):
        g.add((la_strada_film, OWL.sameAs, URIRef(row["related_work_uri"])))

    # Optional relation type literal
    if row.get("work_relation_type"):
        g.add((la_strada_soundtrack, dcterms.relation, Literal(row["work_relation_type"])))

    # --- PUBLICATION, PRODUCTION, YEAR ---

    if row.get("release_year"):
        g.add((la_strada_soundtrack,
               schema.datePublished,
               Literal(str(row["release_year"]), datatype=XSD.gYear)))

    # --- SOUNDTRACK TYPE (e.g., original soundtrack, reissue, etc.) ---

    if row.get("soundtrack_type"):
        g.add((la_strada_soundtrack, schema.additionalType, Literal(row["soundtrack_type"])))

    # --- PUBLISHER OR LABEL ---

    if row.get("publisher"):
        label = URIRef(rrr + "label_" + row["publisher"].replace(" ", "_").lower())
        g.add((label, RDF.type, FOAF.Organization))
        g.add((label, FOAF.name, Literal(row["publisher"])))
        g.add((la_strada_soundtrack, dcterms.publisher, label))

    if row.get("publisher_uri"):
        g.add((label, OWL.sameAs, URIRef(row["publisher_uri"])))

    # --- FORMAT ---

    if row.get("format"):
        g.add((la_strada_soundtrack, schema.encodingFormat, Literal(row["format"])))

    # --- DESCRIPTION AND NOTES ---

    if row.get("description"):
        if language:
            g.add((la_strada_soundtrack, dcterms.description, Literal(row["description"], lang=language)))
        else:
            g.add((la_strada_soundtrack, dcterms.description, Literal(row["description"])))

    if row.get("notes"):
        g.add((la_strada_soundtrack, rdfs.comment, Literal(row["notes"])))

    # --- RIGHTS ---

    if row.get("rights"):
        g.add((la_strada_soundtrack, dcterms.rights, Literal(row["rights"])))

    # --- COLLECTION AND INSTITUTION ---

    # Holding institution
    g.add((cineteca_di_bologna, RDF.type, FOAF.Organization))
    if row.get("institution"):
        g.add((cineteca_di_bologna, FOAF.name, Literal(row["institution"])))
        g.add((la_strada_soundtrack, schema.sourceOrganization, cineteca_di_bologna))

    if row.get("institution_uri"):
        g.add((cineteca_di_bologna, OWL.sameAs, URIRef(row["institution_uri"])))

    # Collection (Renzo Renzi Collection)
    g.add((renzo_renzi_collection, RDF.type, schema.Collection))
    if row.get("collection"):
        g.add((renzo_renzi_collection, schema.name, Literal(row["collection"])))
        g.add((la_strada_soundtrack, dcterms.isPartOf, renzo_renzi_collection))

    if row.get("collection_uri"):
        g.add((renzo_renzi_collection, OWL.sameAs, URIRef(row["collection_uri"])))

    # Current location (inventory / archive location)
    if row.get("current_location"):
        g.add((la_strada_soundtrack, schema.location, Literal(row["current_location"])))

    # --- LANGUAGE ---

    if language:
        g.add((la_strada_soundtrack, dc.language, Literal(language)))


# ===================== SERIALIZATION =====================

g.serialize(format="turtle", destination="../ttl/la_strada_soundtrack_original.ttl")

print("CSV converted to TTL!")
