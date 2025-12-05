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
    # Leggo tutto in modo sicuro (se la colonna non esiste -> "")
    id_value        = row.get("id", "")
    standard        = row.get("standard", "")
    title           = row.get("title", "")
    other_title     = row.get("other_title_information", "")
    resource_type   = row.get("resource_type", "")
    interviewer     = row.get("interviewer", "")
    production_year = row.get("production_year", "")
    duration        = row.get("duration", "")
    colour          = row.get("colour", "")
    sound           = row.get("sound", "")
    format_value    = row.get("format", "")
    rights          = row.get("rights", "")
    language        = row.get("language", "")
    description     = row.get("description", "")
    notes           = row.get("notes", "")

    # Identificatore e standard
    if id_value:
        g.add((renzi_interview, dc.identifier, Literal(id_value)))
    if standard:
        g.add((renzi_interview, dcterms.conformsTo, Literal(standard)))

    # Titoli
    if title:
        g.add((renzi_interview, dcterms.title, Literal(title)))
    if other_title:
        g.add((renzi_interview, schema.alternateName, Literal(other_title)))

    # Tipo di risorsa (es. "videointervista")
    if resource_type:
        g.add((renzi_interview, dcterms.type, Literal(resource_type)))

    # Renzo Renzi come soggetto/intervistato
    g.add((renzi_interview, schema.about, renzo_renzi))

    # Intervistatore come contributore (literal)
    if interviewer:
        g.add((renzi_interview, dcterms.contributor, Literal(interviewer)))
        # opzionale:
        # g.add((renzi_interview, schema.interviewer, Literal(interviewer)))

    # Publisher e luogo
    g.add((renzi_interview, schema.publisher, cineteca_di_bologna))
    g.add((renzi_interview, dcterms.spatial, bologna))
    g.add((renzi_interview, schema.location, renzi_library))

    # Anno di produzione
    if production_year:
        g.add((renzi_interview, dcterms.created,
               Literal(production_year, datatype=XSD.gYear)))

    # Durata, colore, suono, formato
    if duration:
        g.add((renzi_interview, schema.duration, Literal(duration)))
    if colour:
        g.add((renzi_interview, schema.color, Literal(colour)))
    if sound:
        g.add((renzi_interview, schema.sound, Literal(sound)))
    if format_value:
        # USO LA VERSIONE CON [] PER EVITARE IL PROBLEMA DEL .format
        g.add((renzi_interview, dcterms["format"], Literal(format_value)))

    # Collezione
    g.add((renzi_collection, dcterms.hasPart, renzi_interview))

    # Diritti (come URI se è una URL, altrimenti va bene anche Literal)
    if rights:
        if str(rights).startswith("http"):
            g.add((renzi_interview, dcterms.rights, URIRef(rights)))
        else:
            g.add((renzi_interview, dcterms.rights, Literal(rights)))

    # Lingua
    if language:
        g.add((renzi_interview, schema.inLanguage, Literal(language)))

    # Descrizione e note
    if description:
        g.add((renzi_interview, dcterms.description, Literal(description)))
    if notes:
        g.add((renzi_interview, dcterms.description, Literal(notes)))

# =========================
# SERIALIZATION
# =========================

g.serialize(format="turtle", destination="../ttl/renzi_interview_2000.ttl")
print("CSV converted to TTL!")
