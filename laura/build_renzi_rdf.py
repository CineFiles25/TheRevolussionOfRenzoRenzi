import csv
from pathlib import Path

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF

# ===== CONFIGURAZIONE DI BASE =============================================

# CSV in input
ENTITIES_CSV = Path("entities_renzi.csv")
TRIPLES_CSV  = Path("triples_renzi.csv")

# RDF in output
OUTPUT_TTL = Path("renzi.ttl")

# Namespace di base
BASE_NS   = "http://example.org/renzi/"

# Altri namespace usati
SCHEMA = Namespace("https://schema.org/")
SKOS   = Namespace("http://www.w3.org/2004/02/skos/core#")
PROV   = Namespace("http://www.w3.org/ns/prov#")


def init_graph() -> Graph:
    g = Graph()
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("schema", SCHEMA)
    g.bind("skos", SKOS)
    g.bind("prov", PROV)
    g.bind("rdfs", RDFS)
    g.bind("", Namespace(BASE_NS))  # prefisso ":" implicito
    return g


def read_entities(path: Path):
    entities = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            entities.append(row)
    return entities


def read_triples(path: Path):
    triples = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not (row.get("subject") and row.get("predicate") and row.get("object")):
                continue
            triples.append(row)
    return triples


def resolve_curie(curie: str) -> URIRef:
    if ":" not in curie:
        # caso limite: restituisce l'URI così com'è
        return URIRef(curie)

    pref, local = curie.split(":", 1)

    if pref == "schema":
        return SCHEMA[local]
    if pref == "skos":
        return SKOS[local]
    if pref == "prov":
        return PROV[local]
    if pref == "foaf":
        return FOAF[local]
    if pref == "dcterms":
        return DCTERMS[local]
    if pref == "rdfs":
        return RDFS[local]

    # fallback generico
    return URIRef(curie)


def build_graph(entities, triples) -> Graph:
    g = init_graph()
    BASE = Namespace(BASE_NS)

    # === ENTITÀ ===
    for row in entities:
        sid   = (row.get("id") or "").strip()
        label = (row.get("label") or "").strip()
        cls   = (row.get("class") or "").strip() or "schema:Thing"

        subj = BASE[sid]
        cls_uri = resolve_curie(cls)

        g.add((subj, RDF.type, cls_uri))
        if label:
            g.add((subj, RDFS.label, Literal(label)))

    # === TRIPLE ===
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


def main():
    print(f"[INFO] Leggo entità da {ENTITIES_CSV}")
    entities = read_entities(ENTITIES_CSV)

    print(f"[INFO] Leggo triple da {TRIPLES_CSV}")
    triples = read_triples(TRIPLES_CSV)

    print("[INFO] Costruisco il grafo RDF…")
    g = build_graph(entities, triples)

    print(f"[INFO] Serializzo in {OUTPUT_TTL}")
    g.serialize(destination=str(OUTPUT_TTL), format="turtle")
    print("[OK] Fatto.")


if __name__ == "__main__":
    main()