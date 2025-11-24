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

# Main resource: photograph "photo_lastrada_01"
photo_lastrada_01 = URIRef(rrr + "photo_lastrada_01")

# People
federico_fellini = URIRef(rrr + "federico_fellini")
giulietta_masina = URIRef(rrr + "giulietta_masina")
photographer_res = URIRef(rrr + "libero_grandi")  # main photographer

# Event, place, related film
lastrada_premiere_event = URIRef(rrr + "la_strada_premiere_1954")
cinema_fulgor = URIRef(rrr + "cinema_fulgor")
la_strada_film = URIRef(rrr + "la_strada_1954")

# Institution and collection
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
renzo_renzi_collection = URIRef(rrr + "renzo_renzi_collection")

# ===================== READ CSV =====================

photo_df = pd.read_csv(
    "../csv/photo_lastrada_01.csv",
    keep_default_na=False,
    encoding="utf-8"
)

g = graph_bindings()

# ===================== MAP CSV → RDF =====================

for idx, row in photo_df.iterrows():

    # Language tag (e.g. "en", "it")
    language = str(row["language"]).strip() if "language" in row and str(row["language"]).strip() else None

    # --- TYPES FOR THE MAIN RESOURCE ---

    g.add((photo_lastrada_01, RDF.type, schema.Photograph))
    g.add((photo_lastrada_01, RDF.type, schema.ImageObject))
    g.add((photo_lastrada_01, RDF.type, fiaf.FilmRelatedObject))

    # Optional resource type as a literal (e.g. "Photograph")
    if row.get("resource_type"):
        g.add((photo_lastrada_01, dcterms.type, Literal(row["resource_type"])))

    # --- IDENTIFIERS AND STANDARD ---

    # Local identifier
    if row.get("id"):
        g.add((photo_lastrada_01, dc.identifier, Literal(row["id"])))

    # Additional identifiers (e.g. internal codes)
    if row.get("identifiers"):
        g.add((photo_lastrada_01, dc.identifier, Literal(row["identifiers"])))

    # Descriptive / cataloguing standard (e.g. "Scheda F")
    if row.get("standard"):
        g.add((photo_lastrada_01, dcterms.conformsTo, Literal(row["standard"])))

    # --- TITLE AND OTHER TITLE INFORMATION ---

    if row.get("title"):
        if language:
            g.add((photo_lastrada_01, dc.title, Literal(row["title"], lang=language)))
        else:
            g.add((photo_lastrada_01, dc.title, Literal(row["title"])))

    if row.get("other_title_information"):
        if language:
            g.add((photo_lastrada_01, dcterms.alternative, Literal(row["other_title_information"], lang=language)))
        else:
            g.add((photo_lastrada_01, dcterms.alternative, Literal(row["other_title_information"])))

    # --- PHOTOGRAPHER ---

    g.add((photographer_res, RDF.type, FOAF.Person))

    if row.get("photographer"):
        g.add((photographer_res, FOAF.name, Literal(row["photographer"])))
        g.add((photo_lastrada_01, dc.creator, photographer_res))

    if row.get("photographer_uri"):
        g.add((photographer_res, OWL.sameAs, URIRef(row["photographer_uri"])))

    # --- DEPICTED PEOPLE ---

    # Local typing for depicted persons
    g.add((federico_fellini, RDF.type, FOAF.Person))
    g.add((giulietta_masina, RDF.type, FOAF.Person))

    # Names from CSV
    if row.get("depicted_people"):
        people_names = [name.strip() for name in str(row["depicted_people"]).split(";") if name.strip()]
        local_people = [federico_fellini, giulietta_masina]

        for local_res, name in zip(local_people, people_names):
            g.add((local_res, FOAF.name, Literal(name)))
            g.add((photo_lastrada_01, FOAF.depicts, local_res))

    # External URIs for depicted people (VIAF, Wikidata, etc.)
    if row.get("depicted_people_uri"):
        people_uris = [uri.strip() for uri in str(row["depicted_people_uri"]).split(";") if uri.strip()]
        local_people = [federico_fellini, giulietta_masina]

        for local_res, uri in zip(local_people, people_uris):
            g.add((local_res, OWL.sameAs, URIRef(uri)))

    # --- DEPICTED EVENT ---

    g.add((lastrada_premiere_event, RDF.type, schema.Event))

    if row.get("depicted_event"):
        if language:
            g.add((lastrada_premiere_event, schema.name, Literal(row["depicted_event"], lang=language)))
        else:
            g.add((lastrada_premiere_event, schema.name, Literal(row["depicted_event"])))

        # The photograph depicts this event
        g.add((photo_lastrada_01, schema.about, lastrada_premiere_event))

    if row.get("depicted_event_uri"):
        g.add((lastrada_premiere_event, OWL.sameAs, URIRef(row["depicted_event_uri"])))

    # --- DEPICTED PLACE ---

    g.add((cinema_fulgor, RDF.type, schema.Place))

    if row.get("depicted_place"):
        if language:
            g.add((cinema_fulgor, schema.name, Literal(row["depicted_place"], lang=language)))
        else:
            g.add((cinema_fulgor, schema.name, Literal(row["depicted_place"])))

        # The photograph is associated with this place
        g.add((photo_lastrada_01, schema.locationCreated, cinema_fulgor))

    if row.get("depicted_place_uri"):
        g.add((cinema_fulgor, OWL.sameAs, URIRef(row["depicted_place_uri"])))

    # --- CREATION YEAR AND COLOUR ---

    if row.get("creation_year"):
        g.add(
            (
                photo_lastrada_01,
                schema.dateCreated,
                Literal(str(row["creation_year"]), datatype=XSD.gYear)
            )
        )

    if row.get("colour"):
        # "Black and white" or similar information
        g.add((photo_lastrada_01, schema.color, Literal(row["colour"])))

    # --- DIMENSIONS, MATERIAL, CARRIER TYPE, PHYSICAL DESCRIPTION ---

    if row.get("dimensions"):
        g.add((photo_lastrada_01, dcterms.extent, Literal(row["dimensions"])))

    if row.get("material_technique"):
        # Technique and material used in the photographic print
        g.add((photo_lastrada_01, schema.artMedium, Literal(row["material_technique"])))

    if row.get("carrier_type"):
        # Type of carrier / support (e.g. photographic print)
        g.add((photo_lastrada_01, schema.additionalType, Literal(row["carrier_type"])))

    if row.get("physical_description"):
        if language:
            g.add((photo_lastrada_01, dcterms.description, Literal(row["physical_description"], lang=language)))
        else:
            g.add((photo_lastrada_01, dcterms.description, Literal(row["physical_description"])))

    # Inventory number
    if row.get("inventory_number"):
        g.add((photo_lastrada_01, schema.identifier, Literal(row["inventory_number"])))

    # --- INSTITUTION, COLLECTION, CURRENT LOCATION ---

    # Institution: Cineteca di Bologna
    g.add((cineteca_di_bologna, RDF.type, FOAF.Organization))
    if row.get("institution"):
        g.add((cineteca_di_bologna, FOAF.name, Literal(row["institution"])))
        g.add((photo_lastrada_01, schema.sourceOrganization, cineteca_di_bologna))

    if row.get("institution_uri"):
        g.add((cineteca_di_bologna, OWL.sameAs, URIRef(row["institution_uri"])))

    # Collection: Renzo Renzi Collection
    g.add((renzo_renzi_collection, RDF.type, schema.Collection))
    if row.get("collection"):
        g.add((renzo_renzi_collection, schema.name, Literal(row["collection"])))
        g.add((photo_lastrada_01, dcterms.isPartOf, renzo_renzi_collection))

    if row.get("collection_uri"):
        g.add((renzo_renzi_collection, OWL.sameAs, URIRef(row["collection_uri"])))

    # Current location (e.g. store, shelf, box)
    if row.get("current_location"):
        g.add((photo_lastrada_01, schema.location, Literal(row["current_location"])))

    # --- RELATED WORKS (THE FILM "LA STRADA") ---

    g.add((la_strada_film, RDF.type, schema.Movie))

    if row.get("related_works"):
        # e.g. "la_strada_film"
        g.add((la_strada_film, dc.title, Literal(row["related_works"])))
        g.add((photo_lastrada_01, schema.about, la_strada_film))

    if row.get("related_works_uri"):
        g.add((la_strada_film, OWL.sameAs, URIRef(row["related_works_uri"])))

    # --- RIGHTS, NOTES, LANGUAGE ---

    if row.get("rights"):
        g.add((photo_lastrada_01, dcterms.rights, Literal(row["rights"])))

    if row.get("notes"):
        g.add((photo_lastrada_01, rdfs.comment, Literal(row["notes"])))

    if language:
        g.add((photo_lastrada_01, dc.language, Literal(language)))


# ===================== SERIALIZATION =====================

g.serialize(format="turtle", destination="../ttl/photo_lastrada_01.ttl")

print("CSV converted to TTL!")
