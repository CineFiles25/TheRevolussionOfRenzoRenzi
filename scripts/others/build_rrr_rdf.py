from pathlib import Path
import csv

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF, SKOS, OWL


# === PATHS =====================================================

ENTITIES_CSV = Path("csv/rrr_entities.csv")
TRIPLES_CSV = Path("csv/rrr_triples.csv")
OUTPUT_TTL = Path("ttl/rrr.ttl")


# === NAMESPACES ================================================

RRR = Namespace("https://cinefiles25.github.io/renzi/")
SCHEMA = Namespace("https://schema.org/")
PROV = Namespace("http://www.w3.org/ns/prov#")


def resolve_qname(qname: str) -> URIRef | None:
    if ":" not in qname:
        return None

    prefix, local = qname.split(":", 1)
    prefix = prefix.strip()
    local = local.strip()

    if prefix == "schema":
        return SCHEMA[local]
    if prefix == "dcterms":
        return DCTERMS[local]
    if prefix == "foaf":
        return FOAF[local]
    if prefix == "skos":
        return SKOS[local]
    if prefix == "prov":
        return PROV[local]
    if prefix == "owl":
        return OWL[local]
    if prefix == "rrr":
        return RRR[local]

    print(f"[WARN] Unknown prefix in predicate: {qname}")
    return None


def build_graph() -> Graph:
    g = Graph()

    # Bind prefixes for nicer Turtle output
    g.bind("rrr", RRR)
    g.bind("schema", SCHEMA)
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("skos", SKOS)
    g.bind("prov", PROV)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("owl", OWL)

    id_to_uri: dict[str, URIRef] = {}

    # === STEP 1: LOAD ENTITIES =================================
    with ENTITIES_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ent_id = (row.get("id") or "").strip()
            label = (row.get("label") or "").strip()
            cls = (row.get("class") or "").strip()
            uri = (row.get("uri") or "").strip()
            same_as_raw = (row.get("sameAs") or "").strip()

            if not ent_id:
                continue

            subj = URIRef(uri) if uri else RRR[ent_id]
            id_to_uri[ent_id] = subj

            if cls:
                cls_uri = resolve_qname(cls)
                if cls_uri:
                    g.add((subj, RDF.type, cls_uri))
                else:
                    print(f"[WARN] Unknown class for entity {ent_id}: {cls}")

            if label:
                g.add((subj, RDFS.label, Literal(label)))

            if same_as_raw:
                for same_as in same_as_raw.split(";"):
                    same_as = same_as.strip()
                    if same_as:
                        g.add((subj, OWL.sameAs, URIRef(same_as)))

    # === STEP 2: LOAD TRIPLES ==================================
    with TRIPLES_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            subj_id = (row.get("subject") or "").strip()
            pred_qn = (row.get("predicate") or "").strip()
            obj_val = (row.get("object") or "").strip()
            obj_type = (row.get("object_type") or "").strip().lower() or "iri"

            if not subj_id or not pred_qn or not obj_val:
                continue

            subj = id_to_uri.get(subj_id, RRR[subj_id])
            pred = resolve_qname(pred_qn)
            if not pred:
                continue

            if obj_type == "iri":
                obj = id_to_uri.get(obj_val, RRR[obj_val])
            elif obj_type == "literal":
                obj = Literal(obj_val)
            else:
                print(
                    f"[WARN] Unknown object_type '{obj_type}', "
                    "treating as literal."
                )
                obj = Literal(obj_val)

            g.add((subj, pred, obj))

    return g


def main() -> None:
    graph = build_graph()
    OUTPUT_TTL.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(OUTPUT_TTL, format="turtle")
    print(f"RDF graph written to {OUTPUT_TTL} with {len(graph)} triples.")


if __name__ == "__main__":
    main()
