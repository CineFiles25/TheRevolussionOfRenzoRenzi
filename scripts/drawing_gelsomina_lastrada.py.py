import csv
import re
import requests
from io import StringIO

# GitHub raw URL of the drawing CSV file
GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/"
    "CineFiles25/TheRevolussionOfRenzoRenzi/main/"
    "csv/drawing_gelsomina_lastrada.csv"
)

# Output TTL file name
OUTPUT_TTL = "drawing_gelsomina_lastrada.ttl"

# RDF prefixes to be written at the top of the TTL file
PREFIXES = """@prefix rrr: <https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/> .
@prefix oa: <https://iccd.beniculturali.it/it/ricercanormative/29/oa-opere-oggetti-d-arte-3_00#> .
@prefix iccd: <https://iccd.beniculturali.it/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

"""

# Mapping from CSV column names to RDF properties
COLUMN_TO_PROPERTY = {
    "Title": "dc:title",
    "Author": "dc:creator",
    "Description": "dc:description",
    "Technique": "dcterms:medium",
    "Support": "dcterms:material",
    "Dimensions": "dcterms:extent",
    "Collection": "dcterms:isPartOf",
    "URL": "dcterms:identifier",
}

# Authority file: label -> external authority URI
AUTHORITY_URIS = {
    "Renzo Renzi": "http://viaf.org/viaf/40486517",
    "Bologna": "http://viaf.org/viaf/257723025",
    "Cineteca di Bologna": "http://viaf.org/viaf/124960346",
    "Federico Fellini": "http://viaf.org/viaf/76315386",
}

# Convert text to a URI-safe identifier
def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "item"

# Escape special characters in Turtle string literals
def escape_literal(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
    )

# Main conversion function
def convert_from_github_csv(github_url: str, output_ttl: str) -> None:
    print(f"Fetching CSV from GitHub:\n{github_url}\n")

    response = requests.get(github_url)
    response.raise_for_status()

    csv_text = response.text
    rows = list(csv.DictReader(StringIO(csv_text)))

    print(f"Read {len(rows)} data row(s) from CSV (excluding header).\n")

    used_authority_labels = set()

    with open(output_ttl, "w", encoding="utf-8") as out:
        # Write prefixes
        out.write(PREFIXES + "\n")

        for idx, row in enumerate(rows, start=1):
            title = (row.get("Title") or "").strip()
            instance_id = slugify(title) if title else f"drawing-{idx}"

            object_type = (row.get("Object Type") or "").strip()
            if object_type:
                class_name = slugify(object_type).capitalize()
                rdf_type = f"oa:{class_name}"
            else:
                rdf_type = "oa:Artwork"

            out.write(f"### Drawing #{idx}\n")
            out.write(f"rrr:{instance_id} a {rdf_type} ;\n")

            triples = []
            linked_authority_slugs = set()

            # Literal properties
            for column_name, property_iri in COLUMN_TO_PROPERTY.items():
                value = (row.get(column_name) or "").strip()
                if not value:
                    continue

                if column_name == "URL":
                    triples.append(f"    {property_iri} <{value}>")
                else:
                    literal = escape_literal(value)
                    triples.append(f'    {property_iri} "{literal}"')

                # Check for any authority label as substring in this value
                for label, uri in AUTHORITY_URIS.items():
                    if label in value:
                        auth_slug = slugify(label)
                        linked_authority_slugs.add(auth_slug)
                        used_authority_labels.add(label)

            # Link the drawing to authority entities
            for auth_slug in linked_authority_slugs:
                triples.append(f"    dcterms:relation rrr:{auth_slug}")

            if triples:
                out.write(" ;\n".join(triples))
                out.write(" .\n\n")
            else:
                out.write(" .\n\n")

        # Write authority entities that were actually used
        if used_authority_labels:
            out.write("### Authority entities ###\n\n")
            for label in sorted(used_authority_labels):
                uri = AUTHORITY_URIS[label]
                auth_slug = slugify(label)
                title_literal = escape_literal(label)
                out.write(f"rrr:{auth_slug} owl:sameAs <{uri}> ;\n")
                out.write(f'    dcterms:title "{title_literal}" .\n\n')

    print(f"Conversion completed. TTL written to: {output_ttl}")

# Script entry point
if __name__ == "__main__":
    convert_from_github_csv(GITHUB_CSV_URL, OUTPUT_TTL)

