# Andrew Ng's Paper-Reading Method

## Source and Attribution

This reference distills, in original wording, the paper-reading workflow taught by Andrew Ng in Stanford CS230 Lecture 8:

- **Video:** [Stanford CS230: Deep Learning | Autumn 2018 | Lecture 8 — Career Advice / Reading Research Papers](https://www.youtube.com/watch?v=733m6qBH-jI)
- **Paper-reading segment:** approximately 2:25–29:40
- **Single-paper multiple-pass discussion:** approximately 6:25 onward

Paper Coach is an independent open-source adaptation. It is not affiliated with, sponsored by, or endorsed by Andrew Ng, Stanford University, Stanford Online, deeplearning.ai, or the course staff.

## 1. Reading a Body of Literature

Andrew Ng describes learning a field as a non-linear process:

1. Assemble an initial list of papers and serious supporting resources.
2. Skim across the list rather than reading every paper from first word to last.
3. Drop low-value or clearly irrelevant papers early.
4. Identify seminal or especially relevant papers and invest more time in them.
5. Follow citations selectively, adding new papers as the map of the field improves.
6. Return to partially read papers when later context makes them more valuable.

The lecture offers rough volume guidance:

- **5–20 papers:** basic working familiarity—often enough to understand or apply an area;
- **50–100 well-understood papers:** strong knowledge of an area, closer to research-level command.

These are heuristics, not mastery scores. Relevance, difficulty, diversity, and depth of understanding matter more than raw counts.

## 2. Multiple Passes Through One Paper

### Pass 1 — Highest Information Density

Read:

- title;
- Abstract;
- figures and figure captions, especially the central architecture or result figures.

Goal: form a fast, provisional model of what the paper is about without reading linearly.

### Pass 2 — Build the Paper Skeleton

Read:

- Introduction;
- Conclusion or Discussion;
- all major figures again;
- skim the rest.

Related Work can be deferred when the reader is new to the field. Abstract, Introduction, and Conclusion are often carefully optimized to communicate the paper's acceptance case, so they are high-information sections.

### Pass 3 — Working Understanding

Read the prose of the paper while initially skipping dense mathematical details. Preserve momentum. It is acceptable to move past a difficult or apparently low-value passage and return only if it becomes necessary.

### Pass 4 — Deep Understanding

Return to the parts that matter for the actual goal:

- re-derive important mathematics from a blank page;
- run available code;
- reimplement the core method from scratch;
- follow essential references;
- test whether the claimed mechanism survives close scrutiny.

## 3. Four Quick-Mastery Questions

Andrew Ng proposes four questions as a compact test of understanding:

1. **What did the authors try to accomplish?**
2. **What were the key elements of the approach?**
3. **What can you use yourself?**
4. **What other references do you want to follow?**

Paper Coach uses these four questions exactly once in quick mode and once in the final teach-back of deep mode.

## 4. Mathematics and Code as Understanding Tests

For mathematics:

1. read and annotate the derivation;
2. put the paper aside;
3. reproduce the derivation from a blank page;
4. compare and locate missing assumptions or steps.

For code:

- running the authors' implementation is a lightweight test;
- reimplementing the core method is a deeper test of understanding.

## 5. Consistency Beats Cramming

The lecture emphasizes steady practice over isolated bursts. Reading a few papers every week builds pattern recognition: architecture tables, result layouts, experimental conventions, and recurring argumentative structures become easier to parse over time.

## 6. What Paper Coach Adds

Paper Coach preserves the multiple-pass order while adding explicit interaction design:

- **Quick mode:** one checkpoint using only the four questions;
- **Deep mode:** stage-specific questions for orientation, structure, mechanism, evidence, and optional deep work;
- **one answer opportunity:** missing answers are completed immediately on the next turn;
- **local evidence boundary:** questions and corrections can use only material already revealed for that checkpoint;
- **multilingual delivery:** coaching follows the prompt language while source quotations remain identifiable.

These additions are Paper Coach's design choices, not claims that Andrew Ng prescribed this exact dialogue protocol.
