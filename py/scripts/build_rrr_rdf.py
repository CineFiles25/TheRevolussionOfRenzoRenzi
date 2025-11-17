import csv
from pathlib import Path

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF

# ============================================================================
# CONFIGURATION
# ============================================================================

# Input CSV files
ENTITIES_CSV = Path("entities_renzi.csv")
TRIPLES_CSV  = Path("triples_renzi.csv")

# Output Turtle file
OUTPUT_TTL = Path("renzi.ttl")

# Base namespace for all local entities (prefix ":")
BASE_NS = "http://example.org/renzi/"

# Additional namespaces
SCHEMA = Namespace("https://schema.org/")
SKOS   = Namespace("http://www.w3.org/2004/02/skos/core#")
PROV   = Namespace("http://www.w3.org/ns/prov#")


# ============================================================================
# GRAPH INITIALIZATION
# ============================================================================

def init_graph() -> Graph:
    g = Graph()
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("schema", SCHEMA)
    g.bind("skos", SKOS)
    g.bind("prov", PROV)
    g.bind("rdfs", RDFS)
    g.bind("", Namespace(BASE_NS))  # default prefix ":"
    return g


# ============================================================================
# CSV READERS
# ============================================================================

def read_entities(path: Path):
    entities = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("id"):
                entities.append(row)
    return entities


def read_triples(path: Path):
    triples = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("subject") and row.get("predicate") and row.get("object"):
                triples.append(row)
    return triples


# ============================================================================
# CURIE RESOLUTION
# ============================================================================

def resolve_curie(curie: str) -> URIRef:
    if ":" not in curie:
        return URIRef(curie)

    prefix, local = curie.split(":", 1)

    if prefix == "schema":
        return SCHEMA[local]
    if prefix == "skos":
        return SKOS[local]
    if prefix == "prov":
        return PROV[local]
    if prefix == "foaf":
        return FOAF[local]
    if prefix == "dcterms":
        return DCTERMS[local]
    if prefix == "rdfs":
        return RDFS[local]

    # Generic fallback
    return URIRef(curie)


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def build_graph(entities, triples) -> Graph:
    """
    Build the RDF graph from the entities list and the triples list.
    """
    g = init_graph()
    BASE = Namespace(BASE_NS)

    # --- ENTITIES ---
    for row in entities:
        sid   = (row.get("id") or "").strip()
        label = (row.get("label") or "").strip()
        cls   = (row.get("class") or "").strip() or "schema:Thing"

        subj = BASE[sid]
        cls_uri = resolve_curie(cls)

        g.add((subj, RDF.type, cls_uri))
        if label:
            g.add((subj, RDFS.label, Literal(label)))

    # --- TRIPLES ---
    for row in triples:
        s = (row.get("subject") or "").strip()
        p = (row.get("predicate") or "").strip()
        o = (row.get("object") or "").strip()
        otype = (row.get("object_type") or "iri").strip().lower()

        subj = BASE[s]
        pred = resolve_curie(p)

        if otype == "iri":
            obj = BASE[o]
        else:
            obj = Literal(o)

        g.add((subj, pred, obj))

    return g


# ============================================================================
# MAIN
# ============================================================================

def main():
    print(f"[INFO] Reading entities from {ENTITIES_CSV}")
    entities = read_entities(ENTITIES_CSV)

    print(f"[INFO] Reading triples from {TRIPLES_CSV}")
    triples = read_triples(TRIPLES_CSV)

    print("[INFO] Building RDF graph…")
    g = build_graph(entities, triples)

    print(f"[INFO] Serializing to {OUTPUT_TTL}")
    g.serialize(destination=str(OUTPUT_TTL), format="turtle")
    print("[OK] Done.")


if __name__ == "__main__":
    main()
