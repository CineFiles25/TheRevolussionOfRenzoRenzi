<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <!-- ROOT TEMPLATE -->
  <xsl:template match="/">
    <xsl:text disable-output-escaping="yes">&lt;!DOCTYPE html&gt;</xsl:text>
    <html lang="it">
      <head>
        <meta charset="UTF-8"/>
        <title>
          <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
        </title>
        <style>
          body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            margin: 0;
            padding: 1.5rem;
            background-color: #f7f7f7;
            line-height: 1.5;
          }
          main {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-radius: 8px;
          }
          header.page-header {
            margin-bottom: 1.5rem;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 1rem;
          }
          header.page-header h1 {
            font-size: 1.8rem;
            margin: 0 0 0.25rem 0;
          }
          header.page-header p.source {
            margin: 0;
            font-size: 0.9rem;
            color: #666;
          }
          section.meta {
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
          }
          section.meta h2 {
            font-size: 1.1rem;
            margin-top: 0;
          }
          section.meta h3 {
            font-size: 1rem;
            margin-bottom: 0.25rem;
          }
          section.meta ul {
            margin: 0 0 0.75rem 1.25rem;
            padding: 0;
          }
          section.meta li {
            margin-bottom: 0.15rem;
          }
          .scene {
            margin: 1.5rem 0;
          }
          .scene h2 {
            font-size: 1.2rem;
            margin-bottom: 0.25rem;
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
          .stage-setting strong,
          .stage-direction strong,
          .stage-transition strong {
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.08em;
            margin-right: 0.25rem;
          }
          .stage-transition {
            text-transform: uppercase;
            letter-spacing: 0.08em;
          }
          .speech {
            margin: 0.25rem 0;
          }
          .speaker {
            font-weight: bold;
            text-transform: uppercase;
          }
          .pb {
            margin: 1rem 0;
            text-align: center;
            font-size: 0.8rem;
            color: #999;
          }
        </style>
      </head>
      <body>
        <main>
          <header class="page-header">
            <h1>
              <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
            </h1>
            <p class="source">
              <xsl:text>Source: </xsl:text>
              <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc//tei:title"/>
              <xsl:text> (</xsl:text>
              <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc//tei:date"/>
              <xsl:text>)</xsl:text>
            </p>
          </header>

          <!-- Participants (cast & places) -->
          <xsl:apply-templates select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc"/>

          <!-- Main text -->
          <xsl:apply-templates select="/tei:TEI/tei:text"/>
        </main>
      </body>
    </html>
  </xsl:template>

  <!-- PARTICIPANTS -->

  <xsl:template match="tei:particDesc">
    <section class="meta">
      <h2>Personaggi e luoghi</h2>
      <xsl:apply-templates select="tei:listPerson"/>
      <xsl:apply-templates select="tei:listPlace"/>
    </section>
  </xsl:template>

  <xsl:template match="tei:listPerson">
    <h3>Personaggi</h3>
    <ul>
      <xsl:for-each select="tei:person">
        <li>
          <xsl:choose>
            <xsl:when test="tei:persName[@type='role']">
              <xsl:value-of select="tei:persName[@type='role'][1]"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="tei:persName[1]"/>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:if test="tei:persName[@type='actor']">
            <xsl:text> — </xsl:text>
            <xsl:value-of select="tei:persName[@type='actor'][1]"/>
          </xsl:if>
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template match="tei:listPlace">
    <h3>Luoghi</h3>
    <ul>
      <xsl:for-each select="tei:place">
        <li>
          <xsl:value-of select="tei:placeName"/>
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <!-- TEXT BODY -->

  <xsl:template match="tei:text">
    <xsl:apply-templates select="tei:body"/>
  </xsl:template>

  <xsl:template match="tei:body">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Scenes -->
  <xsl:template match="tei:div[@type='scene']">
    <section class="scene">
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </section>
  </xsl:template>

  <!-- Scene headings -->
  <xsl:template match="tei:div[@type='scene']/tei:head[@type='logline']">
    <p class="logline">
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="tei:div[@type='scene']/tei:head[not(@type='logline')]">
    <h2>
      <xsl:apply-templates/>
    </h2>
  </xsl:template>

  <!-- Stage directions -->
  <xsl:template match="tei:stage[@type='setting']">
    <p class="stage stage-setting">
      <strong>[Ambientazione]</strong>
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="tei:stage[@type='direction']">
    <p class="stage stage-direction">
      <strong>[Indicazione]</strong>
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="tei:stage[@type='transition']">
    <p class="stage stage-transition">
      <strong>[Transizione]</strong>
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!-- Stage directions inside speeches -->
  <xsl:template match="tei:sp/tei:stage">
    <p class="stage">
      <em>
        <xsl:apply-templates/>
      </em>
    </p>
  </xsl:template>

  <!-- Speeches -->
  <xsl:template match="tei:sp">
    <div class="speech">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <!-- First paragraph in a speech: prints speaker name -->
  <xsl:template match="tei:sp/tei:p[1]">
    <p>
      <span class="speaker">
        <xsl:value-of select="normalize-space(../tei:speaker)"/>
      </span>
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!-- Do not print speaker separately -->
  <xsl:template match="tei:speaker"/>

  <!-- Page breaks -->
  <xsl:template match="tei:pb">
    <div class="pb">
      <xsl:text>[p. </xsl:text>
      <xsl:value-of select="@n"/>
      <xsl:text>]</xsl:text>
    </div>
  </xsl:template>

  <!-- Normal paragraphs (outside speeches) -->
  <xsl:template match="tei:p[not(parent::tei:sp)]">
    <p>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!-- Plain text -->
  <xsl:template match="text()">
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>
