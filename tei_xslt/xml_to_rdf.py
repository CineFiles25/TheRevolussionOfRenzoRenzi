import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, FOAF

def lastrada_xml_to_rdf(xml_file, output_file):
    """
    Convert La Strada TEI XML screenplay to RDF format
    """
    
    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Create RDF graph
    g = Graph()
    
    # Define namespaces
    rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
    tei = Namespace("http://www.tei-c.org/ns/1.0/")
    schema = Namespace("https://schema.org/")
    
    # Bind namespaces
    g.bind("rrr", rrr)
    g.bind("tei", tei)
    g.bind("schema", schema)
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    
    # TEI namespace for XPath queries
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    # ========================================================================
    # MAIN WORK - The Screenplay
    # ========================================================================
    screenplay = URIRef(rrr["lastrada_screenplay_seq1"])
    g.add((screenplay, RDF.type, schema.CreativeWork))
    g.add((screenplay, RDF.type, tei.TEI))
    g.add((screenplay, DCTERMS.title, Literal("La strada — Sequenza I", lang="it")))
    
    # Extract author
    author_elem = root.find(".//tei:author", ns)
    if author_elem is not None and author_elem.text:
        g.add((screenplay, schema.author, Literal(author_elem.text)))
    
    # Extract editor
    editor_elem = root.find(".//tei:editor", ns)
    if editor_elem is not None and editor_elem.text:
        g.add((screenplay, schema.editor, Literal(editor_elem.text)))
    
    # Extract publisher
    publisher_elem = root.find(".//tei:publisher", ns)
    if publisher_elem is not None and publisher_elem.text:
        g.add((screenplay, schema.publisher, Literal(publisher_elem.text)))
    
    # Extract publication date
    date_elem = root.find(".//tei:date[@when]", ns)
    if date_elem is not None:
        g.add((screenplay, schema.datePublished, Literal(date_elem.get('when'), datatype=XSD.gYear)))
    
    # Extract language
    lang_elem = root.find(".//tei:language[@ident]", ns)
    if lang_elem is not None:
        g.add((screenplay, schema.inLanguage, Literal(lang_elem.get('ident'))))
    
    # ========================================================================
    # CHARACTERS (PERSONS)
    # ========================================================================
    for person in root.findall(".//tei:person", ns):
        person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
        if not person_id:
            continue
            
        character_uri = URIRef(rrr[f"character_{person_id}"])
        g.add((character_uri, RDF.type, FOAF.Person))
        g.add((character_uri, RDF.type, schema.Person))
        g.add((screenplay, schema.character, character_uri))
        
        # Character name
        role_name = person.find(".//tei:persName[@type='role']", ns)
        if role_name is not None and role_name.text:
            g.add((character_uri, FOAF.name, Literal(role_name.text, lang="it")))
            g.add((character_uri, schema.name, Literal(role_name.text, lang="it")))
        
        # Actor name and VIAF link
        actor_name = person.find(".//tei:persName[@type='actor']", ns)
        if actor_name is not None:
            if actor_name.text:
                actor_uri = URIRef(rrr[f"actor_{person_id}"])
                g.add((actor_uri, RDF.type, FOAF.Person))
                g.add((actor_uri, FOAF.name, Literal(actor_name.text)))
                g.add((character_uri, schema.actor, actor_uri))
                
                # VIAF authority link
                viaf_ref = actor_name.get('ref')
                if viaf_ref:
                    g.add((actor_uri, RDFS.seeAlso, URIRef(viaf_ref)))
    
    # ========================================================================
    # PLACES
    # ========================================================================
    for place in root.findall(".//tei:place", ns):
        place_id = place.get('{http://www.w3.org/XML/1998/namespace}id')
        if not place_id:
            continue
            
        place_uri = URIRef(rrr[f"place_{place_id}"])
        g.add((place_uri, RDF.type, schema.Place))
        
        place_name = place.find(".//tei:placeName", ns)
        if place_name is not None and place_name.text:
            g.add((place_uri, schema.name, Literal(place_name.text, lang="it")))
    
    # ========================================================================
    # SCENES
    # ========================================================================
    scene_counter = 0
    for div in root.findall(".//tei:div[@type='scene']", ns):
        scene_counter += 1
        scene_id = div.get('{http://www.w3.org/XML/1998/namespace}id') or f"scene_{scene_counter}"
        scene_num = div.get('n', str(scene_counter))
        
        scene_uri = URIRef(rrr[f"scene_{scene_id}"])
        g.add((scene_uri, RDF.type, rrr.Scene))
        g.add((scene_uri, schema.partOf, screenplay))
        g.add((scene_uri, schema.position, Literal(int(scene_num), datatype=XSD.integer)))
        
        # Scene heading
        for head in div.findall("tei:head", ns):
            if head.text:
                if head.get('type') == 'logline':
                    g.add((scene_uri, rrr.logline, Literal(head.text, lang="it")))
                else:
                    g.add((scene_uri, DCTERMS.title, Literal(head.text, lang="it")))
        
        # Stage directions (setting)
        for stage in div.findall("tei:stage[@type='setting']", ns):
            setting_text = ''.join(stage.itertext()).strip()
            if setting_text:
                g.add((scene_uri, rrr.setting, Literal(setting_text, lang="it")))
            
            # Link to places
            where_ref = stage.get('where')
            if where_ref:
                place_ref = where_ref.replace('#', '')
                place_uri = URIRef(rrr[f"place_{place_ref}"])
                g.add((scene_uri, schema.location, place_uri))
        
        # Narrative paragraphs
        para_counter = 0
        for para in div.findall("tei:p", ns):
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
        for sp in div.findall("tei:sp", ns):
            speech_counter += 1
            speaker_ref = sp.get('who')
            
            speech_uri = URIRef(rrr[f"{scene_id}_speech_{speech_counter}"])
            g.add((speech_uri, RDF.type, rrr.Dialog))
            g.add((speech_uri, schema.partOf, scene_uri))
            g.add((speech_uri, schema.position, Literal(speech_counter, datatype=XSD.integer)))
            
            # Link speaker
            if speaker_ref:
                character_id = speaker_ref.replace('#', '')
                character_uri = URIRef(rrr[f"character_{character_id}"])
                g.add((speech_uri, schema.character, character_uri))
            
            # Speaker label
            speaker_elem = sp.find("tei:speaker", ns)
            if speaker_elem is not None and speaker_elem.text:
                g.add((speech_uri, rrr.speakerLabel, Literal(speaker_elem.text, lang="it")))
            
            # Dialog text
            for p in sp.findall("tei:p", ns):
                dialog_text = ''.join(p.itertext()).strip()
                if dialog_text:
                    g.add((speech_uri, schema.text, Literal(dialog_text, lang="it")))
            
            # Stage directions within speech
            for stage in sp.findall(".//tei:stage[@type='direction']", ns):
                direction_text = ''.join(stage.itertext()).strip()
                if direction_text:
                    g.add((speech_uri, rrr.stageDirection, Literal(direction_text, lang="it")))
        
        # Transitions
        for stage in div.findall("tei:stage[@type='transition']", ns):
            transition_text = ''.join(stage.itertext()).strip()
            if transition_text:
                g.add((scene_uri, rrr.transition, Literal(transition_text, lang="it")))
    
    # ========================================================================
    # SERIALIZE
    # ========================================================================
    print(f"Total triples created: {len(g)}")
    g.serialize(destination=output_file, format='turtle')
    print(f"RDF file saved to {output_file}!")

if __name__ == "__main__":
    xml_file = "lastrada.xml"
    output_file = "lastrada.ttl"
    
    lastrada_xml_to_rdf(xml_file, output_file)