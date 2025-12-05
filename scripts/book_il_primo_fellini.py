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

book_il_primo_fellini = URIRef(rrr + "book_il_primo_fellini")
la_strada_film        = URIRef(rrr + "la_strada_film")
renzo_renzi           = URIRef(rrr + "renzo_renzi")
federico_fellini      = URIRef(rrr + "federico_fellini")
bologna               = URIRef(rrr + "bologna")

# Basic typing
g.add((renzo_renzi, RDF.type, FOAF.Person))
g.add((federico_fellini, RDF.type, FOAF.Person))
g.add((bologna, RDF.type, schema.Place))
g.add((la_strada_film, RDF.type, schema.Movie))

# Authority links
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((la_strada_film, OWL.sameAs, URIRef("http://viaf.org/viaf/176979060")))

# Conceptual model: Book subclass of CreativeWork
g.add((schema.Book, RDFS.subClassOf, schema.CreativeWork))

# =========================
# CSV LOADING
# =========================

first_fellini_book = read_csv(
    "../csv/book_il_primo_fellini.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# =========================
# MAPPING TO RDF
# =========================

for idx, row in first_fellini_book.iterrows():

    # Type
    g.add((book_il_primo_fellini, RDF.type, schema.Book))

    # Identifiers and titles
    g.add((book_il_primo_fellini, dc.identifier, Literal(row["id"])))
    g.add((book_il_primo_fellini, dcterms.title, Literal(row["title"])))
    g.add((book_il_primo_fellini, dcterms.alternative,
           Literal(row["other_title_information"])))

    # Statement of responsibility → descriptive note
    g.add((book_il_primo_fellini, dc.description,
           Literal(row["responsibility_statement"])))

    # Agents
    g.add((book_il_primo_fellini, schema.author, renzo_renzi))
    g.add((book_il_primo_fellini, dcterms.contributor, federico_fellini))

    if row["other_contributors"]:
        g.add((book_il_primo_fellini, schema.contributor,
               Literal(row["other_contributors"])))

    # Publisher, place, and publication year
    g.add((book_il_primo_fellini, dcterms.publisher, Literal(row["publisher"])))
    g.add((book_il_primo_fellini, dcterms.spatial, bologna))
    g.add((book_il_primo_fellini, dcterms.issued,
           Literal(row["publication_year"], datatype=XSD.gYear)))

    # Series
    if row["series"]:
        series_uri = URIRef(rrr + "series_il_primo_fellini")
        g.add((series_uri, RDF.type, schema.CreativeWork))
        g.add((series_uri, dcterms.title, Literal(row["series"])))
        g.add((book_il_primo_fellini, dcterms.isPartOf, series_uri))

    # Extent / notes / rights
    g.add((book_il_primo_fellini, dcterms.extent, Literal(row["extent"])))

    if row["notes"]:
        g.add((book_il_primo_fellini, dc.description, Literal(row["notes"])))

    if row["rights"]:
        g.add((book_il_primo_fellini, dcterms.rights, Literal(row["rights"])))

    # Subjects
    g.add((book_il_primo_fellini, dc.subject, federico_fellini))

    if row["subjects"]:
        g.add((book_il_primo_fellini, dc.subject, Literal(row["subjects"])))

    # Relation to the film La Strada
    g.add((book_il_primo_fellini, dcterms.relation, la_strada_film))

    # Language
    g.add((book_il_primo_fellini, schema.inLanguage, Literal(row["language"])))

    # Standard used
    g.add((book_il_primo_fellini, dcterms.conformsTo, Literal(row["standard"])))

# =========================
# SERIALIZATION
# =========================

g.serialize(format="turtle", destination="../ttl/book_il_primo_fellini.ttl")
print("CSV converted to TTL!")

g.serialize(format="turtle", destination="../ttl/book_il_primo_fellini.ttl")
print("CSV converted to TTL!")

