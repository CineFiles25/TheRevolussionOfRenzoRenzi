from rdflib import Graph
import glob
from pathlib import Path

def validate_ttl_files():
    script_path = Path(__file__).resolve()
    ttl_dir = script_path.parents[1] / "ttl"

    ttl_files = sorted(
        f for f in glob.glob(str(ttl_dir / "*.ttl"))
        if not f.endswith("full_dataset.ttl")
    )

    print(f"Validating {len(ttl_files)} TTL files...\n")

    for ttl in ttl_files:
        g = Graph()
        try:
            g.parse(ttl, format="turtle")
            print(f"✔ VALID: {Path(ttl).name}")
        except Exception as e:
            print(f"❌ ERROR in {Path(ttl).name}")
            print(f"   {e}\n")

if __name__ == "__main__":
    validate_ttl_files()
