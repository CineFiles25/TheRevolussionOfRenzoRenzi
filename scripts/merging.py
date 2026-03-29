from rdflib import Graph, Namespace, URIRef
from pandas import read_csv
import glob
from pathlib import Path

# NAMESPACES
rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
owl = Namespace("http://www.w3.org/2002/07/owl#")

# Locate directories
script_path = Path(__file__).resolve()
ttl_dir = script_path.parents[1] / "ttl"
if not ttl_dir.is_dir():
    ttl_dir = script_path.parents[2] / "ttl"
csv_dir = script_path.parents[1] / "csv"

# Collect all TTL files except the merged output
ttl_files = sorted(
    f for f in glob.glob(str(ttl_dir / "*.ttl"))
    if not f.endswith("full_dataset.ttl")
)

merged_graph = Graph()
merged_graph.bind("rrr", rrr)
merged_graph.bind("owl", owl)

# Parse each TTL file
for ttl_file in ttl_files:
    merged_graph.parse(ttl_file, format="turtle")

# Add owl:sameAs triples from rrr_entities.csv
entities_csv = csv_dir / "rrr_entities.csv"
df = read_csv(str(entities_csv), keep_default_na=False, encoding="utf-8")

for _, row in df.iterrows():
    entity_id = row.get("id")
    same_as = row.get("sameAs")
    if entity_id and same_as:
        merged_graph.add((
            URIRef(rrr + entity_id),
            owl.sameAs,
            URIRef(same_as)
        ))

# Output path
output_path = ttl_dir / "full_dataset.ttl"

# Serialize merged graph
merged_graph.serialize(destination=str(output_path), format="turtle")
print(f"Merged {len(ttl_files)} files into {output_path}")
print(f"owl:sameAs triples added from rrr_entities.csv")
