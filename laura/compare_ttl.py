#!/usr/bin/env python3
"""
compare_ttl.py

Confronta due file Turtle e verifica se descrivono
lo stesso grafo RDF (a livello di triple), ignorando
l'ordine delle righe e i dettagli di serializzazione.
"""

from rdflib import Graph
from pathlib import Path
import sys


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def main():
    if len(sys.argv) != 3:
        print("Uso: python compare_ttl.py file1.ttl file2.ttl")
        sys.exit(1)

    path1 = Path(sys.argv[1])
    path2 = Path(sys.argv[2])

    if not path1.exists():
        print(f"❌ File non trovato: {path1}")
        sys.exit(1)
    if not path2.exists():
        print(f"❌ File non trovato: {path2}")
        sys.exit(1)

    print(f"[INFO] Carico {path1}")
    g1 = load_graph(path1)

    print(f"[INFO] Carico {path2}")
    g2 = load_graph(path2)

    print("[INFO] Confronto i due grafi RDF…")
    if g1.isomorphic(g2):
        print("✅ I due file descrivono lo STESSO grafo (sono isomorfi).")
    else:
        print("⚠️ I due file NON sono lo stesso grafo (non isomorfi).")
        print("    (controlla se hai cambiato qualche tripla o URI)")


if __name__ == "__main__":
    main()
