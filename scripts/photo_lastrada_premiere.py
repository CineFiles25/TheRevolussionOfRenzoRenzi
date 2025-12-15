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

premiere_photo = URIRef(rrr + "photo_lastrada_premiere")
la_strada_film = URIRef(rrr + "la_strada_film")
federico_fellini = URIRef(rrr + "federico_fellini")
giulietta_masina = URIRef(rrr + "giulietta_masina")
cinema_fulgor = URIRef(rrr + "cinema_fulgor")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")
renzi_collection = URIRef(rrr + "renzi_collection")

# Base types
g.add((premiere_photo, RDF.type, schema.Photograph))
g.add((schema.Photograph, RDFS.subClassOf, schema.CreativeWork))

g.add((federico_fellini, RDF.type, foaf.Person))
g.add((giulietta_masina, RDF.type, foaf.Person))
g.add((bologna, RDF.type, schema.Place))
g.add((cineteca_di_bologna, RDF.type, schema.Organization))
g.add((cinema_fulgor, RDF.type, schema.MovieTheater))
g.add((renzi_collection, RDF.type, dcterms.Collection))
g.add((la_strada_film, RDF.type, schema.Movie))

# Authority links
g.add((la_strada_film, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))
g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((giulietta_masina, OWL.sameAs, URIRef("http://viaf.org/viaf/37021297")))
g.add((cinema_fulgor, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q36839368")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# CSV LOADING
# N.B. run this script from the `scripts/` directory

photo_df = read_csv(
    "../csv/photo_lastrada_premiere.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# MAPPING TO RDF

for _, row in photo_df.iterrows():

    # IDENTIFIERS, STANDARD, TYPE

    if row.get("id"):
        g.add((premiere_photo, dcterms.identifier, Literal(row["id"])))

    if row.get("identifiers"):
        for ident in [i.strip() for i in row["identifiers"].split(";") if i.strip()]:
            g.add((premiere_photo, dcterms.identifier, Literal(ident)))

    if row.get("standard"):
        g.add((premiere_photo, dcterms.conformsTo, Literal(row["standard"])))

    if row.get("resource_type"):
        g.add((premiere_photo, dcterms.type, Literal(row["resource_type"])))

    # TITLES AND DESCRIPTION

    if row.get("title"):
        g.add((premiere_photo, dcterms.title, Literal(row["title"])))

    if row.get("other_title_information"):
        g.add((premiere_photo, schema.alternateName, Literal(row["other_title_information"])))

    if row.get("notes"):
        g.add((premiere_photo, dcterms.description, Literal(row["notes"])))

    # CREATOR AND DEPICTED SUBJECTS

    if row.get("creator"):
        g.add((premiere_photo, dcterms.creator, Literal(row["creator"])))

    g.add((premiere_photo, foaf.depicts, federico_fellini))
    g.add((premiere_photo, foaf.depicts, giulietta_masina))

    if row.get("depicted_people"):
        g.add((premiere_photo, dc.subject, Literal(row["depicted_people"])))

    if row.get("depicted_people_uri"):
        for uri_str in [u.strip() for u in row["depicted_people_uri"].split("|") if u.strip()]:
            g.add((premiere_photo, dcterms.relation, Literal(uri_str, datatype=XSD.anyURI)))

    if row.get("depicted_event"):
        g.add((premiere_photo, dc.subject, Literal(row["depicted_event"])))

    if row.get("depicted_event_uri"):
        g.add((premiere_photo, dcterms.relation, Literal(row["depicted_event_uri"], datatype=XSD.anyURI)))

    if row.get("depicted_place"):
        g.add((premiere_photo, schema.locationCreated, Literal(row["depicted_place"])))

    g.add((premiere_photo, schema.contentLocation, cinema_fulgor))
    g.add((cinema_fulgor, schema.location, bologna))

    if row.get("depicted_place_uri"):
        g.add((premiere_photo, dcterms.relation, Literal(row["depicted_place_uri"], datatype=XSD.anyURI)))

    # CREATION / TECHNIQUE / PHYSICAL DESC

    if row.get("creation_year"):
        g.add((premiere_photo, dcterms.created, Literal(row["creation_year"], datatype=XSD.gYear)))

    if row.get("colour"):
        g.add((premiere_photo, schema.color, Literal(row["colour"])))

    if row.get("material_technique"):
        g.add((premiere_photo, dcterms.medium, Literal(row["material_technique"])))

    if row.get("carrier_type"):
        g.add((premiere_photo, dcterms.medium, Literal(row["carrier_type"])))

    if row.get("physical_description"):
        g.add((premiere_photo, dcterms.extent, Literal(row["physical_description"])))

    if row.get("inventory_number"):
        g.add((premiere_photo, dcterms.identifier, Literal(row["inventory_number"])))

    # INSTITUTION / COLLECTION / RIGHTS

    g.add((premiere_photo, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((renzi_collection, dcterms.hasPart, premiere_photo))

    if row.get("collection"):
        g.add((renzi_collection, dcterms.title, Literal(row["collection"])))

    if row.get("institution"):
        g.add((premiere_photo, dcterms.publisher, Literal(row["institution"])))

    if row.get("institution_uri"):
        g.add((premiere_photo, dcterms.relation, Literal(row["institution_uri"], datatype=XSD.anyURI)))

    if row.get("collection_uri"):
        for uri_str in [u.strip() for u in row["collection_uri"].split("|") if u.strip()]:
            g.add((premiere_photo, dcterms.relation, Literal(uri_str, datatype=XSD.anyURI)))

    if row.get("rights"):
        g.add((premiere_photo, dcterms.rights, Literal(row["rights"])))

    # RELATED WORKS (FILM "LA STRADA")

    if row.get("related_works"):
        for work_id in [w.strip() for w in row["related_works"].split(";") if w.strip()]:
            related_uri = URIRef(rrr + work_id)
            g.add((premiere_photo, dcterms.relation, related_uri))

    g.add((premiere_photo, dcterms.relation, la_strada_film))
    g.add((premiere_photo, schema.about, la_strada_film))

    if row.get("related_works_uri"):
        g.add((premiere_photo, dcterms.relation, Literal(row["related_works_uri"], datatype=XSD.anyURI)))

    # LANGUAGE

    if row.get("language"):
        g.add((premiere_photo, schema.inLanguage, Literal(row["language"])))


# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/photo_lastrada_premiere.ttl")
print("CSV converted to TTL!")
