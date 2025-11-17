import csv
from rdflib import Graph, Namespace, URIRef, Literal, RDF, XSD, OWL

# Namespace definitions (following your framework, with added fiaf for target TTL compatibility)
nsDict = {
    "renzi": Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage/"),
    "owl": Namespace("http://www.w3.org/2002/07/owl#"),
    "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
    "schema": Namespace("https://schema.org/"),
    "dc": Namespace("http://purl.org/dc/elements/1.1/"),
    "dcterms": Namespace("http://purl.org/dc/terms/"),
    "crm": Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "foaf": Namespace("http://xmlns.com/foaf/0.1/"),
    "fiaf": Namespace("https://fiaf.github.io/film-related-materials/objects/")  # Added for target TTL compliance
}

# Initialize RDF graph (reusing your function structure)
def init_graph():
    g = Graph()
    for prefix, ns in nsDict.items():
        g.bind(prefix, ns)
    return g

# Serialize graph to Turtle format (reusing your function)
def serialize_graph(graph, output_path):
    graph.serialize(destination=output_path, format="turtle")

# Process CSV file and generate RDF triples (core logic adapted to your CSV structure)
def process_csv_to_graph(csv_path, graph):
    # Read CSV file using csv module (matching your framework style)
    with open(csv_path, mode='r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 1. Generate unique URI for the artwork (normalize title to valid URI format)
            artwork_title = row["Title"].strip()
            artwork_slug = artwork_title.lower().replace(": ", "_").replace(" ", "_").replace('"', "").replace(",", "")
            artwork_uri = URIRef(nsDict["renzi"] + f"artwork_{artwork_slug}")
            
            # 2. Declare artwork type (map CSV "Object Type" to fiaf: type)
            object_type = row["Object Type"].strip()
            graph.add((artwork_uri, RDF.type, nsDict["fiaf"][object_type]))  # e.g., fiaf:Drawing
            
            # 3. Map core artwork properties (exact CSV column matches to target TTL predicates)
            graph.add((artwork_uri, nsDict["dcterms"]["title"], Literal(artwork_title)))
            graph.add((artwork_uri, nsDict["dcterms"]["description"], Literal(row["Description"].strip())))
            graph.add((artwork_uri, nsDict["fiaf"]["technique"], Literal(row["Technique"].strip())))
            graph.add((artwork_uri, nsDict["fiaf"]["support"], Literal(row["Support"].strip())))
            graph.add((artwork_uri, nsDict["fiaf"]["dimensions"], Literal(row["Dimensions"].strip())))
            graph.add((artwork_uri, nsDict["fiaf"]["collection"], Literal(row["Collection"].strip())))
            graph.add((artwork_uri, nsDict["dcterms"]["identifier"], Literal(row["URL"].strip())))
            
            # 4. Process Author as fiaf:Person entity (matching target TTL's Person handling)
            author_name = row["Author"].strip()
            author_slug = author_name.lower().replace(", ", "_").replace(" ", "_")
            author_uri = URIRef(nsDict["renzi"] + f"person_{author_slug}")
            
            # Declare author type and attributes
            graph.add((author_uri, RDF.type, nsDict["fiaf"]["Person"]))
            graph.add((author_uri, nsDict["dcterms"]["title"], Literal(author_name)))  # Follows Person naming in target TTL
            # Link artwork to its author
            graph.add((artwork_uri, nsDict["fiaf"]["author"], author_uri))

# Main function (integrates all logic for easy execution)
if __name__ == "__main__":
    # Configure file paths (modify these according to your actual setup)
    CSV_INPUT_PATH = "../csv/artworks.csv"
    TTL_OUTPUT_PATH = "../ttl/artworks.ttl"
    
    # Execute conversion workflow
    rdf_graph = init_graph()
    process_csv_to_graph(CSV_INPUT_PATH, rdf_graph)
    serialize_graph(rdf_graph, TTL_OUTPUT_PATH)
    
    print(f"CSV converted successfully! TTL file saved to: {TTL_OUTPUT_PATH}")
