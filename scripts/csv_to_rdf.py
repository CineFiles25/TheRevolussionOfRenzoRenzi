import pandas as pd
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD
import os
import re

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage/")
rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
fiaf = Namespace("https://fiaf.github.io/film-related-materials/objects/")

# GRAPH SETUP

g = Graph()

ns_dict = {
    "rrr": rrr,   
    "rdf": rdf_ns,
    "rdfs": rdfs,
    "owl": owl,
    "schema": schema,
    "dc": dc,
    "dcterms": dcterms,
    "crm": crm,
    "foaf": foaf,
    "fiaf": fiaf
}

for prefix, ns in ns_dict.items():
    g.bind(prefix, ns)

# CSV → RDF TRANSFORMATION

def csv_to_rdf(csv_path, base_uri, output_ttl):
    """Convert CSV file to RDF Turtle format"""
    df = pd.read_csv(csv_path, keep_default_na=False, encoding="utf-8")
    
    for idx, row in df.iterrows():
        # Create unique subject URI for each row
        row_id = row.get('Id') or row.get('Title') or f"item_{idx}"
        subject = URIRef(base_uri + slugify(row_id))
        
        # Add basic type
        g.add((subject, RDF.type, URIRef(schema + "Thing")))
        
        # Convert each column to RDF property
        for column, value in row.items():
            if value and str(value).strip():  # Skip empty values
                predicate = URIRef(rrr + slugify(column))
                
                # Try to detect datatype
                if column.lower() in ['year', 'date']:
                    try:
                        if len(str(value)) == 4 and str(value).isdigit():
                            g.add((subject, predicate, Literal(value, datatype=XSD.gYear)))
                        else:
                            g.add((subject, predicate, Literal(value)))
                    except:
                        g.add((subject, predicate, Literal(value)))
                elif column.lower() in ['url', 'website']:
                    g.add((subject, predicate, Literal(value, datatype=XSD.anyURI)))
                elif column.lower() in ['area', 'size', 'width', 'height']:
                    try:
                        g.add((subject, predicate, Literal(float(value), datatype=XSD.float)))
                    except:
                        g.add((subject, predicate, Literal(value)))
                elif column.lower() in ['seats', 'count', 'number']:
                    try:
                        g.add((subject, predicate, Literal(int(value), datatype=XSD.integer)))
                    except:
                        g.add((subject, predicate, Literal(value)))
                else:
                    g.add((subject, predicate, Literal(value)))
    
    # Serialize to Turtle
    g.serialize(format="turtle", destination=output_ttl)
    print(f"Converted {csv_path} to {output_ttl}")

# EXAMPLE USE
if __name__ == "__main__":
    # Convert set_photo.csv
    csv_to_rdf(
        csv_path="../csv/set_photo.csv",
        base_uri="https://github.com/CineFiles25/informational-science-and-cultural-heritage/set_photo/",
        output_ttl="../ttl/set_photo.ttl"
    )
    
    # Convert other CSV files
    csv_to_rdf(
        csv_path="../csv/library.csv", 
        base_uri="https://github.com/CineFiles25/informational-science-and-cultural-heritage/library/",
        output_ttl="../ttl/library.ttl"
    )
    
    csv_to_rdf(
        csv_path="../csv/documentary.csv",
        base_uri="https://github.com/CineFiles25/informational-science-and-cultural-heritage/documentary/", 
        output_ttl="../ttl/documentary.ttl"
    )
    
    print("All CSV files converted to RDF Turtle format!")
