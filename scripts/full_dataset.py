import pandas as pd
from rdflib import Namespace, Graph, RDF, URIRef, Literal, XSD, RDFS, OWL, FOAF
import re

# NAMESPACES

rrr = Namespace("https://github.com/CineFiles25/informational-science-and-cultural-heritage/")
rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
schema = Namespace("https://schema.org/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
fiaf = Namespace("https://fiaf.github.io/film-related-materials/objects/")

# GRAPH SETUP

g = Graph()

ns_dict = {
    "rrr": rrr,   
    "rdf": rdf_ns,
    "rdfs": rdfs,
    "owl": owl,
    "schema": schema,
    "dc": dc,
    "dcterms": dcterms,
    "crm": crm,
    "foaf": foaf,
    "fiaf": fiaf
}

for prefix, ns in ns_dict.items():
    g.bind(prefix, ns)

# ENTITIES

# People, Places and Organizations
renzo_renzi = URIRef(rrr + "renzo_renzi")
aldo_ferrari = URIRef(rrr + "aldo_ferrari")
cineteca_di_bologna = URIRef(rrr + "cineteca_di_bologna")
bologna = URIRef(rrr + "bologna")

# Items 
library = URIRef(rrr + "renzi_library")
documentary = URIRef(rrr + "quando_il_po_e_dolce")
set_photo = URIRef(rrr + "ferrari_set_photo")

# AUTHORITY 

g.add((renzo_renzi, OWL.sameAs, URIRef("http://viaf.org/viaf/40486517")))
g.add((cineteca_di_bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/124960346")))
g.add((bologna, OWL.sameAs, URIRef("http://viaf.org/viaf/257723025")))

# CSV → RDF TRANSFORMATION

# Library 

renzi_library = pd.read_csv("../csv/renzi_library.csv", keep_default_na=False, encoding="utf-8")
    
for idx, row in renzi_library.iterrows():
    g.add((library, RDF.type, URIRef(schema + "Library")))
    g.add((library, RDFS.subClassOf, URIRef(schema + "CivicStructure")))
    g.add((library, OWL.sameAs, URIRef("https://isni.org/isni/0000000459141457")))
    g.add((library, dc.identifier, Literal(row["Id ISIL"])))
    g.add((library, schema.name, Literal(row["Name"])))
    g.add((library, schema.alternateName, Literal(row["Alt Title"])))
    g.add((library, schema.additionalType, Literal(row["Original Function"])))
    g.add((library, crm.P52_has_current_owner, Literal(row["Owner"])))
    g.add((library, schema.date, Literal(row["Completion Of Work"], datatype=XSD.gYear)))
    g.add((library, schema.foundingDate, Literal(row["Library Foundation"], datatype=XSD.gYear)))
    g.add((library, schema.address, Literal(row["Address"])))
    g.add((library, schema.addressLocality, Literal(row["City"])))
    g.add((library, schema.addressCountry, Literal(row["Country"])))
    g.add((library, schema.geo, Literal(row["Coordinates"])))
    g.add((library, schema.url, Literal(row["Website"], datatype=XSD.anyURI)))
    g.add((library, schema.additionalType, Literal(row["Structure Type"])))
    g.add((library, schema.floorSize, Literal(row["Area"], datatype=XSD.float)))
    g.add((library, schema.seatingCapacity, Literal(row["Seats"], datatype=XSD.integer)))
    g.add((library, dc.description, Literal(row["Audio System"])))
    g.add((library, dc.description, Literal(row["Video System"])))
    g.add((renzo_renzi, schema.honorificPrefix, library))

# Documentary 

quando_il_po_è_dolce = pd.read_csv("../csv/po_documentary.csv", keep_default_na=False, encoding="utf-8")

for idx, row in quando_il_po_è_dolce.iterrows():
    g.add((documentary, RDF.type, URIRef(schema + "Movie")))
    g.add((documentary, RDFS.subClassOf, URIRef(schema + "CreativeWork")))
    g.add((documentary, dc.title, Literal(row["Title"])))
    g.add((documentary, schema.alternateName, Literal(row["Alt Title"])))
    g.add((documentary, schema.director, renzo_renzi))
    g.add((documentary, schema.author, renzo_renzi))
    g.add((documentary, schema.edition, Literal(row["Edition"])))
    g.add((documentary, schema.genre, Literal(row["Type"])))
    g.add((documentary, schema.countryOfOrigin, Literal(row["Country"])))    
    g.add((documentary, schema.productionCompany, Literal(row["Production Company"])))    
    g.add((documentary, schema.datePublished, Literal(row["Year"], datatype=XSD.gYear)))
    g.add((documentary, schema.duration, Literal(row["Running Time"])))
    g.add((documentary, schema.color, Literal(row["Color"])))
    g.add((documentary, schema.encodingFormat, Literal(row["Film Type"])))
    g.add((documentary, schema.frameRate, Literal(row["Frame Rate"])))
    g.add((documentary, schema.contentSize, Literal(row["Film Length"])))    
    g.add((documentary, schema.sound, Literal(row["Sound"])))
    g.add((documentary, schema.inLanguage, Literal(row["Language"])))
    g.add((documentary, schema.about, Literal(row["Subject"])))
    g.add((documentary, schema.spatialCoverage, Literal(row["Filming Location"])))
    g.add((documentary, schema.musicBy, Literal(row["Music Composer"])))
    g.add((documentary, schema.contentRating, Literal(row["Certificate"])))
    
# Set Photo by Aldo Ferrari

ferrari_set_photo = pd.read_csv("../csv/ferrari_set_photo.csv", keep_default_na=False, encoding="utf-8")

for idx, row in ferrari_set_photo.iterrows():
    g.add((set_photo, RDF.type, URIRef(schema + "Photograph")))
    g.add((set_photo, RDFS.subClassOf, URIRef(schema + "CreativeWork")))
    g.add((set_photo, dc.title, Literal(row["Title"])))
    g.add((set_photo, dc.creator, aldo_ferrari))    
    g.add((set_photo, schema.dateCreated, Literal(row["Date Taken"], datatype=XSD.gYear)))
    g.add((set_photo, schema.about, renzo_renzi))    
    g.add((set_photo, schema.locationCreated, Literal(row["Location"])))
    g.add((set_photo, schema.owner, cineteca_di_bologna))
    g.add((set_photo, dcterms.isPartOf, Literal(row["Collection"])))    
    g.add((set_photo, schema.url, Literal(row["Url"], datatype=XSD.anyURI)))
    g.add((set_photo, schema.material, Literal(row["Form"])))
    g.add((set_photo, schema.artform, Literal(row["Technique"]))) 
    g.add((set_photo, schema.width, Literal(row["Dimensions"], datatype=XSD.integer)))
    g.add((set_photo, schema.contentSize, Literal(row["File Size"])))
    g.add((set_photo, schema.fileFormat, Literal(row["Format"])))
    g.add((set_photo, schema.license, Literal(row["Type Of License"])))

# SERIALIZATION 

if __name__ == "__main__":
    g.serialize(format="turtle", destination="../ttl/full_dataset.ttl")
    print("All CSV files converted to RDF Turtle format!")
