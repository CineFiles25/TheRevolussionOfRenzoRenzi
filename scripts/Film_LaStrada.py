import pandas as pd
from rdflib import Namespace, Graph, RDF, URIRef, Literal

# Define namespaces (matching the target Turtle format)
fiaf = Namespace("https://fiaf.github.io/film-related-materials/objects/")
dcterms = Namespace("http://purl.org/dc/terms/")
renzi = Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage/")  # Custom namespace for entities without Wikidata IDs
foaf = Namespace("http://xmlns.com/foaf/0.1/")

# Create RDF graph
g = Graph()

# Bind namespace prefixes
ns_dict = {
    "fiaf": fiaf,
    "dcterms": dcterms,
    "renzi": renzi,
    "foaf": foaf
}
for prefix, ns in ns_dict.items():
    g.bind(prefix, ns)

# Read the provided CSV (using exact column names from your input)
films_df = pd.read_csv(
    "../csv/films.csv",  # Replace with your actual CSV path
    keep_default_na=False,
    encoding="utf-8"
)

# Process each row in CSV
for _, row in films_df.iterrows():
    # Create unique URI for the film (using original title to avoid duplicates)
    # Replace special characters to make valid URI
    film_slug = row["Original Title"].lower().replace(", ", "_").replace(" ", "_").replace("'", "")
    film = URIRef(renzi + f"film_{film_slug}")
    
    # Declare film type
    g.add((film, RDF.type, fiaf.Film))
    
    # Map core film attributes (exact column matches)
    g.add((film, dcterms.title, Literal(row["National Title (in Italy)"])))  # National title in Italy
    g.add((film, fiaf.originalTitle, Literal(row["Original Title"])))       # Original title
    g.add((film, fiaf.productionCompany, Literal(row["Production Company / Sponsor"])))  # Production company
    g.add((film, fiaf.countryOfOrigin, Literal(row["Country of Origin"])))  # Country of origin
    g.add((film, fiaf.language, Literal(row["Language"])))                  # Language
    g.add((film, fiaf.yearOfFirstRelease, Literal(row["Year of First Public Release"])))  # Release year
    g.add((film, fiaf.length, Literal(row["Length"])))                      # Length (e.g., 3220 mt)
    g.add((film, fiaf.duration, Literal(row["Duration"])))                  # Duration (e.g., 108)
    g.add((film, fiaf.gauge, Literal(row["Gauge / Format"])))                # Gauge/Format (e.g., 35)
    g.add((film, fiaf.color, Literal(row["Colour"])))                        # Colour (e.g., B/N)
    g.add((film, fiaf.sound, Literal(row["Sound"])))                          # Sound (e.g., Sonoro)
    g.add((film, fiaf.workType, Literal(row["Work Type"])))                  # Work type (e.g., Fiction)
    
    # Process director as a Person entity (since target Turtle uses entity for director)
    director_name = row["Director"]
    director_slug = director_name.lower().replace(", ", "_").replace(" ", "_")
    director = URIRef(renzi + f"person_{director_slug}")
    
    # Declare director type and attributes
    g.add((director, RDF.type, fiaf.Person))
    g.add((director, foaf.name, Literal(director_name)))  # Use foaf:name for person name
    g.add((film, fiaf.director, director))                # Link film to director

# Serialize to Turtle
g.serialize(format="turtle", destination="../ttl/films.ttl")

print("CSV converted and serialized to ../ttl/films.ttl")
