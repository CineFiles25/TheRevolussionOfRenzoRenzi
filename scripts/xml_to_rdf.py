import xml.etree.ElementTree as ET
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD

# NAMESPACES
rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
owl = Namespace("http://www.w3.org/2002/07/owl#")

# TEI namespace (XML only, not used as RDF vocabulary)
tei_ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
xml_ns = '{http://www.w3.org/XML/1998/namespace}'

# GRAPH
g = Graph()

g.bind("rrr", rrr)
g.bind("schema", schema)
g.bind("dcterms", dcterms)
g.bind("dc", dc)
g.bind("foaf", foaf)
g.bind("crm", crm)
g.bind("owl", owl)

# MAIN ENTITY
screenplay = URIRef(rrr + "lastrada_screenplay_seq1")

# LOAD XML
tree = ET.parse("../../tei_xslt/lastrada.xml")
root = tree.getroot()

# RESOURCE TYPE
g.add((screenplay, RDF.type, schema.CreativeWork))
g.add((screenplay, dcterms.title, Literal("La strada — Sequenza I", lang="it")))

# AUTHOR
author = root.find(".//tei:author", tei_ns)
if author is not None and author.text:
    g.add((screenplay, schema.author, Literal(author.text, lang="it")))

# EDITOR
editor = root.find(".//tei:editor", tei_ns)
if editor is not None and editor.text:
    g.add((screenplay, schema.editor, Literal(editor.text, lang="it")))

# PUBLISHER
publisher = root.find(".//tei:publisher", tei_ns)
if publisher is not None and publisher.text:
    g.add((screenplay, dcterms.publisher, Literal(publisher.text, lang="it")))

# PUBLICATION DATE
date = root.find(".//tei:date[@when]", tei_ns)
if date is not None:
    g.add((screenplay, dcterms.issued, Literal(date.get("when"), datatype=XSD.gYear)))

# LANGUAGE
lang = root.find(".//tei:language[@ident]", tei_ns)
if lang is not None:
    g.add((screenplay, dcterms.language, Literal(lang.get("ident"))))

# PERSONS (characters + actors)
for person in root.findall(".//tei:person", tei_ns):
    person_id = person.get(f"{xml_ns}id")
    if not person_id:
        continue

    character_uri = URIRef(rrr + f"character_{person_id}")
    g.add((character_uri, RDF.type, foaf.Person))
    g.add((screenplay, schema.character, character_uri))

    # Role name
    role_name = person.find(".//tei:persName[@type='role']", tei_ns)
    if role_name is not None and role_name.text:
        g.add((character_uri, schema.name, Literal(role_name.text, lang="it")))

    # Actor
    actor_name = person.find(".//tei:persName[@type='actor']", tei_ns)
    if actor_name is not None and actor_name.text:
        actor_uri = URIRef(rrr + f"actor_{person_id}")
        g.add((actor_uri, RDF.type, foaf.Person))
        g.add((actor_uri, foaf.name, Literal(actor_name.text)))
        g.add((character_uri, schema.actor, actor_uri))

        # VIAF — uniformato a owl:sameAs
        viaf_ref = actor_name.get("ref")
        if viaf_ref:
            g.add((actor_uri, owl.sameAs, URIRef(viaf_ref)))

# PLACES
for place in root.findall(".//tei:place", tei_ns):
    place_id = place.get(f"{xml_ns}id")
    if not place_id:
        continue

    place_uri = URIRef(rrr + f"place_{place_id}")
    g.add((place_uri, RDF.type, schema.Place))

    place_name = place.find(".//tei:placeName", tei_ns)
    if place_name is not None and place_name.text:
        g.add((place_uri, schema.name, Literal(place_name.text, lang="it")))

# SCENES
scene_counter = 0

for div in root.findall(".//tei:div[@type='scene']", tei_ns):
    scene_counter += 1
    scene_id = div.get(f"{xml_ns}id") or f"scene_{scene_counter}"
    scene_num = div.get("n", str(scene_counter))

    scene_uri = URIRef(rrr + f"scene_{scene_id}")
    g.add((scene_uri, RDF.type, schema.CreativeWork))
    g.add((scene_uri, schema.isPartOf, screenplay))
    g.add((scene_uri, schema.position, Literal(scene_num, datatype=XSD.integer)))

    # Scene headings
    for head in div.findall("tei:head", tei_ns):
        if head.text:
            if head.get("type") == "logline":
                g.add((scene_uri, dcterms.abstract, Literal(head.text, lang="it")))
            else:
                g.add((scene_uri, dcterms.title, Literal(head.text, lang="it")))

    # Stage directions (settings)
    for stage in div.findall("tei:stage[@type='setting']", tei_ns):
        setting_text = "".join(stage.itertext()).strip()
        if setting_text:
            g.add((scene_uri, dcterms.abstract, Literal(setting_text, lang="it")))

        where_ref = stage.get("where")
        if where_ref:
            place_ref = where_ref.replace("#", "")
            place_uri = URIRef(rrr + f"place_{place_ref}")
            g.add((scene_uri, schema.location, place_uri))

    # Paragraphs
    para_counter = 0
    for para in div.findall("tei:p", tei_ns):
        para_counter += 1
        para_text = "".join(para.itertext()).strip()
        if para_text:
            para_uri = URIRef(rrr + f"{scene_id}_para_{para_counter}")
            g.add((para_uri, RDF.type, schema.Text))
            g.add((para_uri, schema.isPartOf, scene_uri))
            g.add((para_uri, schema.text, Literal(para_text, lang="it")))
            g.add((para_uri, schema.position, Literal(para_counter, datatype=XSD.integer)))

    # Speeches
    speech_counter = 0
    for sp in div.findall("tei:sp", tei_ns):
        speech_counter += 1
        speaker_ref = sp.get("who")

        speech_uri = URIRef(rrr + f"{scene_id}_speech_{speech_counter}")
        g.add((speech_uri, RDF.type, schema.Text))
        g.add((speech_uri, schema.isPartOf, scene_uri))
        g.add((speech_uri, schema.position, Literal(speech_counter, datatype=XSD.integer)))

        if speaker_ref:
            character_id = speaker_ref.replace("#", "")
            character_uri = URIRef(rrr + f"character_{character_id}")
            g.add((speech_uri, schema.character, character_uri))

        speaker_elem = sp.find("tei:speaker", tei_ns)
        if speaker_elem is not None and speaker_elem.text:
            g.add((speech_uri, schema.name, Literal(speaker_elem.text, lang="it")))

        for p in sp.findall("tei:p", tei_ns):
            dialog_text = "".join(p.itertext()).strip()
            if dialog_text:
                g.add((speech_uri, schema.text, Literal(dialog_text, lang="it")))

        for stage in sp.findall(".//tei:stage[@type='direction']", tei_ns):
            direction_text = "".join(stage.itertext()).strip()
            if direction_text:
                g.add((speech_uri, schema.description, Literal(direction_text, lang="it")))

    # Transitions
    for stage in div.findall("tei:stage[@type='transition']", tei_ns):
        transition_text = "".join(stage.itertext()).strip()
        if transition_text:
            g.add((scene_uri, schema.description, Literal(transition_text, lang="it")))

# SERIALIZATION
g.serialize(format="turtle", destination="../../tei_xslt/lastrada_screenplay.ttl")
g.serialize(format="xml", destination="../../tei_xslt/lastrada_screenplay.rdf")

print("XML converted to RDF!")
