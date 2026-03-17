from rdflib import Graph

# Carica il dataset completo
g = Graph()
g.parse("../ttl/full_dataset.ttl", format="turtle")

print(f"Dataset caricato con {len(g)} triple.\n")

def run_query(label, query):
    print(f"=== {label} ===")
    results = g.query(query)
    for row in results:
        print(row)
    print("\n")


# ---------------------------------------------------------
# C1 — COERENZA DELLE ENTITÀ
# ---------------------------------------------------------

# C1.1 — Persone che non hanno opere collegate
run_query(
    "C1.1 — Persone senza opere collegate",
    """
    SELECT ?person WHERE {
        ?person a <http://xmlns.com/foaf/0.1/Person> .
        FILTER NOT EXISTS { ?work ?p ?person . }
    }
    """
)

# C1.2 — Fotografie senza creator né depicted persons
run_query(
    "C1.2 — Fotografie senza creator o depicted persons",
    """
    SELECT ?photo WHERE {
        ?photo a <https://schema.org/Photograph> .
        FILTER NOT EXISTS { ?photo <http://purl.org/dc/terms/creator> ?c . }
        FILTER NOT EXISTS { ?photo <http://xmlns.com/foaf/0.1/depicts> ?d . }
    }
    """
)

# C1.3 — Opere senza titolo
run_query(
    "C1.3 — Opere senza titolo",
    """
    SELECT ?work WHERE {
        ?work a ?type .
        FILTER NOT EXISTS { ?work <http://purl.org/dc/terms/title> ?title . }
    }
    """
)


# ---------------------------------------------------------
# C2 — COERENZA DELLE RELAZIONI
# ---------------------------------------------------------

# C2.1 — Relazioni schema:about che puntano a entità non esistenti
run_query(
    "C2.1 — schema:about verso risorse non definite",
    """
    SELECT ?work ?target WHERE {
        ?work <https://schema.org/about> ?target .
        FILTER NOT EXISTS { ?target ?p ?o . }
    }
    """
)

# C2.2 — dcterms:relation usato in modo incoerente (literals invece di risorse)
run_query(
    "C2.2 — dcterms:relation con literal (errore concettuale)",
    """
    SELECT ?s ?lit WHERE {
        ?s <http://purl.org/dc/terms/relation> ?lit .
        FILTER(isLiteral(?lit))
    }
    """
)

# C2.3 — foaf:depicts usato con literal (errore concettuale)
run_query(
    "C2.3 — foaf:depicts con literal",
    """
    SELECT ?photo ?lit WHERE {
        ?photo <http://xmlns.com/foaf/0.1/depicts> ?lit .
        FILTER(isLiteral(?lit))
    }
    """
)


# ---------------------------------------------------------
# C3 — COERENZA TEMPORALE
# ---------------------------------------------------------

# C3.1 — Fotografie datate dopo la morte delle persone ritratte
run_query(
    "C3.1 — Fotografie scattate dopo la morte dei depicted",
    """
    SELECT ?photo ?year ?person WHERE {
        ?photo a <https://schema.org/Photograph> ;
               <http://purl.org/dc/terms/created> ?year ;
               <http://xmlns.com/foaf/0.1/depicts> ?person .

        ?person <http://purl.org/dc/terms/date> ?death .

        FILTER(xsd:gYear(?year) > xsd:gYear(?death))
    }
    """
)

# C3.2 — Opere con anno precedente alla nascita dell’autore
run_query(
    "C3.2 — Opere create prima della nascita dell’autore",
    """
    SELECT ?work ?year ?author WHERE {
        ?work <http://purl.org/dc/terms/created> ?year ;
              <http://purl.org/dc/terms/creator> ?author .

        ?author <http://purl.org/dc/terms/date> ?birth .

        FILTER(xsd:gYear(?year) < xsd:gYear(?birth))
    }
    """
)


# ---------------------------------------------------------
# C4 — COERENZA GEOGRAFICA
# ---------------------------------------------------------

# C4.1 — Luoghi usati come literal invece che come risorsa
run_query(
    "C4.1 — Luoghi come literal (incoerenza)",
    """
    SELECT ?s ?place WHERE {
        ?s <https://schema.org/location> ?place .
        FILTER(isLiteral(?place))
    }
    """
)

# C4.2 — Risorse schema:Place senza coordinate o descrizione
run_query(
    "C4.2 — Luoghi senza informazioni aggiuntive",
    """
    SELECT ?place WHERE {
        ?place a <https://schema.org/Place> .
        FILTER NOT EXISTS { ?place <https://schema.org/address> ?a . }
        FILTER NOT EXISTS { ?place <https://schema.org/geo> ?g . }
        FILTER NOT EXISTS { ?place <http://purl.org/dc/terms/description> ?d . }
    }
    """
)


# ---------------------------------------------------------
# C5 — COERENZA CSV → RDF
# ---------------------------------------------------------

# C5.1 — Campi CSV non mappati (titoli multipli)
run_query(
    "C5.1 — Opere con più di un titolo (possibile errore CSV)",
    """
    SELECT ?work (COUNT(?title) AS ?count) WHERE {
        ?work <http://purl.org/dc/terms/title> ?title .
    }
    GROUP BY ?work
    HAVING (?count > 1)
    """
)

# C5.2 — Opere senza alcun metadato oltre al tipo
run_query(
    "C5.2 — Opere con solo rdf:type (incomplete)",
    """
    SELECT ?work WHERE {
        ?work a ?type .
        FILTER NOT EXISTS { ?work ?p ?o . FILTER(?p != rdf:type) }
    }
    """
)
