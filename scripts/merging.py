from rdflib import Graph
import glob
from pathlib import Path

# Locate the ttl directory
script_path = Path(__file__).resolve()
ttl_dir = script_path.parents[1] / "ttl"
if not ttl_dir.is_dir():
    ttl_dir = script_path.parents[2] / "ttl"

# Collect all TTL files except the merged output
ttl_files = sorted(
    f for f in glob.glob(str(ttl_dir / "*.ttl"))
    if not f.endswith("full_dataset.ttl")
)

merged_graph = Graph()

# Parse each TTL file
for ttl_file in ttl_files:
    merged_graph.parse(ttl_file, format="turtle")

# Output path
output_path = ttl_dir / "full_dataset.ttl"

# Serialize merged graph
merged_graph.serialize(destination=str(output_path), format="turtle")

print(f"Merged {len(ttl_files)} files into {output_path}")
