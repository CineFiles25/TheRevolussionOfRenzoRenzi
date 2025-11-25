import csv
import re
import requests
from io import StringIO

# GitHub raw URL of the CSV file
GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/CineFiles25/TheRevolussionOfRenzoRenzi/refs/heads/main/csv/lastrada_movie.csv"
)

# Output TTL file name
OUTPUT_TTL = "lastrada_movie.ttl"

# RDF prefixes to be written at the top of the TTL file
PREFIXES = """@prefix rrr: <https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/> .
@prefix fiaf: <https://fiaf.github.io/film-related-materials/objects/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix wd: <http://www.wikidata.org/entity/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

"""

# Mapping from CSV column names to RDF properties
COLUMN_TO_PROPERTY = {
    "Original Title": "dcterms:title",
    "National Title (in Italy)": "dcterms:alternative",
    "Director": "dcterms:creator",
    "Production Company / Sponsor": "dcterms:publisher",
    "Country of Origin": "dcterms:spatial",
    "Language": "dcterms:language",
    "Year of First Public Release": "dcterms:issued",
    "Length": "dcterms:extent",
    "Duration": "dcterms:extent",
    "Gauge / Format": "dcterms:format",
    "Colour": "dcterms:format",
    "Sound": "dcterms:format",
    "Work Type": "dcterms:type",
}

# Authority file: label -> external authority URI (VIAF in your case)
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

# Turn a slug into a CamelCase class name, e.g. "fiction-film" -> "FictionFilm"
def camelize_slug(slug: str) -> str:
    parts = slug.split("-")
    return "".join(part.capitalize() for part in parts if part)

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

    # Track which authority labels are actually used in the data
    used_authority_labels = set()

    with open(output_ttl, "w", encoding="utf-8") as out:
        # Write prefixes
        out.write(PREFIXES + "\n")

        for idx, row in enumerate(rows, start=1):
            # Use Original Title to build the instance identifier
            original_title = (row.get("Original Title") or "").strip()
            instance_id = slugify(original_title) if original_title else f"movie-{idx}"

            # Use Work Type to derive a FIAF class, e.g. "Fiction (film)" -> fiaf:FictionFilm
            work_type = (row.get("Work Type") or "").strip()
            if work_type:
                work_slug = slugify(work_type)
                class_name = camelize_slug(work_slug)
                rdf_type = f"fiaf:{class_name}"
            else:
                rdf_type = "fiaf:Film"

            out.write(f"### Film work #{idx}\n")
            out.write(f"rrr:{instance_id} a {rdf_type} ;\n")

            triples = []
            row_authority_slugs = set()

            # Regular literal properties
            for column_name, property_iri in COLUMN_TO_PROPERTY.items():
                value = (row.get(column_name) or "").strip()
                if not value:
                    continue

                literal = escape_literal(value)
                triples.append(f'    {property_iri} "{literal}"')

                # Check if this literal matches any authority label
                if value in AUTHORITY_URIS:
                    auth_slug = slugify(value)
                    row_authority_slugs.add(auth_slug)
                    used_authority_labels.add(value)

            # Link the film to authority entities (generic relation)
            for auth_slug in row_authority_slugs:
                triples.append(f"    dcterms:relation rrr:{auth_slug}")

            if triples:
                out.write(" ;\n".join(triples))
                out.write(" .\n\n")
            else:
                out.write(" .\n\n")

        # Write authority entities at the end
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

