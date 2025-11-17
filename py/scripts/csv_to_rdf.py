import pandas as pd
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# -----------------------------
# NAMESPACES
# -----------------------------

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

# -----------------------------
# GRAPH SETUP
# -----------------------------

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

# -----------------------------
# PREDICATE MAPPING (EDIT HERE)
# -----------------------------
# You assign which ontology property corresponds to each CSV column

predicate_map = {
    "Title": dcterms.title,
    "Alt Title": schema.alternateName,
    "Director": schema.director,
    "Screenwriter": schema.creator,
    "Country": schema.countryOfOrigin,
    "Language": dcterms.language,
    "Year": schema.datePublished,
    "Running Time": schema.duration,
    "Production Company": schema.productionCompany,
    "Subject": dcterms.subject,
    "Filming Location": schema.locationCreated,
    "Owner": schema.owner,
    "Collection": dcterms.isPartOf,
    "Format": dcterms.format,
    "Type": rdf_ns.type,
    # Add more as needed...
}

# -----------------------------
# CSV → RDF TRANSFORMATION
# -----------------------------

def csv_to_rdf(csv_path, base_uri, output_ttl):
    df = pd.read_csv(csv_path, keep_default_na=False)

    for idx, row in df.iterrows():

        subject_uri = URIRef(base_uri + str(idx))
        g.add((subject_uri, RDF.type, schema.CreativeWork))

        for col, value in row.items():
            if value == "" or value is None:
                continue

            if col in predicate_map:
                predicate = predicate_map[col]
            else:
                # Default fallback
                predicate = rrr[col.replace(" ", "_")]

            g.add((subject_uri, predicate, Literal(value)))

    g.serialize(destination=output_ttl, format="turtle")
    print(f"✔ RDF saved to {output_ttl}")

# -----------------------------
# EXAMPLE USE
# -----------------------------
# csv_to_rdf("csv/library.csv", rrr, "library.ttl")
# csv_to_rdf("csv/set_photo.csv", rrr, "set_photo.ttl")
# csv_to_rdf("csv/documentary.csv", rrr, "documentary.ttl")
