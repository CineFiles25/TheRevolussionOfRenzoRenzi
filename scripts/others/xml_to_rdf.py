from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import xml.etree.ElementTree as ET

def xml_to_rdf(xml_file, output_file):
    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Create RDF graph
    g = Graph()
    
    # Define namespaces
    rrr = Namespace("https://github.com/CineFiles25/TheRevolussionOfRenzoRenzi/")
    tei = Namespace("http://www.tei-c.org/ns/1.0/")
    g.bind("rrr", rrr)
    g.bind("tei", tei)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    
    print(f"Root element: {root.tag}")
    print(f"Number of children: {len(root)}")
    
    # Helper function to remove namespace from tag
    def clean_tag(tag):
        """Remove namespace URI from tag, keep only local name"""
        if '}' in tag:
            return tag.split('}')[1]
        return tag
    
    # Recursive function to process all elements
    def process_element(element, parent_subject=None, idx=0):
        """Recursively process XML elements"""
        # Create a subject URI
        tag_name = clean_tag(element.tag)
        subject = URIRef(rrr[f"{tag_name}_{idx}"])
        
        # Add type
        g.add((subject, RDF.type, tei[tag_name]))
        
        # Link to parent if exists
        if parent_subject:
            g.add((subject, rrr["hasParent"], parent_subject))
        
        # Add attributes as properties
        for attr, value in element.attrib.items():
            attr_name = clean_tag(attr)
            g.add((subject, rrr[attr_name], Literal(value)))
        
        # Add text content if exists
        if element.text and element.text.strip():
            g.add((subject, rrr["textContent"], Literal(element.text.strip())))
        
        # Process child elements recursively
        for child_idx, child in enumerate(element):
            process_element(child, subject, f"{idx}_{child_idx}")
            
            # Add tail text (text after closing tag)
            if child.tail and child.tail.strip():
                g.add((subject, rrr["tailText"], Literal(child.tail.strip())))
        
        return subject
    
    # Start processing from root
    process_element(root, None, 0)
    
    # Print statistics
    print(f"Total triples created: {len(g)}")
    
    # Serialize to RDF file
    g.serialize(destination=output_file, format='turtle')
    print(f"RDF file saved to {output_file}!")

if __name__ == "__main__":
    xml_file = "lastrada.xml"
    output_file = "lastrada.ttl"
    
    xml_to_rdf(xml_file, output_file)