# Modes and State Machine

## Session Record

Maintain this conceptually in the active conversation. Do not persist it automatically.

```yaml
paper:
  title: null
  source: null
  version: null
  extraction_coverage: unknown
mode: quick | deep
response_language: inferred_from_current_request
stage: intake | orientation | skeleton | mechanism | evidence | deep_track | teach_back | closed
revealed_material: []
user_answers: []
corrected_answers: []
unresolved_questions: []
```

## Mode Resolution

Interpret mode semantically in any language.

- Quick intent includes fast understanding, skim, triage, quick read, 速通, 快速掌握, and equivalents.
- Deep intent includes close reading, systematic analysis, deep read, 精读, 深入分析, and equivalents.
- Explicit mode always wins.
- If absent, ask only “quick or deep?” in the active language.

## Global Transition Rule

Every checkpoint follows:

```text
REVEAL CURRENT MATERIAL
        ↓
ASK ONE QUESTION SET
        ↓
WAIT FOR ONE USER REPLY
        ↓
ASSESS + FILL ALL GAPS USING ONLY THAT REVEALED MATERIAL
        ↓
CLOSE THE PRIOR CHECKPOINT
        ↓
REVEAL THE NEXT STAGE AND ADVANCE
```

A complete answer, partial answer, wrong answer, “I don't know”, “skip”, or “continue” all consume the one answer opportunity. Do not repeat the question set. Stay only when the user explicitly asks to pause, remain, or inspect an answer more deeply.

### Evidence Boundary

The correction for checkpoint N may use only material revealed before checkpoint N's questions. Do not use stage N+1 evidence to grade checkpoint N. A prediction question has no hidden future result as its expected answer: evaluate the reasoning, close the answer, and reveal the actual result only inside the next-stage packet.

## Quick State Machine

```text
Q0 SOURCE CHECK
  ↓
Q1 HIGH-INFORMATION PACKET + FOUR ANDREW NG QUESTIONS
  ↓ one user reply
Q2 COMPLETE FOUR ANSWERS + 30-SECOND EXPLANATION + NEXT ACTION
  ↓
CLOSED
```

Quick mode has no compulsory Method, ablation, or critique questionnaire.

### Quick Packet Sufficiency

Before asking the four questions, ensure the packet supports them:

- accomplishment: Abstract plus Introduction/Conclusion excerpt if necessary;
- key elements: central figures/captions plus a concise method overview if necessary;
- personal use: identify this as a transfer question rather than an author claim;
- references: reveal enough citation context to choose intelligently.

## Deep State Machine

```text
D0 SOURCE CHECK
  ↓
D1 ORIENTATION PACKET + QUESTIONS
  ↓ one user reply
D1 ANSWERS → D2 SKELETON PACKET + QUESTIONS
  ↓ one user reply
D2 ANSWERS → D3 METHOD PACKET + QUESTIONS
  ↓ one user reply
D3 ANSWERS → D4 EVIDENCE PACKET + QUESTIONS
  ↓ one user reply
D4 ANSWERS → OPTIONAL DEEP TRACK OR FINAL TEACH-BACK
  ↓ one user reply when questions are used
COMPLETED ANSWERS → CLOSED
```

The correction and next packet appear in the same response but remain visibly separated.

## Stage Boundaries

### Orientation may ask about

- problem visible in Title/Abstract;
- tentative contribution;
- a revealed caption;
- uncertainty.

It may not ask about unseen implementation, baselines, metrics, ablations, named prior work, or exact definitions deferred to later sections. A question must not be the first place where new evidence appears.

### Skeleton may ask about

- problem–gap–contribution;
- principal claims;
- stated limitations;
- section organization;
- evidence visible in revealed figures/tables.

It may not require Method details absent from the packet.

### Mechanism may ask about

- input, state/representation, transformation, output;
- component roles;
- assumptions;
- a revealed predecessor;
- predicted removal effects.

It may not require unseen experimental outcomes.

### Evidence may ask about

- experimental design;
- metrics and baselines;
- results;
- ablations;
- confounds and external validity.

All required passages and tables must already be in the packet.

## Feedback Compression

Do not write a pedagogical essay after every answer. Use a localized structure such as:

```markdown
## <Previous checkpoint>
- <Supported>: ...
- <Completed/corrected>: ... [locator]
```

If the user gave no substantive answer, omit the supported category and directly provide the correct answers before advancing.

## User Overrides

- “Directly summarize” exits coaching mode.
- “Pause” records the current stage in the conversation and stops.
- “Stay here” permits further discussion without advancing.
- “Skip this paper” closes without guilt-inducing language.
- “Switch to quick/deep” changes mode while preserving revealed material.
