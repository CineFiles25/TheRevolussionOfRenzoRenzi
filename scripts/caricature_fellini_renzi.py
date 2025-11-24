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
    "fiaf": fiaf,
}


def graph_bindings():
    """Bind all namespaces to the RDF graph."""
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g


# ===================== LOCAL ENTITIES =====================

# Main resource: Renzo Renzi's caricature of Federico Fellini
caricature_fellini_renzi = URIRef(rrr + "caricature_fellini_renzi")

# Persons involved
renzo_renzi = URIRef(rrr + "renzo_renzi")
federico_fellini = URIRef(rrr + "federico_fellini")

# Holding institution and collection
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzo_renzi_collection = URIRef(rrr + "renzo_renzi_collection")

# ===================== READ CSV =====================

caricature_df = pd.read_csv(
    "../csv/caricature_renzi_fellini.csv",
    keep_default_na=False,
    encoding="utf-8"
)

g = graph_bindings()

# ===================== MAP CSV → RDF =====================

for idx, row in caricature_df.iterrows():
    # Language tag (e.g. "it")
    language = str(row["language"]).strip() if "language" in row and str(row["language"]).strip() else None

    # --- TYPES FOR THE MAIN RESOURCE ---

    # The caricature is a drawing and a visual artwork related to film culture
    g.add((caricature_fellini_renzi, RDF.type, schema.VisualArtwork))
    g.add((caricature_fellini_renzi, RDF.type, fiaf.FilmRelatedObject))

    # Optional more specific resource type as literal (e.g. "Drawing")
    if row.get("resource_type"):
        g.add((caricature_fellini_renzi, dcterms.type, Literal(row["resource_type"])))

    # Object type as a human-readable category (e.g. "Drawing / caricature")
    if row.get("object_type"):
        g.add((caricature_fellini_renzi, schema.additionalType, Literal(row["object_type"])))

    # --- IDENTIFIERS AND STANDARDS ---

    # Local identifier
    if row.get("id"):
        g.add((caricature_fellini_renzi, dc.identifier, Literal(row["id"])))

    # Descriptive / cataloguing standard
    if row.get("standard"):
        g.add((caricature_fellini_renzi, dcterms.conformsTo, Literal(row["standard"])))

    # --- TITLE AND INSCRIPTION ---

    # Title of the caricature
    if row.get("title"):
        if language:
            g.add((caricature_fellini_renzi, dc.title, Literal(row["title"], lang=language)))
        else:
            g.add((caricature_fellini_renzi, dc.title, Literal(row["title"])))

    # Handwritten inscription on the drawing
    if row.get("inscription"):
        if language:
            g.add((caricature_fellini_renzi, schema.inscription, Literal(row["inscription"], lang=language)))
        else:
            g.add((caricature_fellini_renzi, schema.inscription, Literal(row["inscription"])))

    # --- CREATOR AND DEPICTED PERSON ---

    # Local typing for persons
    g.add((renzo_renzi, RDF.type, FOAF.Person))
    g.add((federico_fellini, RDF.type, FOAF.Person))

    # Creator: Renzo Renzi
    if row.get("creator"):
        g.add((renzo_renzi, FOAF.name, Literal(row["creator"])))
        g.add((caricature_fellini_renzi, dc.creator, renzo_renzi))

    # Depicted person: Federico Fellini
    if row.get("depicted_person"):
        g.add((federico_fellini, FOAF.name, Literal(row["depicted_person"])))
        # The drawing visually depicts Fellini
        g.add((caricature_fellini_renzi, FOAF.depicts, federico_fellini))

    # External URIs (VIAF or other authority files)
    if row.get("creator_uri"):
        g.add((renzo_renzi, OWL.sameAs, URIRef(row["creator_uri"])))

    if row.get("depicted_person_uri"):
        g.add((federico_fellini, OWL.sameAs, URIRef(row["depicted_person_uri"])))

    # --- CREATION, TECHNIQUE, MATERIAL, DIMENSIONS ---

    # Creation date (kept as a free-text literal because it is approximate)
    if row.get("creation_date"):
        g.add((caricature_fellini_renzi, dcterms.created, Literal(row["creation_date"])))

    # Artistic technique (e.g. ink, markers)
    if row.get("technique"):
        g.add((caricature_fellini_renzi, schema.artMedium, Literal(row["technique"])))

    # Material support (e.g. cut paper)
    if row.get("material"):
        g.add((caricature_fellini_renzi, schema.material, Literal(row["material"])))

    # Physical dimensions (height, width, etc.)
    if row.get("dimensions"):
        g.add((caricature_fellini_renzi, dcterms.extent, Literal(row["dimensions"])))

    # --- INSTITUTION, COLLECTION, LOCATION ---

    # Holding institution (Cineteca di Bologna)
    g.add((cineteca_di_bologna, RDF.type, FOAF.Organization))
    if row.get("institution"):
        g.add((cineteca_di_bologna, FOAF.name, Literal(row["institution"])))
        # The caricature is held by / associated with this institution
        g.add((caricature_fellini_renzi, schema.sourceOrganization, cineteca_di_bologna))

    if row.get("institution_uri"):
        g.add((cineteca_di_bologna, OWL.sameAs, URIRef(row["institution_uri"])))

    # Collection (Renzo Renzi Collection)
    g.add((renzo_renzi_collection, RDF.type, schema.Collection))
    if row.get("collection"):
        g.add((renzo_renzi_collection, schema.name, Literal(row["collection"])))
        # The caricature is part of this collection
        g.add((caricature_fellini_renzi, dcterms.isPartOf, renzo_renzi_collection))

    if row.get("collection_uri"):
        g.add((renzo_renzi_collection, OWL.sameAs, URIRef(row["collection_uri"])))

    # Current location (e.g. inventory or storage location)
    if row.get("current_location"):
        g.add((caricature_fellini_renzi, schema.location, Literal(row["current_location"])))

    # --- RIGHTS AND DESCRIPTIVE FIELDS ---

    # Rights statement for the object (e.g. all rights reserved)
    if row.get("rights"):
        g.add((caricature_fellini_renzi, dcterms.rights, Literal(row["rights"])))

    # Short description of the caricature
    if row.get("description"):
        if language:
            g.add((caricature_fellini_renzi, dcterms.description, Literal(row["description"], lang=language)))
        else:
            g.add((caricature_fellini_renzi, dcterms.description, Literal(row["description"])))

    # Additional notes about the object or the project
    if row.get("notes"):
        g.add((caricature_fellini_renzi, rdfs.comment, Literal(row["notes"])))

    # Language of the main textual content (e.g. inscription, title)
    if language:
        g.add((caricature_fellini_renzi, dc.language, Literal(language)))


# ===================== SERIALIZATION =====================

g.serialize(format="turtle", destination="../ttl/caricature_renzi_fellini.ttl")

print("CSV converted to TTL!")
