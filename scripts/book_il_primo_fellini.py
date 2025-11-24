import pandas as pd
from pandas import read_csv
from rdflib import Namespace, Graph, RDF, URIRef, OWL, Literal, XSD, RDFS, FOAF

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
dbo = Namespace("http://dbpedia.org/ontology/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
fiaf = Namespace("https://fiaf.github.io/film-related-materials/objects/")

g = Graph()

ns_dict = {
    "rrr": rrr,
    "rdf": rdf,
    "rdfs": rdfs,
    "owl": owl,
    "schema": schema,
    "dc": dc,
    "dcterms": dcterms,
    "dbo": dbo,
    "crm": crm,
    "foaf": foaf,
    "fiaf": fiaf
}


def graph_bindings():
    """Bind all namespaces to the graph."""
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g


# ENTITIES (LOCAL RESOURCES)

# Main bibliographic resource (the book "Il primo Fellini")
first_fellini_book = URIRef(rrr + "first_fellini_book")

# Persons involved
federico_fellini = URIRef(rrr + "federico_fellini")
renzo_renzi = URIRef(rrr + "renzo_renzi")
liliana_betti = URIRef(rrr + "liliana_betti")
eschilo_tarquini = URIRef(rrr + "eschilo_tarquini")

# Publisher, place and related work
cappelli_editore = URIRef(rrr + "cappelli_editore")
bologna = URIRef(rrr + "bologna")
la_strada_1954 = URIRef(rrr + "la_strada_1954")

# CSV FILE

book_il_primo_fellini = pd.read_csv(
    "../csv/book_il_primo_fellini.csv",
    keep_default_na=False,
    encoding="utf-8"
    )

g = graph_bindings()

# MAP CSV ROWS TO RDF TRIPLES

for idx, row in book_il_primo_fellini.iterrows():
    # Language of the resource (e.g. "it")
    language = str(row["language"]).strip() if "language" in row and str(row["language"]).strip() else None

    # Types for main resource
    g.add((first_fellini_book, RDF.type, schema.Book))
    g.add((first_fellini_book, RDF.type, dcterms.BibliographicResource))

    # Identifier
    if row.get("id"):
        g.add((first_fellini_book, dc.identifier, Literal(row["id"])))

    # Descriptive standard (ISBD(G))
    if row.get("standard"):
        g.add((first_fellini_book, dcterms.conformsTo, Literal(row["standard"])))

    # Title proper
    if row.get("title_proper"):
        if language:
            g.add((first_fellini_book, dc.title, Literal(row["title_proper"], lang=language)))
        else:
            g.add((first_fellini_book, dc.title, Literal(row["title_proper"])))

    # Other title information (subtitle)
    if row.get("other_title_information"):
        if language:
            g.add((first_fellini_book, dcterms.alternative, Literal(row["other_title_information"], lang=language)))
        else:
            g.add((first_fellini_book, dcterms.alternative, Literal(row["other_title_information"])))

    # Statement of responsibility (kept as a free-text note on the book)
    if row.get("responsibility_statement"):
        g.add((first_fellini_book, rdfs.comment, Literal(row["responsibility_statement"])))

    # --- CREATOR AND CONTRIBUTORS ---

    # Local typing for persons
    g.add((federico_fellini, RDF.type, FOAF.Person))
    g.add((renzo_renzi, RDF.type, FOAF.Person))
    g.add((liliana_betti, RDF.type, FOAF.Person))
    g.add((eschilo_tarquini, RDF.type, FOAF.Person))

    # Attach creator name to local resource
    if row.get("creator"):
        g.add((federico_fellini, FOAF.name, Literal(row["creator"])))
        g.add((first_fellini_book, dc.creator, federico_fellini))

    # Attach contributors' names to local resources
    if row.get("other_contributors"):
        # Expected order: Renzo Renzi; Liliana Betti; Eschilo Tarquini
        contributor_names = [name.strip() for name in str(row["other_contributors"]).split(";") if name.strip()]
        local_contributors = [renzo_renzi, liliana_betti, eschilo_tarquini]

        for local_res, name in zip(local_contributors, contributor_names):
            g.add((local_res, FOAF.name, Literal(name)))
            g.add((first_fellini_book, dcterms.contributor, local_res))

    # External URIs for creator and contributors (linked with owl:sameAs)
    if row.get("creator_uri"):
        g.add((federico_fellini, OWL.sameAs, URIRef(row["creator_uri"])))

    if row.get("other_contributors_uri"):
        contributor_uris = [uri.strip() for uri in str(row["other_contributors_uri"]).split(";") if uri.strip()]
        local_contributors = [renzo_renzi, liliana_betti, eschilo_tarquini]
        for local_res, uri in zip(local_contributors, contributor_uris):
            g.add((local_res, OWL.sameAs, URIRef(uri)))

    # --- PUBLISHER, PLACE, YEAR ---

    # Place of publication
    if row.get("publication_place"):
        g.add((first_fellini_book, dcterms.spatial, Literal(row["publication_place"])))
        g.add((bologna, RDF.type, schema.Place))
        g.add((bologna, schema.name, Literal(row["publication_place"])))
        # Link book to the place resource
        g.add((first_fellini_book, schema.locationCreated, bologna))

    # Publisher (organization)
    if row.get("publisher"):
        g.add((cappelli_editore, RDF.type, FOAF.Organization))
        g.add((cappelli_editore, FOAF.name, Literal(row["publisher"])))
        g.add((first_fellini_book, dcterms.publisher, cappelli_editore))

    if row.get("publisher_uri"):
        g.add((cappelli_editore, OWL.sameAs, URIRef(row["publisher_uri"])))

    # Publication year
    if row.get("publication_year"):
        g.add(
            (
                first_fellini_book,
                schema.datePublished,
                Literal(str(row["publication_year"]), datatype=XSD.gYear)
            )
        )

    # Series (the book is part of a series)
    if row.get("series"):
        g.add((first_fellini_book, dcterms.isPartOf, Literal(row["series"])))

    # Extent (pages, illustrations, physical size)
    if row.get("extent"):
        g.add((first_fellini_book, dcterms.extent, Literal(row["extent"])))

    # General notes about the project/resource
    if row.get("notes"):
        g.add((first_fellini_book, dcterms.description, Literal(row["notes"])))

    # --- RELATED WORK (THE FILM "LA STRADA") ---

    if row.get("related_work"):
        g.add((la_strada_1954, RDF.type, schema.Movie))
        g.add((la_strada_1954, dc.title, Literal(row["related_work"])))
        # The book is about this work
        g.add((first_fellini_book, schema.about, la_strada_1954))

    if row.get("related_work_uri"):
        g.add((la_strada_1954, OWL.sameAs, URIRef(row["related_work_uri"])))

    # Relation type as a literal (e.g. "is_about")
    if row.get("work_relation_type"):
        g.add((first_fellini_book, dcterms.relation, Literal(row["work_relation_type"])))


# SERIALIZATION

g.serialize(format="turtle", destination="../ttl/book_il_primo_fellini.ttl")

print("CSV converted to TTL!")
