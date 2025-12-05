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

la_strada_soundtrack = URIRef(rrr + "la_strada_soundtrack_original")
la_strada_film       = URIRef(rrr + "la_strada_film")
nino_rota            = URIRef(rrr + "nino_rota")
federico_fellini     = URIRef(rrr + "federico_fellini")

# Tipi di base
g.add((la_strada_film, RDF.type, schema.Movie))
g.add((schema.MusicRecording, RDFS.subClassOf, schema.CreativeWork))

g.add((nino_rota, RDF.type, FOAF.Person))
g.add((federico_fellini, RDF.type, FOAF.Person))

# Authority links
g.add((nino_rota, OWL.sameAs, URIRef("http://viaf.org/viaf/88980189")))
g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((la_strada_film, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18402")))

# =========================
# CSV
# =========================

la_strada_soundtrack_original = read_csv(
    "../csv/la_strada_soundtrack_original.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# =========================
# MAPPING
# =========================

for idx, row in la_strada_soundtrack_original.iterrows():
    # Tipo dell'oggetto
    g.add((la_strada_soundtrack, RDF.type, schema.MusicRecording))

    # Prendo tutti i campi in modo sicuro (se non esistono → "")
    title               = row.get("title", "")
    other_title         = row.get("other_title_information", "")
    soundtrack_type     = row.get("Soundtrack Type", "")
    release_year        = row.get("Release Year", "")
    publisher           = row.get("Publisher", "")
    country             = row.get("Country", "")
    recording_location  = row.get("Recording Location", "")
    current_location    = row.get("Current Location", "")
    language            = row.get("Language", "")
    standard            = row.get("Standard", "")
    identifier          = row.get("ID", "")
    notes               = row.get("Notes", "")

    # Titolo e titolo alternativo
    if title:
        g.add((la_strada_soundtrack, dcterms.title, Literal(title)))
    if other_title:
        g.add((la_strada_soundtrack, schema.alternateName, Literal(other_title)))

    # Autore / compositore
    g.add((la_strada_soundtrack, dcterms.creator, nino_rota))
    g.add((la_strada_soundtrack, schema.composer, nino_rota))

    # Tipo di soundtrack (se c'è la colonna e il dato)
    if soundtrack_type:
        g.add((la_strada_soundtrack, schema.additionalType, Literal(soundtrack_type)))

    # Relazione con il film La Strada
    g.add((la_strada_soundtrack, dcterms.relation, la_strada_film))
    g.add((la_strada_soundtrack, schema.about, la_strada_film))

    # Pubblicazione
    if release_year:
        g.add((la_strada_soundtrack, schema.datePublished,
               Literal(release_year, datatype=XSD.gYear)))

    if publisher:
        g.add((la_strada_soundtrack, dcterms.publisher, Literal(publisher)))

    # Luoghi / provenienza (rimangono literal)
    if country:
        g.add((la_strada_soundtrack, schema.countryOfOrigin, Literal(country)))
    if recording_location:
        g.add((la_strada_soundtrack, schema.locationCreated, Literal(recording_location)))
    if current_location:
        g.add((la_strada_soundtrack, schema.contentLocation, Literal(current_location)))

    # Lingua
    if language:
        g.add((la_strada_soundtrack, schema.inLanguage, Literal(language)))

    # Standard di riferimento (ISBD NBM / FIAF ecc.)
    if standard:
        g.add((la_strada_soundtrack, dcterms.conformsTo, Literal(standard)))

    # Identificatore locale
    if identifier:
        g.add((la_strada_soundtrack, dc.identifier, Literal(identifier)))

    # Note
    if notes:
        g.add((la_strada_soundtrack, dcterms.description, Literal(notes)))

# =========================
# SERIALIZATION
# =========================

g.serialize(format="turtle", destination="../ttl/la_strada_soundtrack_original.ttl")
print("CSV converted to TTL!")


