import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD
from rdflib.namespace import FOAF, DCTERMS

rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
tei = Namespace("http://www.tei-c.org/ns/1.0/")
schema = Namespace("https://schema.org/")

g = Graph()

ns_dict = {
    "rrr": rrr,
    "tei": tei,
    "schema": schema,
    "dcterms": DCTERMS,
    "foaf": FOAF,
    "rdf": RDF,
    "rdfs": RDFS
}

def graph_bindings():
    for prefix, ns in ns_dict.items():
        g.bind(prefix, ns)
    return g

g = graph_bindings()

# TEI namespace for XML queries
tei_ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Parse XML file
tree = ET.parse("../../tei_xslt/lastrada.xml")
root = tree.getroot()

screenplay = URIRef(rrr + "lastrada_screenplay_seq1")

# Screenplay metadata
g.add((screenplay, RDF.type, schema.CreativeWork))
g.add((screenplay, RDF.type, tei.TEI))
g.add((screenplay, DCTERMS.title, Literal("La strada — Sequenza I", lang="it")))

# Author
author = root.find(".//tei:author", tei_ns)
if author is not None and author.text:
    g.add((screenplay, schema.author, Literal(author.text)))

# Editor
editor = root.find(".//tei:editor", tei_ns)
if editor is not None and editor.text:
    g.add((screenplay, schema.editor, Literal(editor.text)))

# Publisher
publisher = root.find(".//tei:publisher", tei_ns)
if publisher is not None and publisher.text:
    g.add((screenplay, schema.publisher, Literal(publisher.text)))

# Publication date
date = root.find(".//tei:date[@when]", tei_ns)
if date is not None:
    g.add((screenplay, schema.datePublished, Literal(date.get('when'), datatype=XSD.gYear)))

# Language
lang = root.find(".//tei:language[@ident]", tei_ns)
if lang is not None:
    g.add((screenplay, schema.inLanguage, Literal(lang.get('ident'))))

for person in root.findall(".//tei:person", tei_ns):
    person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
    if not person_id:
        continue
    
    character_uri = URIRef(rrr[f"character_{person_id}"])
    g.add((character_uri, RDF.type, FOAF.Person))
    g.add((character_uri, RDF.type, schema.Person))
    g.add((screenplay, schema.character, character_uri))
    
    # Role name
    role_name = person.find(".//tei:persName[@type='role']", tei_ns)
    if role_name is not None and role_name.text:
        g.add((character_uri, FOAF.name, Literal(role_name.text, lang="it")))
        g.add((character_uri, schema.name, Literal(role_name.text, lang="it")))
    
    # Actor name
    actor_name = person.find(".//tei:persName[@type='actor']", tei_ns)
    if actor_name is not None and actor_name.text:
        actor_uri = URIRef(rrr[f"actor_{person_id}"])
        g.add((actor_uri, RDF.type, FOAF.Person))
        g.add((actor_uri, FOAF.name, Literal(actor_name.text)))
        g.add((character_uri, schema.actor, actor_uri))
        
        # VIAF reference
        viaf_ref = actor_name.get('ref')
        if viaf_ref:
            g.add((actor_uri, RDFS.seeAlso, URIRef(viaf_ref)))

for place in root.findall(".//tei:place", tei_ns):
    place_id = place.get('{http://www.w3.org/XML/1998/namespace}id')
    if not place_id:
        continue
    
    place_uri = URIRef(rrr[f"place_{place_id}"])
    g.add((place_uri, RDF.type, schema.Place))
    
    place_name = place.find(".//tei:placeName", tei_ns)
    if place_name is not None and place_name.text:
        g.add((place_uri, schema.name, Literal(place_name.text, lang="it")))

scene_counter = 0
for div in root.findall(".//tei:div[@type='scene']", tei_ns):
    scene_counter += 1
    scene_id = div.get('{http://www.w3.org/XML/1998/namespace}id') or f"scene_{scene_counter}"
    scene_num = div.get('n', str(scene_counter))
    
    scene_uri = URIRef(rrr[f"scene_{scene_id}"])
    g.add((scene_uri, RDF.type, rrr.Scene))
    g.add((scene_uri, schema.partOf, screenplay))
    g.add((scene_uri, schema.position, Literal(int(scene_num), datatype=XSD.integer)))
    
    # Scene headings
    for head in div.findall("tei:head", tei_ns):
        if head.text:
            if head.get('type') == 'logline':
                g.add((scene_uri, rrr.logline, Literal(head.text, lang="it")))
            else:
                g.add((scene_uri, DCTERMS.title, Literal(head.text, lang="it")))
    
    # Stage directions (settings)
    for stage in div.findall("tei:stage[@type='setting']", tei_ns):
        setting_text = ''.join(stage.itertext()).strip()
        if setting_text:
            g.add((scene_uri, rrr.setting, Literal(setting_text, lang="it")))
        
        where_ref = stage.get('where')
        if where_ref:
            place_ref = where_ref.replace('#', '')
            place_uri = URIRef(rrr[f"place_{place_ref}"])
            g.add((scene_uri, schema.location, place_uri))
    
    # Narrative paragraphs
    para_counter = 0
    for para in div.findall("tei:p", tei_ns):
        para_counter += 1
        para_text = ''.join(para.itertext()).strip()
        if para_text:
            para_uri = URIRef(rrr[f"{scene_id}_para_{para_counter}"])
            g.add((para_uri, RDF.type, rrr.Narrative))
            g.add((para_uri, schema.partOf, scene_uri))
            g.add((para_uri, schema.text, Literal(para_text, lang="it")))
            g.add((para_uri, schema.position, Literal(para_counter, datatype=XSD.integer)))
    
    # Speech/Dialog
    speech_counter = 0
    for sp in div.findall("tei:sp", tei_ns):
        speech_counter += 1
        speaker_ref = sp.get('who')
        
        speech_uri = URIRef(rrr[f"{scene_id}_speech_{speech_counter}"])
        g.add((speech_uri, RDF.type, rrr.Dialog))
        g.add((speech_uri, schema.partOf, scene_uri))
        g.add((speech_uri, schema.position, Literal(speech_counter, datatype=XSD.integer)))
        
        if speaker_ref:
            character_id = speaker_ref.replace('#', '')
            character_uri = URIRef(rrr[f"character_{character_id}"])
            g.add((speech_uri, schema.character, character_uri))
        
        speaker_elem = sp.find("tei:speaker", tei_ns)
        if speaker_elem is not None and speaker_elem.text:
            g.add((speech_uri, rrr.speakerLabel, Literal(speaker_elem.text, lang="it")))
        
        for p in sp.findall("tei:p", tei_ns):
            dialog_text = ''.join(p.itertext()).strip()
            if dialog_text:
                g.add((speech_uri, schema.text, Literal(dialog_text, lang="it")))
        
        for stage in sp.findall(".//tei:stage[@type='direction']", tei_ns):
            direction_text = ''.join(stage.itertext()).strip()
            if direction_text:
                g.add((speech_uri, rrr.stageDirection, Literal(direction_text, lang="it")))
    
    # Transitions
    for stage in div.findall("tei:stage[@type='transition']", tei_ns):
        transition_text = ''.join(stage.itertext()).strip()
        if transition_text:
            g.add((scene_uri, rrr.transition, Literal(transition_text, lang="it")))

print(f"Total triples created: {len(g)}")

# Serialize to Turtle
g.serialize(destination="tei_xslt/lastrada_screenplay.ttl", format='turtle')
print("Turtle file saved to tei_xslt/lastrada_screenplay.ttl")

# Serialize to RDF/XML
g.serialize(destination="tei_xslt/lastrada_screenplay.rdf", format='xml')
print("RDF/XML file saved to tei_xslt/lastrada_screenplay.rdf")

print("XML successfully converted to RDF!")
