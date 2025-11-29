import pandas as pd
from rdflib import (
    Namespace,
    Graph,
    RDF,
    URIRef,
    OWL,
    Literal,
    XSD,
    RDFS,
)

# ============================================
# NAMESPACES
# ============================================

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
fiaf = Namespace("https://fiaf.github.io/film-related-materials/objects/")
owl = Namespace("http://www.w3.org/2002/07/owl#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# ============================================
# GRAPH CREATION & PREFIXES
# ============================================

g = Graph()

ns_dict = {
    "rrr": rrr,
    "schema": schema,
    "dcterms": dcterms,
    "dc": dc,
    "fiaf": fiaf,
    "owl": owl,
    "rdf": rdf,
    "rdfs": rdfs,
}

def graph_bindings():
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

g = graph_bindings()

# ============================================
# FIXED ENTITIES (MANUALLY CREATED)
# ============================================

# use rrr["localName"]
la_strada = rrr["la-strada"]

# authority URIs
renzo_renzi = rrr["renzo-renzi"]
cineteca_di_bologna = rrr["cineteca-di-bologna"]
bologna = rrr["bologna"]

# sameAs
g.add((renzo_renzi, owl.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, owl.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, owl.sameAs, URIRef("http://viaf.org/viaf/257723025")))

# ============================================
# READ CSV FROM GITHUB
# ============================================

GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/CineFiles25/TheRevolussionOfRenzoRenzi/refs/heads/main/csv/lastrada_movie.csv"
)

df = pd.read_csv(GITHUB_CSV_URL, keep_default_na=False, encoding="utf-8")

# ============================================
# MAPPING LOOP (SIMPLE, CLEAN, DIRECT)
# ============================================

for idx, row in df.iterrows():

    # creat FIAF class
    g.add((la_strada, RDF.type, fiaf.Film))

    # ==== Literary metadata ====
    if row["Original Title"]:
        g.add((la_strada, dcterms.title, Literal(row["Original Title"])))

    if row["National Title (in Italy)"]:
        g.add((la_strada, dcterms.alternative, Literal(row["National Title (in Italy)"])))

    if row["Director"]:
        g.add((la_strada, dcterms.creator, Literal(row["Director"])))

    if row["Production Company / Sponsor"]:
        g.add((la_strada, dcterms.publisher, Literal(row["Production Company / Sponsor"])))

    if row["Country of Origin"]:
        g.add((la_strada, dcterms.spatial, Literal(row["Country of Origin"])))

    if row["Language"]:
        g.add((la_strada, dcterms.language, Literal(row["Language"])))

    if row["Year of First Public Release"]:
        g.add((la_strada, dcterms.issued, Literal(row["Year of First Public Release"], datatype=XSD.gYear)))

    # ==== Technical metadata ====
    if row["Length"]:
        g.add((la_strada, dcterms.extent, Literal(row["Length"])))

    if row["Duration"]:
        g.add((la_strada, dcterms.extent, Literal(row["Duration"])))

    if row["Gauge / Format"]:
        g.add((la_strada, dcterms.format, Literal(row["Gauge / Format"])))

    if row["Colour"]:
        g.add((la_strada, dcterms.format, Literal(row["Colour"])))

    if row["Sound"]:
        g.add((la_strada, dcterms.format, Literal(row["Sound"])))

    if row["Work Type"]:
        g.add((la_strada, dcterms.type, Literal(row["Work Type"])))

# ============================================
# SERIALIZATION
# ============================================

g.serialize(format="turtle", destination="lastrada_movie.ttl")
print("GitHub CSV converted to TTL successfully!")

