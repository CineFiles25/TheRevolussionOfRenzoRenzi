from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

# GRAPH
g = Graph()

# Bindings
g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)
g.bind("dc", dc)
g.bind("crm", crm)

# ENTITIES
library = URIRef(rrr + "renzo_renzi_library")
renzi = URIRef(rrr + "renzo_renzi")
cineteca = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
renzi_collection = URIRef(rrr + "renzi_collection")
guida_screenplay = URIRef(rrr + "guida_per_camminare_all_ombra")
book_il_primo_fellini = URIRef(rrr + "book_il_primo_fellini")

# LOAD CSV
df = read_csv("../csv/renzi_library.csv", keep_default_na=False, encoding="utf-8")

# RESOURCE TYPE
g.add((library, RDF.type, schema.Library))

# CSV → RDF MAPPING
for _, row in df.iterrows():

    # Identifier (ISIL)
    if row.get("id_isil"):
        g.add((library, dcterms.identifier, Literal(row["id_isil"])))

    # Name and alternative name
    if row.get("name"):
        g.add((library, schema.name, Literal(row["name"])))

    if row.get("alt_title"):
        g.add((library, schema.alternateName, Literal(row["alt_title"])))

    # Original function (literal)
    if row.get("original_function"):
        g.add((library, dcterms.description, Literal(row["original_function"])))

    # Opening hours
    if row.get("opening_hours"):
        g.add((library, schema.openingHours, Literal(row["opening_hours"])))

    # Ownership
    g.add((library, crm.P52_has_current_owner, cineteca))

    # Completion year
    if row.get("completion_year"):
        g.add((library, schema.dateCreated, Literal(row["completion_year"], datatype=XSD.gYear)))

    # Foundation year
    if row.get("foundation_year"):
        g.add((library, schema.foundingDate, Literal(row["foundation_year"], datatype=XSD.gYear)))

    # Address
    if row.get("address"):
        g.add((library, schema.address, Literal(row["address"])))

    # City (resource)
    g.add((library, schema.addressLocality, bologna))

    # Coordinates
    if row.get("coordinates"):
        g.add((library, schema.geo, Literal(row["coordinates"])))

    # Website
    if row.get("website"):
        g.add((library, schema.url, Literal(row["website"])))

    # Email
    if row.get("email"):
        g.add((library, schema.email, Literal(row["email"])))

    # Phone
    if row.get("phone_number"):
        g.add((library, schema.telephone, Literal(row["phone_number"])))

    # Accessibility
    if row.get("accessible"):
        g.add((library, schema.isAccessibleForFree, Literal(row["accessible"], datatype=XSD.boolean)))

    # Structure type
    if row.get("structure_type"):
        g.add((library, dcterms.description, Literal(row["structure_type"])))

    # Area
    if row.get("area"):
        g.add((library, schema.floorSize, Literal(row["area"])))

    # Seats
    if row.get("seats"):
        g.add((library, schema.seatingCapacity, Literal(row["seats"], datatype=XSD.integer)))

    # Audio system
    if row.get("audio_system"):
        g.add((library, dcterms.description, Literal(row["audio_system"])))

    # Video system
    if row.get("video_system"):
        g.add((library, dcterms.description, Literal(row["video_system"])))

    # Dedication
    g.add((library, schema.dedicatedTo, renzi))

    # ITEMS LOCATED IN THE LIBRARY
    g.add((guida_screenplay, schema.location, library))
    g.add((book_il_primo_fellini, schema.location, library))
    g.add((renzi_collection, schema.location, library))

    # Collection metadata
    g.add((renzi_collection, dcterms.isPartOf, library))
    g.add((renzi_collection, crm.P52_has_current_owner, cineteca))


# SERIALIZATION
g.serialize(format="turtle", destination="../ttl/renzi_library.ttl")
print("renzi_library.ttl generated successfully!")
