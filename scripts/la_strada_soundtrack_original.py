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

la_strada_soundtrack = URIRef(rrr + "la_strada_soundtrack_original")
la_strada_film = URIRef(rrr + "la_strada_film")
nino_rota = URIRef(rrr + "nino_rota")

# Base types
g.add((la_strada_film, RDF.type, schema.Movie))
g.add((schema.MusicRecording, RDFS.subClassOf, schema.CreativeWork))
g.add((nino_rota, RDF.type, foaf.Person))

# Authority links
g.add((nino_rota, OWL.sameAs, URIRef("http://viaf.org/viaf/88980189")))
g.add((la_strada_film, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))

# CSV LOADING
# N.B. run this script from the `scripts/` directory

soundtrack_df = read_csv(
    "../csv/la_strada_soundtrack_original.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# MAPPING TO RDF

for _, row in soundtrack_df.iterrows():

    g.add((la_strada_soundtrack, RDF.type, schema.MusicRecording))

    # Identifier(s) and standard
    if row.get("id"):
        g.add((la_strada_soundtrack, dcterms.identifier, Literal(row["id"])))
    if row.get("identifiers"):
        g.add((la_strada_soundtrack, dcterms.identifier, Literal(row["identifiers"])))
    if row.get("standard"):
        g.add((la_strada_soundtrack, dcterms.conformsTo, Literal(row["standard"])))

    # Titles
    if row.get("title"):
        g.add((la_strada_soundtrack, dcterms.title, Literal(row["title"])))
    if row.get("other_title_information"):
        g.add((la_strada_soundtrack, schema.alternateName, Literal(row["other_title_information"])))

    # Responsibility statement as description
    if row.get("responsibility_statement"):
        g.add((la_strada_soundtrack, dcterms.description, Literal(row["responsibility_statement"])))

    # COMPOSER AND PERFORMERS

    if row.get("composer"):
        g.add((la_strada_soundtrack, dcterms.creator, Literal(row["composer"])))

    g.add((la_strada_soundtrack, schema.composer, nino_rota))

    if row.get("composer_uri"):
        g.add((la_strada_soundtrack, dcterms.relation, Literal(row["composer_uri"], datatype=XSD.anyURI)))

    if row.get("performers"):
        g.add((la_strada_soundtrack, dcterms.contributor, Literal(row["performers"])))
        g.add((la_strada_soundtrack, schema.byArtist, Literal(row["performers"])))

    if row.get("performers_uri"):
        g.add((la_strada_soundtrack, dcterms.relation, Literal(row["performers_uri"], datatype=XSD.anyURI)))

    # PUBLICATION DATA

    if row.get("publication_place"):
        g.add((la_strada_soundtrack, dcterms.spatial, Literal(row["publication_place"])))

    if row.get("publisher"):
        g.add((la_strada_soundtrack, dcterms.publisher, Literal(row["publisher"])))
    if row.get("label"):
        g.add((la_strada_soundtrack, schema.publisher, Literal(row["label"])))

    if row.get("publisher_uri"):
        g.add((la_strada_soundtrack, dcterms.relation, Literal(row["publisher_uri"], datatype=XSD.anyURI)))
    if row.get("label_uri"):
        g.add((la_strada_soundtrack, dcterms.relation, Literal(row["label_uri"], datatype=XSD.anyURI)))

    if row.get("catalogue_number"):
        g.add((la_strada_soundtrack, dcterms.identifier, Literal(row["catalogue_number"])))

    # Publication year: keep as string because it may be uncertain (e.g. "1954?")
    if row.get("publication_year"):
        g.add((la_strada_soundtrack, dcterms.issued, Literal(row["publication_year"])))

    if row.get("carrier_type"):
        g.add((la_strada_soundtrack, dcterms.medium, Literal(row["carrier_type"])))
    if row.get("physical_description"):
        g.add((la_strada_soundtrack, dcterms.extent, Literal(row["physical_description"])))

    if row.get("notes"):
        g.add((la_strada_soundtrack, dcterms.description, Literal(row["notes"])))

    # SUBJECTS AND RELATED WORKS

    if row.get("subjects"):
        g.add((la_strada_soundtrack, dc.subject, Literal(row["subjects"])))

    if row.get("related_works"):
        for work_id in [w.strip() for w in row["related_works"].split(";") if w.strip()]:
            related_uri = URIRef(rrr + work_id)
            g.add((la_strada_soundtrack, dcterms.relation, related_uri))

    g.add((la_strada_soundtrack, dcterms.relation, la_strada_film))
    g.add((la_strada_soundtrack, schema.about, la_strada_film))

    if row.get("related_works_uri"):
        g.add((la_strada_soundtrack, dcterms.relation, Literal(row["related_works_uri"], datatype=XSD.anyURI)))

    # RIGHTS / TYPE / LANGUAGE

    if row.get("rights"):
        g.add((la_strada_soundtrack, dcterms.rights, Literal(row["rights"])))

    if row.get("resource_type"):
        g.add((la_strada_soundtrack, dcterms.type, Literal(row["resource_type"])))

    if row.get("language"):
        g.add((la_strada_soundtrack, schema.inLanguage, Literal(row["language"])))


# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/la_strada_soundtrack_original.ttl")
print("CSV converted to TTL!")
