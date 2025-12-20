from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

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


# ENTITIES

book_il_primo_fellini = URIRef(rrr + "book_il_primo_fellini")
la_strada_film = URIRef(rrr + "la_strada_film")
renzo_renzi = URIRef(rrr + "renzo_renzi")
federico_fellini = URIRef(rrr + "federico_fellini")
bologna = URIRef(rrr + "bologna")

g.add((renzo_renzi, RDF.type, foaf.Person))
g.add((federico_fellini, RDF.type, foaf.Person))
g.add((bologna, RDF.type, schema.Place))
g.add((la_strada_film, RDF.type, schema.Movie))

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((la_strada_film, OWL.sameAs, URIRef("http://viaf.org/viaf/176979060")))

g.add((schema.Book, RDFS.subClassOf, schema.CreativeWork))


# CSV LOADING
# N.B. run this script from the `scripts/` directory

first_fellini_book = read_csv(
    "../csv/book_il_primo_fellini.csv",
    keep_default_na=False,
    encoding="utf-8"
)

g = graph_bindings()


# MAPPING TO RDF

for _, row in first_fellini_book.iterrows():

    g.add((book_il_primo_fellini, RDF.type, schema.Book))

    # Identifiers and titles
    if row.get("id"):
        g.add((book_il_primo_fellini, dcterms.identifier, Literal(row["id"])))

    if row.get("title"):
        g.add((book_il_primo_fellini, dcterms.title, Literal(row["title"])))

    if row.get("other_title_information"):
        g.add((book_il_primo_fellini, dcterms.alternative, Literal(row["other_title_information"])))

    # Responsibility statement -> description
    if row.get("responsibility_statement"):
        g.add((book_il_primo_fellini, dcterms.description, Literal(row["responsibility_statement"])))

    # CREATOR AND CONTRIBUTORS

    # Literal creator from CSV (kept)
    if row.get("creator"):
        g.add((book_il_primo_fellini, dcterms.creator, Literal(row["creator"])))

    # Resource-level author
    g.add((book_il_primo_fellini, schema.author, federico_fellini))

    # Renzi as contributor (resource)
    g.add((book_il_primo_fellini, dcterms.contributor, renzo_renzi))

    # Other contributors (literal)
    if row.get("other_contributors"):
        g.add((book_il_primo_fellini, dcterms.contributor, Literal(row["other_contributors"])))

    # External URIs for people
    if row.get("creator_uri"):
        g.add((book_il_primo_fellini, dcterms.relation, Literal(row["creator_uri"], datatype=XSD.anyURI)))

    if row.get("other_contributors_uri"):
        for uri_str in [u.strip() for u in row["other_contributors_uri"].split("|") if u.strip()]:
            g.add((book_il_primo_fellini, dcterms.relation, Literal(uri_str, datatype=XSD.anyURI)))

    # PUBLICATION

    if row.get("publisher"):
        g.add((book_il_primo_fellini, dcterms.publisher, Literal(row["publisher"])))

    if row.get("publication_place"):
        g.add((book_il_primo_fellini, dcterms.spatial, Literal(row["publication_place"])))

    if row.get("publication_year"):
        g.add((book_il_primo_fellini, dcterms.issued, Literal(row["publication_year"], datatype=XSD.gYear)))

    # SERIES

    if row.get("series"):
        series_uri = URIRef(rrr + "series_il_primo_fellini")
        g.add((series_uri, RDF.type, schema.CreativeWork))
        g.add((series_uri, dcterms.title, Literal(row["series"])))
        g.add((book_il_primo_fellini, dcterms.isPartOf, series_uri))

    # PHYSICAL DESCRIPTION / NOTES / RIGHTS

    if row.get("extent"):
        g.add((book_il_primo_fellini, dcterms.extent, Literal(row["extent"])))

    if row.get("notes"):
        g.add((book_il_primo_fellini, dcterms.description, Literal(row["notes"])))

    if row.get("rights"):
        g.add((book_il_primo_fellini, dcterms.rights, Literal(row["rights"])))

    # SUBJECTS

    g.add((book_il_primo_fellini, dc.subject, federico_fellini))

    if row.get("subjects"):
        g.add((book_il_primo_fellini, dc.subject, Literal(row["subjects"])))

    # RELATED WORKS

    if row.get("related_works"):
        for work_id in [w.strip() for w in row["related_works"].split(";") if w.strip()]:
            related_uri = URIRef(rrr + work_id)
            g.add((book_il_primo_fellini, dcterms.relation, related_uri))

    if row.get("related_works_uri"):
        for uri_str in [u.strip() for u in row["related_works_uri"].split("|") if u.strip()]:
            g.add((book_il_primo_fellini, dcterms.relation, Literal(uri_str, datatype=XSD.anyURI)))

    g.add((book_il_primo_fellini, dcterms.relation, la_strada_film))

    # RESOURCE TYPE AND LANGUAGE

    if row.get("resource_type"):
        g.add((book_il_primo_fellini, dcterms.type, Literal(row["resource_type"])))

    if row.get("language"):
        g.add((book_il_primo_fellini, schema.inLanguage, Literal(row["language"])))

    if row.get("standard"):
        g.add((book_il_primo_fellini, dcterms.conformsTo, Literal(row["standard"])))


# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/book_il_primo_fellini.ttl")
print("CSV converted to TTL!")
