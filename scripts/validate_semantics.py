from rdflib import Graph, URIRef
from rdflib.namespace import RDF
from pathlib import Path

def validate_semantics():
    ttl_path = Path("../ttl/full_dataset.ttl")

    print(f"Loading dataset: {ttl_path}")
    g = Graph()
    g.parse(ttl_path, format="turtle")

    print(f"Total triples: {len(g)}\n")

    # --- 1. SUBJECTS AND OBJECTS ---
    subjects = set(g.subjects())
    objects = set(g.objects())

    # Only consider URIRefs (ignore literals)
    subject_uris = {s for s in subjects if isinstance(s, URIRef)}
    object_uris = {o for o in objects if isinstance(o, URIRef)}

    # --- 2. UNDEFINED RESOURCES ---
    undefined = object_uris - subject_uris

    print("=== Undefined resources (used but never defined) ===")
    for uri in sorted(undefined):
        print(f"⚠ {uri}")
    if not undefined:
        print("✔ No undefined resources found.")
    print()

    # --- 3. ENTITIES WITH NO TYPE ---
    print("=== Resources with no rdf:type ===")
    no_type = []
    for s in subject_uris:
        if not list(g.objects(s, RDF.type)):
            no_type.append(s)

    for uri in sorted(no_type):
        print(f"⚠ {uri}")
    if not no_type:
        print("✔ All resources have a type.")
    print()

    # --- 4. ISOLATED NODES ---
    print("=== Isolated resources (no incoming or outgoing edges) ===")
    isolated = []
    for uri in subject_uris:
        outgoing = list(g.predicate_objects(uri))
        incoming = list(g.subject_predicates(uri))
        if not outgoing and not incoming:
            isolated.append(uri)

    for uri in sorted(isolated):
        print(f"⚠ {uri}")
    if not isolated:
        print("✔ No isolated resources.")
    print()

    # --- 5. SUSPICIOUS PROPERTIES ---
    print("=== Suspicious properties (possible typos) ===")
    suspicious = []
    for p in g.predicates():
        if "colour" in str(p) or "locationCreated" in str(p) or "spatial" in str(p):
            suspicious.append(p)

    for p in sorted(set(suspicious)):
        print(f"⚠ {p}")
    if not suspicious:
        print("✔ No suspicious properties detected.")
    print()

if __name__ == "__main__":
    validate_semantics()
