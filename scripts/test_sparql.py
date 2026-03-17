from rdflib import Graph

# Carica il dataset completo
g = Graph()
g.parse("../ttl/full_dataset.ttl", format="turtle")

print(f"Dataset caricato con {len(g)} triple.\n")

# Funzione helper per eseguire query
def run_query(label, query):
    print(f"=== {label} ===")
    results = g.query(query)
    for row in results:
        print(row)
    print("\n")


# -------------------------
# TEST B1 — Query di base
# -------------------------

run_query(
    "B1.1 — Tutte le risorse con un tipo",
    """
    SELECT ?res ?type WHERE {
        ?res a ?type .
    }
    LIMIT 20
    """
)

run_query(
    "B1.2 — Tutte le fotografie",
    """
    SELECT ?photo WHERE {
        ?photo a <https://schema.org/Photograph> .
    }
    """
)

run_query(
    "B1.3 — Tutte le opere di Renzo Renzi",
    """
    SELECT ?work WHERE {
        ?work <http://purl.org/dc/terms/creator> <https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/renzo_renzi> .
    }
    """
)


# -------------------------
# TEST B2 — Navigazione
# -------------------------

run_query(
    "B2.1 — Fotografie collegate al film La Strada",
    """
    SELECT ?photo WHERE {
        ?photo <http://purl.org/dc/terms/relation> <https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/la_strada_film> .
    }
    """
)

run_query(
    "B2.2 — Luoghi associati alla fotografia 'photo_la_strada_woman'",
    """
    SELECT ?place WHERE {
        <https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/photo_la_strada_woman>
            <https://schema.org/location> ?place .
    }
    """
)

run_query(
    "B2.3 — Film citati nel libro 'Il primo Fellini'",
    """
    SELECT ?film WHERE {
        <https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/book_il_primo_fellini>
            <http://purl.org/dc/terms/relation> ?film .
    }
    """
)


# -------------------------
# TEST B3 — Coerenza interna
# -------------------------

run_query(
    "B3.1 — Risorse senza rdf:type",
    """
    SELECT ?res WHERE {
        ?res ?p ?o .
        FILTER NOT EXISTS { ?res a ?type . }
    }
    """
)

run_query(
    "B3.2 — Titoli duplicati",
    """
    SELECT ?title (COUNT(*) AS ?count) WHERE {
        ?s <http://purl.org/dc/terms/title> ?title .
    }
    GROUP BY ?title
    HAVING (?count > 1)
    """
)

run_query(
    "B3.3 — Anni non numerici",
    """
    SELECT ?work ?year WHERE {
        ?work <http://purl.org/dc/terms/issued> ?year .
        FILTER (!regex(str(?year), "^[0-9]{4}$"))
    }
    """
)
