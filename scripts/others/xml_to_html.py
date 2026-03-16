from lxml import etree
from pathlib import Path

XML_FILE = Path("lastrada.xml")
XSL_FILE = Path("tei2html_lastrada.xsl")
OUT_FILE = Path("lastrada.html")

def main():

    if not XML_FILE.exists():
        raise FileNotFoundError(f"XML file not found: {XML_FILE}")

    if not XSL_FILE.exists():
        raise FileNotFoundError(f"XSL file not found: {XSL_FILE}")

    xml = etree.parse(str(XML_FILE))
    xsl = etree.parse(str(XSL_FILE))
    transform = etree.XSLT(xsl)

    result = transform(xml)

    OUT_FILE.write_bytes(
        etree.tostring(result, encoding="utf-8", pretty_print=True)
    )

    print(f"HTML successfully written to {OUT_FILE}")

if __name__ == "__main__":
    main()
