# Kontrak format laporan Pekan 6

Reference: C:/Users/lenovo/Documents/Laporan Praktikum PBO Pekan 5.docx.
Reference Word render: reference.pdf and reference/page-1.png through page-10.png.
10 rendered pages; 4 sections. Source remains read-only. Package SHA inventory is
recorded by the builder in package_inventory.json before authoring.

Page size 12240 × 15840 twips (Letter); left margin 2268 (4 cm), top/right/bottom
1701 (3 cm); header/footer distance 720 twips. All four section geometries preserved.
Cover has no page number. Front matter first footer i and default footer ii are
literal source text. Body starts 1 with PAGE field in upper right. Bibliography
footer is literal iii. Preserve these sections, headers, footers and page furniture.

Typography: direct Times New Roman, cover 14pt bold centered, body 12pt justified,
1.5 line spacing (360 auto), first-line indent 720 twips. Chapter headings 12pt bold,
centered on two paragraphs BAB n then title. Subheadings 12pt bold justified. TOC
12pt bold with original right tab and dot leader. Code 10pt Consolas, dark shading,
light text as original NormalWeb paragraphs. Clone these original patterns.

Slots, word/document.xml body child indices in reference:
- 0..19: cover; preserve all incl. drawing/logo. Only paragraph 1 changes 5 to 6.
- 20: DAFTAR ISI heading. 21..36: clone TOC entries for actual sections/page values.
- 42..45: kata pengantar and three paragraphs. Preserve wording except scope may
  explicitly describe Abstraction, without inventing events or research.
- 52: original front-matter section break, preserve.
- 53..66: chapter/subhead/body/list patterns for new introduction.
- 68,69,70,71,88: chapter, subhead, code, narrative patterns for discussion.
- 124..172: same patterns reused for tasks T1..T4 and real existing execution evidence.
- 181..186: conclusion, repository link, body section boundary.
- 187..189: bibliography pattern and original final section.

Allowed content expansion: clone chapter/subheading/narrative/code styles and new
tables for required T3/T4 comparisons; source has no table precedent. New tables use
the same Times New Roman 12pt with plain borders, natural row heights. New UML image
is clearly technical content; use a centered inline image. Original logo and all
original images, relationships, styles, numbering, theme, headers/footers, customXml,
footnotes/endnotes remain unchanged. Add image relationship and content type only
as needed. Cover logo drawing XML is preserved byte-for-byte at subtree level.

TOC is static, as in the reference; page values will be recomputed from Word's
actual pagination and inserted using original tab/leader pattern. New paragraphs
have keep-with-next on headings to prevent isolated headings. Chapter page breaks
are explicit rather than copied stretches of empty paragraphs.

Fidelity gates: unchanged reference SHA; unchanged package parts except document,
settings (updateFields if needed), relationships and media additions; 4 original
sections and identical page geometry; preserve cover and logo; inspect every final
page render and verify TOC numbers against Word pagination. Word native export is
the renderer fallback because packaged render_docx.py fails: no soffice.exe on PATH.
