<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html lang="it">
      <head>
        <meta charset="UTF-8"/>
        <title>
          <xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
        </title>
        <style>
          body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            max-width: 800px;
            margin: 2rem auto;
            line-height: 1.5;
          }
          h1, h2, h3 {
            font-weight: 600;
          }
          .scene {
            margin: 1.5rem 0;
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 8px;
          }
          .scene > h2 {
            margin-top: 0;
          }
          .stage {
            font-style: italic;
            color: #555;
          }
          .speech {
            margin: 0.4rem 0;
          }
          .speaker {
            font-weight: 600;
            text-transform: uppercase;
            margin-right: 0.4rem;
          }
        </style>
      </head>
      <body>
        <h1>
          <xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
        </h1>

        <p>
          <strong>Source:</strong>
          <xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:sourceDesc//tei:title"/>
          (<xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:sourceDesc//tei:date"/>)
        </p>

        <xsl:apply-templates select="//tei:text/tei:body"/>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="tei:body">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="tei:div[@type='scene']">
    <section class="scene">
      <xsl:if test="tei:head">
        <h2><xsl:value-of select="tei:head"/></h2>
      </xsl:if>
      <xsl:apply-templates/>
    </section>
  </xsl:template>

  <xsl:template match="tei:head[not(parent::tei:div[@type='scene'])]">
    <h2><xsl:apply-templates/></h2>
  </xsl:template>

  <xsl:template match="tei:stage">
    <p class="stage">
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="tei:sp">
    <p class="speech">
      <span class="speaker">
        <xsl:value-of select="normalize-space(tei:speaker)"/>
      </span>
      <xsl:text> </xsl:text>
      <xsl:apply-templates select="tei:p"/>
    </p>
  </xsl:template>

  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>

  <xsl:template match="text()">
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>