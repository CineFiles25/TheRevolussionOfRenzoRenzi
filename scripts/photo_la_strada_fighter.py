import pandas as pd
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD

# ============================================
# NAMESPACES
# ============================================

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
sf  = Namespace("https://iccd.beniculturali.it/scheda-f/")
dct = Namespace("http://purl.org/dc/terms/")
dc  = Namespace("http://purl.org/dc/elements/1.1/")
owl = Namespace("http://www.w3.org/2002/07/owl#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# ============================================
# GRAPH CREATION
# ============================================

g = Graph()

ns_dict = {
    "rrr": rrr,
    "sf": sf,
    "dct": dct,
    "dc": dc,
    "owl": owl,
    "xsd": xsd,
}

def graph_bindings():
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

g = graph_bindings()

# ============================================
# ENTITIES（fixed instance，name it manunally）
# ============================================

photo = URIRef(rrr + "photo_la_strada_fighter")

# or if there's a need, we can:
# renzo_renzi = URIRef(rrr + "renzo_renzi")
# bologna = URIRef(rrr + "bologna")
# bind with dct:subject / dct:spatial below

# ============================================
# CSV FROM GITHUB
# ============================================

GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/"
    "CineFiles25/TheRevolussionOfRenzoRenzi/refs/heads/main/"
    "csv/photo_la_strada_fighter.csv"
)

photo_df = pd.read_csv(GITHUB_CSV_URL, keep_default_na=False, encoding="utf-8")

# ============================================
# MAPPING（ultra-simple）
# ============================================

for idx, row in photo_df.iterrows():
    # Class：in Scheda F we consider my photo as an instance as sf:Photograph
    g.add((photo, RDF.type, sf.Photograph))

    # ---- （Literal） ----
    if row["standard"]:
        g.add((photo, sf.standard, Literal(row["standard"])))

    if row["title"]:
        g.add((photo, dct.title, Literal(row["title"])))

    if row["other_title_information"]:
        g.add((photo, dct.alternative, Literal(row["other_title_information"])))

    if row["photographer"]:
        g.add((photo, dct.creator, Literal(row["photographer"])))

    if row["depicted_event"]:
        g.add((photo, dct.subject, Literal(row["depicted_event"])))

    if row["depicted_people"]:
        g.add((photo, dct.subject, Literal(row["depicted_people"])))

    if row["depicted_place"]:
        g.add((photo, dct.spatial, Literal(row["depicted_place"])))

    if row["creation_year"]:
        g.add((photo, dct.created, Literal(row["creation_year"], datatype=XSD.gYear)))

    if row["colour"]:
        g.add((photo, sf.colour, Literal(row["colour"])))

    if row["material_technique"]:
        g.add((photo, dct.medium, Literal(row["material_technique"])))

    if row["inventory_number"]:
        g.add((photo, sf.inventoryNumber, Literal(row["inventory_number"])))

    if row["collection"]:
        g.add((photo, dct.isPartOf, Literal(row["collection"])))

    if row["carrier_type"]:
        g.add((photo, sf.carrierType, Literal(row["carrier_type"])))

    if row["physical_description"]:
        g.add((photo, dct.extent, Literal(row["physical_description"])))

    if row["notes"]:
        g.add((photo, dct.description, Literal(row["notes"])))

    if row["identifiers"]:
        g.add((photo, dct.identifier, Literal(row["identifiers"])))

    if row["related_works"]:
        g.add((photo, sf.relatedWork, Literal(row["related_works"])))

    if row["rights"]:
        g.add((photo, dct.rights, Literal(row["rights"])))

    if row["resource_type"]:
        g.add((photo, dct.type, Literal(row["resource_type"])))

    if row["language"]:
        g.add((photo, dct.language, Literal(row["language"])))

    # ---- URI property（instance link to URI，without authority file linked） ----
    if row["photographer_uri"]:
        g.add((photo, sf.photographerRef, URIRef(row["photographer_uri"])))

    if row["depicted_people_uri"]:
        g.add((photo, sf.depictedPersonRef, URIRef(row["depicted_people_uri"])))

    if row["depicted_event_uri"]:
        g.add((photo, sf.depictedEventRef, URIRef(row["depicted_event_uri"])))

    if row["depicted_place_uri"]:
        g.add((photo, sf.depictedPlaceRef, URIRef(row["depicted_place_uri"])))

    if row["related_works_uri"]:
        g.add((photo, sf.relatedWorkRef, URIRef(row["related_works_uri"])))

# ============================================
# SERIALIZATION
# ============================================

g.serialize(format="turtle", destination="photo_lastrada_05_fighter.ttl")
print("CSV from GitHub converted to TTL: photo_lastrada_05_fighter.ttl")
