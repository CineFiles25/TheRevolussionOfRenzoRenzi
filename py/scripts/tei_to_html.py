from lxml import etree

XML_FILE = "lastrada.xml"
XSL_FILE = "tei2html_lastrada.xsl"
OUT_FILE = "lastrada.html"

def main():
    xml = etree.parse(XML_FILE)
    xsl = etree.parse(XSL_FILE)
    transform = etree.XSLT(xsl)

    result = transform(xml)

    with open(OUT_FILE, "wb") as f:
        f.write(etree.tostring(result, encoding="utf-8", pretty_print=True))

    print(f"HTML written to {OUT_FILE}")

if __name__ == "__main__":
    main()
