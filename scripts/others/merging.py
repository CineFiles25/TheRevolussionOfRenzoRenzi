from rdflib import Graph
import glob
from pathlib import Path


script_path = Path(__file__).resolve()
ttl_dir = script_path.parents[1] / "ttl"
if not ttl_dir.is_dir():
    ttl_dir = script_path.parents[2] / "ttl"
ttl_files = glob.glob(str(ttl_dir / "*.ttl"))

merged_graph = Graph()
for ttl_file in ttl_files:
    merged_graph.parse(ttl_file, format="turtle")

output_path = ttl_dir / "full_dataset.ttl"
merged_graph.serialize(destination=str(output_path), format="turtle")

print(f"Merged {len(ttl_files)} files into {output_path}")