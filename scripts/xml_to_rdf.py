from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

import xml.etree.ElementTree as ET

def xml_to_rdf(xml_file, output_file):
    """
    Convert lastrada.xml to RDF format
    """
    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Create RDF graph
    g = Graph()
    
    # Define namespaces
    rrr = Namespace("http://example.org/lastrada/")
    g.bind("rrr", rrr)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    
    # Process XML elements
    for idx, element in enumerate(root):
        # Create a subject URI for each element
        subject = URIRef(rrr[f"item_{idx}"])
        
        # Add type
        g.add((subject, RDF.type, rrr[element.tag]))
        
        # Add attributes as properties
        for attr, value in element.attrib.items():
            g.add((subject, rrr[attr], Literal(value)))
        
        # Add text content if exists
        if element.text and element.text.strip():
            g.add((subject, rrr["value"], Literal(element.text.strip())))
        
        # Process child elements
        for child in element:
            if child.text and child.text.strip():
                g.add((subject, rrr[child.tag], Literal(child.text.strip())))
            
            # Add child attributes
            for attr, value in child.attrib.items():
                g.add((subject, rrr[f"{child.tag}_{attr}"], Literal(value)))
    
    # Serialize to RDF file
    g.serialize(destination=output_file, format='turtle')
    print("RDF file saved to TTL!")

if __name__ == "__main__":
    xml_file = "../../xml/lastrada.xml"
    output_file = "../../ttl/lastrada.ttl"
    xml_to_rdf(xml_file, output_file)