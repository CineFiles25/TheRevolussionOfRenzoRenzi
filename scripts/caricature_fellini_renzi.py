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

caricature_fellini_renzi = URIRef(rrr + "caricature_fellini_renzi")
federico_fellini         = URIRef(rrr + "federico_fellini")
renzo_renzi              = URIRef(rrr + "renzo_renzi")
cineteca_di_bologna      = URIRef(rrr + "cineteca_di_bologna")
renzi_collection         = URIRef(rrr + "renzi_collection")
renzi_library            = URIRef(rrr + "renzo_renzi_library")

# Tipi di base (come nel libro)
g.add((caricature_fellini_renzi, RDF.type, schema.VisualArtwork))
g.add((schema.VisualArtwork, RDFS.subClassOf, schema.CreativeWork))

g.add((federico_fellini, RDF.type, FOAF.Person))
g.add((renzo_renzi, RDF.type, FOAF.Person))
g.add((cineteca_di_bologna, RDF.type, schema.Organization))
g.add((renzi_library, RDF.type, schema.Library))
g.add((renzi_collection, RDF.type, dcterms.Collection))

# Authority links
g.add((federico_fellini, OWL.sameAs, URIRef("http://viaf.org/viaf/76315386")))
g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))

# =========================
# CSV
# =========================

caricature_df = read_csv(
    "../csv/caricature_fellini_renzi.csv",
    keep_default_na=False,
    encoding="utf-8"
)

# =========================
# MAPPING
# =========================

for idx, row in caricature_df.iterrows():
    # Standard di riferimento (es. Scheda OA)
    g.add((caricature_fellini_renzi, dcterms.conformsTo, Literal(row["standard"])))

    # Titoli
    g.add((caricature_fellini_renzi, dcterms.title, Literal(row["title"])))
    if row["other_title_information"]:
        g.add((caricature_fellini_renzi, schema.alternateName,
               Literal(row["other_title_information"])))

    # Iscrizione e descrizione come note descrittive
    if row["inscription"]:
        g.add((caricature_fellini_renzi, dc.description, Literal(row["inscription"])))
    if row["description"]:
        g.add((caricature_fellini_renzi, dc.description, Literal(row["description"])))

    # Autore e soggetto
    g.add((caricature_fellini_renzi, dcterms.creator, renzo_renzi))
    g.add((caricature_fellini_renzi, schema.about, federico_fellini))

    # Dati di creazione e tecnica/materiali
    if row["creation_date"]:
        g.add((caricature_fellini_renzi, dcterms.created, Literal(row["creation_date"])))
    if row["technique"]:
        g.add((caricature_fellini_renzi, dcterms.medium, Literal(row["technique"])))
    if row["material"]:
        g.add((caricature_fellini_renzi, dcterms.material, Literal(row["material"])))

    # Dimensioni → extent (coerente con il libro)
    if row["dimensions"]:
        g.add((caricature_fellini_renzi, dcterms.extent, Literal(row["dimensions"])))

    # Proprietà, collezione, location
    g.add((caricature_fellini_renzi, crm.P52_has_current_owner, cineteca_di_bologna))
    g.add((renzi_collection, dcterms.hasPart, caricature_fellini_renzi))
    g.add((caricature_fellini_renzi, dcterms.location, renzi_library))
    g.add((renzi_library, schema.location, cineteca_di_bologna))

    # Diritti
    if row["rights"]:
        g.add((caricature_fellini_renzi, dcterms.rights, Literal(row["rights"])))

    # Lingua
    if row["language"]:
        g.add((caricature_fellini_renzi, schema.inLanguage, Literal(row["language"])))

# =========================
# SERIALIZATION
# =========================

g.serialize(format="turtle", destination="../ttl/caricature_fellini_renzi.ttl")
print("CSV converted to TTL!")

