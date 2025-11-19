<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <!-- ROOT TEMPLATE -->
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
          .logline {
            font-style: italic;
            color: #555;
            margin-top: 0.25rem;
            margin-bottom: 0.75rem;
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
          .pb {
            font-size: 0.8rem;
            color: #888;
            float: right;
            margin-left: 0.5rem;
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

  <!-- BODY -->
  <xsl:template match="tei:body">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- SCENES -->
  <xsl:template match="tei:div[@type='scene']">
    <section class="scene">
      <xsl:apply-templates/>
    </section>
  </xsl:template>

  <!-- HEADINGS -->
  <!-- Logline -->
  <xsl:template match="tei:head[@type='logline']">
    <p class="logline">
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!-- Other heads -->
  <xsl:template match="tei:head[not(@type='logline')]">
    <h2><xsl:apply-templates/></h2>
  </xsl:template>

  <!-- STAGE DIRECTIONS -->
  <xsl:template match="tei:stage">
    <p class="stage">
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!-- PAGE BREAKS -->
  <xsl:template match="tei:pb">
    <span class="pb">
      <xsl:text>p. </xsl:text>
      <xsl:value-of select="@n"/>
    </span>
  </xsl:template>

  <!-- SPEECHES -->
  <xsl:template match="tei:sp">
    <div class="speech">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <!-- First paragraph inside a speech: print the speaker name -->
  <xsl:template match="tei:sp/tei:p[1]">
    <p>
      <span class="speaker">
        <xsl:value-of select="normalize-space(../tei:speaker)"/>
      </span>
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!-- Following paragraphs inside the same speech -->
  <xsl:template match="tei:sp/tei:p[position() &gt; 1]">
    <p>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!-- Do not print tei:speaker separately -->
  <xsl:template match="tei:speaker"/>

  <!-- Normal paragraphs (outside speeches) -->
  <xsl:template match="tei:p[not(parent::tei:sp)]">
    <p><xsl:apply-templates/></p>
  </xsl:template>

  <!-- Plain text -->
  <xsl:template match="text()">
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>
