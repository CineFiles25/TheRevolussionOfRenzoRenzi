import pandas as pd
from rdflib import Namespace, Graph, RDF, URIRef, Literal

# Define namespaces (matching the prefixes in the target Turtle)
fiaf = Namespace("https://fiaf.github.io/film-related-materials/objects/")
dcterms = Namespace("http://purl.org/dc/terms/")
wd = Namespace("http://www.wikidata.org/entity/")

# Create an RDF graph
g = Graph()

# Bind namespace prefixes (to ensure the generated Turtle uses the specified prefixes)
ns_dict = {
    "fiaf": fiaf,
    "dcterms": dcterms,
    "wd": wd
}
for prefix, ns in ns_dict.items():
    g.bind(prefix, ns)

# Read the CSV file (assuming the CSV contains film and related person information)
# Assumed CSV column names: wikidata_id, title, originalTitle, director_wd_id, director_name, productionCompany, countryOfOrigin, language, yearOfFirstRelease, length, duration, gauge, color, sound, workType
films_df = pd.read_csv("../csv/films.csv", keep_default_na=False, encoding="utf-8")

# Iterate through each row of the CSV to generate RDF triples
for _, row in films_df.iterrows():
    # Film entity (using Wikidata ID, e.g., wd:Q174267)
    film = URIRef(wd + row["wikidata_id"])
    # Declare the film type as fiaf:Film
    g.add((film, RDF.type, fiaf.Film))
    
    # Map film attributes (corresponding to predicates in the target Turtle)
    g.add((film, dcterms.title, Literal(row["title"])))
    g.add((film, fiaf.originalTitle, Literal(row["originalTitle"])))
    
    # Director entity (using Wikidata ID, e.g., wd:Q13975)
    director = URIRef(wd + row["director_wd_id"])
    # Declare the director type as fiaf:Person
    g.add((director, RDF.type, fiaf.Person))
    # Director's name
    g.add((director, dcterms.title, Literal(row["director_name"])))
    # Associate the film with its director
    g.add((film, fiaf.director, director))
    
    # Other film attributes
    g.add((film, fiaf.productionCompany, Literal(row["productionCompany"])))
    g.add((film, fiaf.countryOfOrigin, Literal(row["countryOfOrigin"])))
    g.add((film, fiaf.language, Literal(row["language"])))
    g.add((film, fiaf.yearOfFirstRelease, Literal(row["yearOfFirstRelease"])))  # Add datatype=XSD.gYear if needed
    g.add((film, fiaf.length, Literal(row["length"])))
    g.add((film, fiaf.duration, Literal(row["duration"])))
    g.add((film, fiaf.gauge, Literal(row["gauge"])))
    g.add((film, fiaf.color, Literal(row["color"])))
    g.add((film, fiaf.sound, Literal(row["sound"])))
    g.add((film, fiaf.workType, Literal(row["workType"])))

# Serialize to Turtle format and save
g.serialize(format="turtle", destination="../ttl/films.ttl")

print("CSV converted and serialized to ../ttl/films.ttl")
