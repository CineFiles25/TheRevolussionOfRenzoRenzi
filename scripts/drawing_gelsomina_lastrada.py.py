import pandas as pd
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD

# ============================================
# CONFIGURATION
# ============================================

GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/"
    "CineFiles25/TheRevolussionOfRenzoRenzi/main/"
    "csv/drawing_gelsomina_lastrada.csv"
)

OUTPUT_TTL = "drawing_gelsomina_lastrada.ttl"

# ============================================
# NAMESPACES
# ============================================

rrr      = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
oa       = Namespace("https://iccd.beniculturali.it/it/ricercanormative/29/oa-opere-oggetti-d-arte-3_00#")
iccd     = Namespace("https://iccd.beniculturali.it/")
dc       = Namespace("http://purl.org/dc/elements/1.1/")
dcterms  = Namespace("http://purl.org/dc/terms/")
owl_ns   = Namespace("http://www.w3.org/2002/07/owl#")

g = Graph()

ns_dict = {
    "rrr": rrr,
    "oa": oa,
    "iccd": iccd,
    "dc": dc,
    "dcterms": dcterms,
    "owl": owl_ns,
}

def graph_bindings():
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

g = graph_bindings()

# ============================================
# ENTITY：instance of the drawing（fixed name）
# ============================================

drawing = URIRef(rrr + "drawing_gelsomina_lastrada")

# ============================================
# READ CSV FROM GITHUB
# ============================================

df = pd.read_csv(GITHUB_CSV_URL, keep_default_na=False, encoding="utf-8")
print(f"Read {len(df)} row(s) from CSV.\n")

# ============================================
# MAPPING（ultra simple ABox：one column by one row g.add）
# ============================================

for idx, row in df.iterrows():
    # class： oa:Artwork
    g.add((drawing, RDF.type, oa.Artwork))

    # ---- 字面值属性 ----
    if row["Title"]:
        g.add((drawing, dc.title, Literal(row["Title"])))

    if row["Author"]:
        g.add((drawing, dc.creator, Literal(row["Author"])))

    if row["Description"]:
        g.add((drawing, dc.description, Literal(row["Description"])))

    if row["Technique"]:
        g.add((drawing, dcterms.medium, Literal(row["Technique"])))

    if row["Support"]:
        g.add((drawing, dcterms.material, Literal(row["Support"])))

    if row["Dimensions"]:
        g.add((drawing, dcterms.extent, Literal(row["Dimensions"])))

    if row["Collection"]:
        g.add((drawing, dcterms.isPartOf, Literal(row["Collection"])))

    # ---- URL: URI object----
    if row["URL"]:
        g.add((drawing, dcterms.identifier, URIRef(row["URL"])))

# ============================================
# SERIALIZATION
# ============================================

g.serialize(format="turtle", destination=OUTPUT_TTL)
print(f"CSV from GitHub converted to TTL: {OUTPUT_TTL}")

