# Extraction and Grounding

## Goal

Build two conceptual views of a paper:

1. a **structural view** for headings, sections, captions, and reading packets;
2. a **location view** for pages, sections, figures, tables, or line references.

Do not expose the whole extraction merely because it was parsed internally.

## Harness-Neutral Intake

Use the best capabilities available in the current agent harness:

1. native PDF/file reader;
2. remote webpage or PDF extraction;
3. OCR for scanned pages;
4. vision for figures when available;
5. shell/helper scripts only when they materially improve structure or page mapping.

The core coaching workflow must still work when none of the optional local tools are present. In that case, use exact section/figure locators and disclose that page mapping is unavailable.

## Optional Local PDF Helper

If the harness can run Python and the environment has Miyo plus Poppler `pdftotext`, run:

```text
python scripts/build_paper_map.py paper.pdf --out-dir .paper-coach/paper-name
```

The helper:

- asks Miyo for Markdown structure;
- uses `pdftotext -layout` to retain form-feed page boundaries;
- writes `paper.md`, `map.json`, and one text file per PDF page;
- maps headings and common multilingual Figure/Table captions to pages;
- prints a compact summary rather than the full paper.

It uses only Python's standard library but depends on external `miyo` and optionally `pdftotext` executables. If unavailable, fall back to harness-native readers. Do not install large dependencies without user approval.

## Coverage Gate

Before coaching, inspect when possible:

- page/section count;
- failed or OCR-needed pages;
- text-based versus scanned content;
- presence of Abstract, major sections, captions, references, and appendices;
- whether the agent can inspect figure visuals or only captions.

If extraction is incomplete, state exactly what is missing. Do not treat an empty text layer as an empty paper.

## Remote Sources

1. Prefer the canonical paper page or PDF URL.
2. If exact pages matter, obtain the PDF and build a local page map when allowed.
3. If only webpage text is accessible, cite section names and figure/table identifiers.
4. If access is blocked, say so and use an authorized fallback; never invent missing content.

## Plain Text or Markdown

Detect structure from headings, numbering, and semantics. Cite exact heading names, paragraph context, or provided line numbers. Do not fabricate PDF pages for a source that has none.

## Multilingual Papers

- Do not search only for English strings such as “Abstract” or “Conclusion”.
- Use heading hierarchy, numbering, and semantic meaning.
- Preserve exact source-language heading names in locators.
- The helper recognizes several common caption labels, but the list is not exhaustive; inspect likely caption lines semantically when needed.

## Figures and Tables

Text extraction may provide only a caption, not the visual content.

- Cite `[Fig. N caption, PDF p. X]` when only the caption was available.
- Do not claim to have inspected curves, colors, arrows, spatial layout, or axis values absent from extracted text.
- If the harness has rendering or vision capability, inspect the relevant page before asking visual questions.
- Otherwise give the user the exact figure and page to inspect.

## Evidence Locators

Use the most specific available form:

- `[Abstract, PDF p. 1]`
- `[§3.2 Dense Connectivity, PDF p. 4]`
- `[Fig. 2 caption, PDF p. 3]`
- `[Table 4, PDF p. 7]`
- `[Conclusion]` when page mapping is unavailable.

PDF page means the 1-indexed page shown by a PDF viewer, not a guessed printed footer.

## Claim Classification

Distinguish:

- **Paper states:** directly supported by the paper;
- **Reader interpretation:** the user's reconstruction;
- **Coach inference:** the agent's transfer idea or critique;
- **Open question:** unresolved by available evidence.

“What can you use yourself?” is a transfer question, not a paper claim.

## Question Grounding Audit

For every question, identify its answer basis internally:

```yaml
question: What role does the retrieval module play?
answer_basis:
  - Section 3.2 already shown in this checkpoint
  - Figure 2 caption already shown in this checkpoint
status: answerable
```

If the source was not revealed, add it to the packet or postpone the question. Do not use future-stage evidence to complete a prior checkpoint.

## Fallback Order

1. Harness-native PDF/file/URL reader.
2. Optional local helper for structure and pages.
3. OCR for scanned pages.
4. Vision for figures when available.
5. Transparent section-only citations when page mapping cannot be recovered.

At every fallback, retain the one-answer-opportunity behavior.
