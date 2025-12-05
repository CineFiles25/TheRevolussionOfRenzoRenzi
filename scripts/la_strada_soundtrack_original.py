from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# =========================
# NAMESPACES
# =========================

rrr     = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
rdf     = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs    = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl     = Namespace("http://www.w3.org/2002/07/owl#")
schema  = Namespace("https://schema.org/")
dc      = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
dbo     = Namespace("http://dbpedia.org/ontology/")
crm     = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf    = Namespace("http://xmlns.com/foaf/0.1/")
fiaf    = Namespace("https://fiaf.github.io/film-related-materials/objects/")
skos    = Namespace("http://www.w3.org/2004/02/skos/core#")

# =========================
# GRAPH CREATION
# =========================

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
    """Bind all namespaces to the RDF graph."""
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

g = graph_bindings()

# =========================
# ENTITIES
# =========================

la_strada_soundtrack = URIRef(rrr + "la_strada_soundtrack_original")
la_strada_film       = URIRef(rrr + "la_strada_film")
nino_rota            = URIRef(rrr + "nino_rota")

# Base types
g.add((la_strada_film, RDF.type, schema.Movie))
g.add((schema.MusicRecording, RDFS.subClassOf, schema.CreativeWork))

g.add((nino_rota, RDF.type, FOAF.Person))

# Authority links
g.add((nino_rota, OWL.sameAs, URIRef("http://viaf.org/viaf/88980189")))
# External authority for the film (Wikidata)
g.add((la_strada_film, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))

# =========================
# CSV LOADING
# =========================
# N.B. run this script from the `scripts/` directory

soundtrack_df = read_csv(
    "../csv/la_strada_soundtrack_original.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# =========================
# MAPPING TO RDF
# =========================

for idx, row in soundtrack_df.iterrows():

    # Class type
    g.add((la_strada_soundtrack, RDF.type, schema.MusicRecording))

    # Identifier and reference standard
    g.add((la_strada_soundtrack, dc.identifier, Literal(row["id"])))
    if row["identifiers"]:
        g.add((la_strada_soundtrack, dcterms.identifier, Literal(row["identifiers"])))
    g.add((la_strada_soundtrack, dcterms.conformsTo, Literal(row["standard"])))

    # Titles
    g.add((la_strada_soundtrack, dcterms.title, Literal(row["title"])))
    if row["other_title_information"]:
        g.add(
            (la_strada_soundtrack, schema.alternateName,
             Literal(row["other_title_information"]))
        )

    # Responsibility statement as descriptive note
    if row["responsibility_statement"]:
        g.add(
            (la_strada_soundtrack, dc.description,
             Literal(row["responsibility_statement"]))
        )

    # ----- COMPOSER AND PERFORMERS -----

    # Literal composer from CSV
    if row["composer"]:
        g.add((la_strada_soundtrack, dc.creator, Literal(row["composer"])))

    # Composer as project person node
    g.add((la_strada_soundtrack, schema.composer, nino_rota))

    # Composer authority URI from CSV
    if row["composer_uri"]:
        g.add(
            (la_strada_soundtrack, dcterms.relation,
             Literal(row["composer_uri"], datatype=XSD.anyURI))
        )

    # Performers (literal list)
    if row["performers"]:
        g.add(
            (la_strada_soundtrack, dcterms.contributor,
             Literal(row["performers"]))
        )
        # Optional: performers as byArtist literal
        g.add(
            (la_strada_soundtrack, schema.byArtist,
             Literal(row["performers"]))
        )

    if row["performers_uri"]:
        g.add(
            (la_strada_soundtrack, dcterms.relation,
             Literal(row["performers_uri"], datatype=XSD.anyURI))
        )

    # ----- PUBLICATION DATA -----

    # Place of publication (literal, e.g. [France])
    if row["publication_place"]:
        g.add(
            (la_strada_soundtrack, dcterms.spatial,
             Literal(row["publication_place"]))
        )

    # Publisher and label
    if row["publisher"]:
        g.add((la_strada_soundtrack, dcterms.publisher, Literal(row["publisher"])))
    if row["label"]:
        g.add((la_strada_soundtrack, schema.publisher, Literal(row["label"])))

    if row["publisher_uri"]:
        g.add(
            (la_strada_soundtrack, dcterms.relation,
             Literal(row["publisher_uri"], datatype=XSD.anyURI))
        )
    if row["label_uri"]:
        g.add(
            (la_strada_soundtrack, dcterms.relation,
             Literal(row["label_uri"], datatype=XSD.anyURI))
        )

    # Catalogue number
    if row["catalogue_number"]:
        g.add(
            (la_strada_soundtrack, dcterms.identifier,
             Literal(row["catalogue_number"]))
        )

    # Publication year (kept as string, e.g. "1954?")
    if row["publication_year"]:
        g.add(
            (la_strada_soundtrack, dcterms.issued,
             Literal(row["publication_year"]))
        )

    # Carrier type and physical description
    if row["carrier_type"]:
        g.add(
            (la_strada_soundtrack, dcterms.medium,
             Literal(row["carrier_type"]))
        )
    if row["physical_description"]:
        g.add(
            (la_strada_soundtrack, dcterms.extent,
             Literal(row["physical_description"]))
        )

    # Notes
    if row["notes"]:
        g.add(
            (la_strada_soundtrack, dcterms.description,
             Literal(row["notes"]))
        )

    # ----- SUBJECTS AND RELATED WORKS -----

    if row["subjects"]:
        g.add((la_strada_soundtrack, dc.subject, Literal(row["subjects"])))

    # Internal related work(s) in the project graph
    if row["related_works"]:
        for work_id in [w.strip() for w in row["related_works"].split(";") if w.strip()]:
            related_uri = URIRef(rrr + work_id)
            g.add((la_strada_soundtrack, dcterms.relation, related_uri))

    # Explicit relation to the La Strada film node
    g.add((la_strada_soundtrack, dcterms.relation, la_strada_film))
    g.add((la_strada_soundtrack, schema.about, la_strada_film))

    # External URI for the related work (film authority)
    if row["related_works_uri"]:
        g.add(
            (la_strada_soundtrack, dcterms.relation,
             Literal(row["related_works_uri"], datatype=XSD.anyURI))
        )

    # ----- RIGHTS / TYPE / LANGUAGE -----

    if row["rights"]:
        g.add((la_strada_soundtrack, dcterms.rights, Literal(row["rights"])))

    if row["resource_type"]:
        g.add(
            (la_strada_soundtrack, dcterms.type,
             Literal(row["resource_type"]))
        )

    if row["language"]:
        g.add(
            (la_strada_soundtrack, schema.inLanguage,
             Literal(row["language"]))
        )

# =========================
# SERIALIZATION
# =========================

g.serialize(format="turtle", destination="../ttl/la_strada_soundtrack_original.ttl")
print("CSV converted to TTL!")
