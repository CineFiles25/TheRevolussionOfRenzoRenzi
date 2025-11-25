import csv
import re
import requests
from io import StringIO

# ------------ configuration ------------

# GitHub raw URL of your Scheda F CSV
GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/"
    "CineFiles25/TheRevolussionOfRenzoRenzi/refs/heads/main/"
    "csv/%E2%80%9Cla_strada_004%E2%80%9D%20(woman).csv"
)

# Output TTL file name
OUTPUT_TTL = "la_strada_004_woman.ttl"

PREFIXES = """@prefix rrr:  <https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/> .
@prefix sf:   <https://iccd.beniculturali.it/scheda-f/> .
@prefix dct:  <http://purl.org/dc/terms/> .
@prefix dc:   <http://purl.org/dc/elements/1.1/> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

"""

# CSV column -> property IRI (literal properties on the photo)
COLUMN_TO_PROPERTY = {
    "standard": "sf:standard",
    "title": "dct:title",
    "other_title_information": "dct:alternative",
    "photographer": "dct:creator",
    "depicted_event": "dct:subject",
    "depicted_people": "dct:subject",
    "depicted_place": "dct:spatial",
    "creation_year": "dct:created",
    "colour": "sf:colour",
    "material_technique": "dct:medium",
    "inventory_number": "sf:inventoryNumber",
    "collection": "dct:isPartOf",
    "carrier_type": "sf:carrierType",
    "physical_description": "dct:extent",
    "notes": "dct:description",
    "identifiers": "dct:identifier",
    "related_works": "sf:relatedWork",
    "rights": "dct:rights",
    "resource_type": "dct:type",
    "language": "dct:language",
}

# URI columns and the properties used to link the photo to authority nodes
URI_LINK_PROPERTIES = {
    "photographer_uri": "sf:photographerRef",
    "depicted_people_uri": "sf:depictedPersonRef",
    "depicted_event_uri": "sf:depictedEventRef",
    "depicted_place_uri": "sf:depictedPlaceRef",
    "related_works_uri": "sf:relatedWorkRef",
}

# Type of authority node for each URI column
URI_AUTH_TYPES = {
    "photographer_uri": "sf:Photographer",
    "depicted_people_uri": "sf:Person",
    "depicted_event_uri": "sf:Event",
    "depicted_place_uri": "sf:Place",
    "related_works_uri": "sf:Work",
}

# ------------ helpers ------------

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "item"

def escape_literal(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
    )

# ------------ main conversion ------------

def convert_from_github_csv(github_url: str, output_ttl: str) -> None:
    print(f"Fetching CSV from GitHub:\n{github_url}\n")
    response = requests.get(github_url)
    response.raise_for_status()

    csv_text = response.text
    reader = csv.DictReader(StringIO(csv_text))
    rows = list(reader)

    print(f"Read {len(rows)} row(s) from CSV.\n")

    # Collect authority nodes: key = local id, value = dict(label, uri, type)
    authorities = {}

    with open(output_ttl, "w", encoding="utf-8") as out:
        out.write(PREFIXES)

        # Minimal schema
        out.write("\n### Schema (Scheda F) ###\n\n")
        out.write("sf:Photograph a owl:Class ;\n")
        out.write('    dc:title "Photograph (Scheda F resource)"@en .\n\n')

        for c in ["Photographer", "Person", "Event", "Place", "Work"]:
            out.write(f"sf:{c} a owl:Class .\n")
        out.write("\n")

        out.write("### Instances ###\n\n")

        for row in rows:
            row_id = (row.get("id") or "").strip()
            if not row_id:
                continue

            inst_id = slugify(row_id)
            out.write(f"rrr:{inst_id} a sf:Photograph ;\n")

            triples = []

            # Literal properties
            for col, prop in COLUMN_TO_PROPERTY.items():
                value = (row.get(col) or "").strip()
                if not value:
                    continue
                lit = escape_literal(value)
                triples.append(f'    {prop} "{lit}"')

            # URI / authority links
            for uri_col, link_prop in URI_LINK_PROPERTIES.items():
                uris_value = (row.get(uri_col) or "").strip()
                if not uris_value:
                    continue

                names_col = uri_col.replace("_uri", "")
                names_value = (row.get(names_col) or "").strip()

                uri_list = [u.strip() for u in uris_value.split(";") if u.strip()]
                name_list = [n.strip() for n in names_value.split(";")] if names_value else []

                for idx, uri in enumerate(uri_list):
                    label = name_list[idx] if idx < len(name_list) else uri
                    auth_slug = slugify(label if label else uri)
                    auth_ref = f"rrr:{auth_slug}"

                    triples.append(f"    {link_prop} {auth_ref}")

                    if auth_slug not in authorities:
                        authorities[auth_slug] = {
                            "label": label,
                            "uri": uri,
                            "type": URI_AUTH_TYPES.get(uri_col, "owl:Thing"),
                        }

            if triples:
                out.write(" ;\n".join(triples))
                out.write(" .\n\n")
            else:
                out.write(" .\n\n")

        # Authority entities
        if authorities:
            out.write("### Authority entities ###\n\n")
            for auth_id, data in authorities.items():
                label = escape_literal(data["label"])
                uri = data["uri"]
                auth_type = data["type"]
                out.write(f"rrr:{auth_id} a {auth_type} ;\n")
                out.write(f'    dct:title "{label}" ;\n')
                out.write(f"    owl:sameAs <{uri}> .\n\n")

    print(f"Conversion completed. TTL written to: {output_ttl}")

if __name__ == "__main__":
    convert_from_github_csv(GITHUB_CSV_URL, OUTPUT_TTL)
