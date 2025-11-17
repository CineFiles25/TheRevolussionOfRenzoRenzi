from pathlib import Path
import csv

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF, SKOS

# === PATHS =====================================================

# run this script from the ROOT of the repo:
#   python py/build_rrr_rdf.py

ENTITIES_CSV = Path("csv/entities_renzi.csv")
TRIPLES_CSV  = Path("csv/triples_renzi.csv")
OUTPUT_TTL   = Path("ttl/rrr.ttl")

# === NAMESPACES ================================================

# base namespaces
RRR    = Namespace("https://example.org/rrr/")
SCHEMA = Namespace("https://schema.org/")
PROV   = Namespace("http://www.w3.org/ns/prov#")

g = Graph()

g.bind("rrr", RRR)
g.bind("schema", SCHEMA)
g.bind("dcterms", DCTERMS)
g.bind("foaf", FOAF)
g.bind("skos", SKOS)
g.bind("prov", PROV)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)

# small helper to resolve "prefix:LocalName" into a URIRef
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

    # unknown namespace
    return None


# === STEP 1: LOAD ENTITIES =====================================

id_to_uri: dict[str, URIRef] = {}

with ENTITIES_CSV.open(encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ent_id = (row.get("id") or "").strip()
        label  = (row.get("label") or "").strip()
        cls    = (row.get("class") or "").strip()
        uri    = (row.get("uri") or "").strip()
        same_as = (row.get("sameAs") or "").strip()

        if not ent_id:
            continue

        # if an explicit URI is given, use it; otherwise mint one with the RRR namespace
        if uri:
            subj = URIRef(uri)
        else:
            subj = RRR[ent_id]

        id_to_uri[ent_id] = subj

        # rdf:type from the "class" column (e.g. schema:CreativeWork, foaf:Person, skos:Concept)
        if cls:
            cls_uri = resolve_qname(cls)
            if cls_uri is not None:
                g.add((subj, RDF.type, cls_uri))

        # rdfs:label from the "label" column
        if label:
            g.add((subj, RDFS.label, Literal(label)))

        # optional sameAs
        if same_as:
            g.add((subj, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(same_as)))


# === STEP 2: LOAD TRIPLES ======================================

with TRIPLES_CSV.open(encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        subj_id  = (row.get("subject") or "").strip()
        pred_qn  = (row.get("predicate") or "").strip()
        obj_id   = (row.get("object") or "").strip()
        obj_type = (row.get("object_type") or "").strip().lower() or "iri"

        if not subj_id or not pred_qn or not obj_id:
            continue

        subj = id_to_uri.get(subj_id, RRR[subj_id])
        pred = resolve_qname(pred_qn)
        if pred is None:
            # you can print a warning here if you like:
            # print(f"Unknown predicate namespace: {pred_qn}")
            continue

        if obj_type == "iri":
            obj = id_to_uri.get(obj_id, RRR[obj_id])
        else:
            # fallback: treat as literal
            obj = Literal(obj_id)

        g.add((subj, pred, obj))


# === STEP 3: SERIALIZE =========================================

OUTPUT_TTL.parent.mkdir(parents=True, exist_ok=True)
g.serialize(OUTPUT_TTL, format="turtle")

print(f"RDF graph written to {OUTPUT_TTL} with {len(g)} triples.")
