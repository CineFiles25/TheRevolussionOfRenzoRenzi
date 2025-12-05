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
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

g = graph_bindings()

# =========================
# ENTITIES
# =========================

renzi_interview      = URIRef(rrr + "renzi_interview_2000")
renzo_renzi          = URIRef(rrr + "renzo_renzi")
bologna              = URIRef(rrr + "bologna")
cineteca_di_bologna  = URIRef(rrr + "cineteca_di_bologna")
renzi_collection     = URIRef(rrr + "renzi_collection")
renzi_library        = URIRef(rrr + "renzo_renzi_library")

# Tipi di base
g.add((renzi_interview, RDF.type, schema.Interview))
g.add((schema.Interview, RDFS.subClassOf, schema.CreativeWork))

g.add((renzo_renzi, RDF.type, FOAF.Person))
g.add((bologna, RDF.type, schema.Place))
g.add((cineteca_di_bologna, RDF.type, schema.Organization))
g.add((renzi_collection, RDF.type, dcterms.Collection))
g.add((renzi_library, RDF.type, schema.Library))

# Authority links
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# =========================
# CSV
# =========================

renzi_interview_2000 = read_csv(
    "../csv/renzi_interview_2000.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# =========================
# MAPPING
# =========================

for idx, row in renzi_interview_2000.iterrows():
    # Identificatore e standard di descrizione (FIAF / ISBD NBM ecc.)
    if row["id"]:
        g.add((renzi_interview, dc.identifier, Literal(row["id"])))
    if row["standard"]:
        g.add((renzi_interview, dcterms.conformsTo, Literal(row["standard"])))

    # Titolo principale e titolo alternativo
    if row["title"]:
        g.add((renzi_interview, dcterms.title, Literal(row["title"])))
    if row["other_title_information"]:
        g.add((renzi_interview, schema.alternateName,
               Literal(row["other_title_information"])))

    # Tipo di risorsa (es. "videointervista")
    if row["resource_type"]:
        g.add((renzi_interview, dcterms.type, Literal(row["resource_type"])))

    # Soggetto/partecipante principale
    g.add((renzi_interview, schema.about, renzo_renzi))
    # volendo, potresti anche aggiungere:
    # g.add((renzi_interview, schema.interviewee, renzo_renzi))

    # Intervistatore come contributore (literal)
    if row["interviewer"]:
        g.add((renzi_interview, dcterms.contributor, Literal(row["interviewer"])))
        # volendo: schema.interviewer come literal:
        # g.add((renzi_interview, schema.interviewer, Literal(row["interviewer"])))

    # Produttore/editore e luogo
    g.add((renzi_interview, schema.publisher, cineteca_di_bologna))
    g.add((renzi_interview, dcterms.spatial, bologna))
    g.add((renzi_interview, schema.location, renzi_library))

    # Anno di produzione
    if row["production_year"]:
        g.add((renzi_interview, dcterms.created,
               Literal(row["production_year"], datatype=XSD.gYear)))

    # Durata, colore, suono, formato
    if row["duration"]:
        g.add((renzi_interview, schema.duration, Literal(row["duration"])))
    if row["colour"]:
        g.add((renzi_interview, schema.color, Literal(row["colour"])))
    if row["sound"]:
        g.add((renzi_interview, schema.sound, Literal(row["sound"])))
    if row["format"]:
        g.add((renzi_interview, dcterms.format, Literal(row["format"])))

    # Collezione
    g.add((renzi_collection, dcterms.hasPart, renzi_interview))

    # Diritti (come URI, se nel CSV c'è un link)
    if row["rights"]:
        g.add((renzi_interview, dcterms.rights, URIRef(row["rights"])))

    # Lingua
    if row["language"]:
        g.add((renzi_interview, schema.inLanguage, Literal(row["language"])))

    # Descrizioni e note
    if row["description"]:
        g.add((renzi_interview, dcterms.description, Literal(row["description"])))
    if row["notes"]:
        g.add((renzi_interview, dcterms.description, Literal(row["notes"])))

# =========================
# SERIALIZATION
# =========================

g.serialize(format="turtle", destination="../ttl/renzi_interview_2000.ttl")
print("CSV converted to TTL!")
