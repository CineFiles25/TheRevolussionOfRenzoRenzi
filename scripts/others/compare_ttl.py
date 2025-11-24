import sys
from pathlib import Path

from rdflib import Graph


def load_graph(path: Path) -> Graph:
    """Load a Turtle file into an rdflib Graph."""
    g = Graph()
    g.parse(path, format="turtle")
    return g


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python scripts/compare_ttl.py path/to/first.ttl path/to/second.ttl")
        return 1

    first_path = Path(sys.argv[1])
    second_path = Path(sys.argv[2])

    if not first_path.exists():
        print(f"[ERROR] File not found: {first_path}")
        return 1
    if not second_path.exists():
        print(f"[ERROR] File not found: {second_path}")
        return 1

    print(f"[INFO] Loading first graph:  {first_path}")
    g1 = load_graph(first_path)
    print(f"[INFO] Loading second graph: {second_path}")
    g2 = load_graph(second_path)

    set1 = set(g1)
    set2 = set(g2)

    only_in_first = set1 - set2
    only_in_second = set2 - set1

    print()
    print("=== SUMMARY ===")
    print(f"Triples in first:  {len(set1)}")
    print(f"Triples in second: {len(set2)}")
    print(f"Only in first:     {len(only_in_first)}")
    print(f"Only in second:    {len(only_in_second)}")
    print()

    if not only_in_first and not only_in_second:
        print("[OK] Graphs are identical (same set of triples).")
        return 0

    # Print details (limited, but enough for debugging)
    if only_in_first:
        print("=== Triples only in FIRST graph ===")
        for s, p, o in sorted(only_in_first, key=lambda t: (str(t[0]), str(t[1]), str(t[2]))):
            print(f"- {s} {p} {o}")
        print()

    if only_in_second:
        print("=== Triples only in SECOND graph ===")
        for s, p, o in sorted(only_in_second, key=lambda t: (str(t[0]), str(t[1]), str(t[2]))):
            print(f"+ {s} {p} {o}")
        print()

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
