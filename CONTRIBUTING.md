# Contributing to Paper Coach

Thank you for improving research-paper reading as a learning process rather than a summary-generation task.

## Good contributions

- discipline-specific checkpoint questions;
- multilingual section and caption handling;
- stronger evidence-grounding rules;
- math, code, reproduction, and review tracks;
- small helper scripts with clear optional dependencies;
- evaluations that test reader understanding, calibration, or transfer;
- corrections to inaccurate or overly broad claims in the documentation.

## Design invariants

Changes must preserve:

1. one user-answer opportunity per checkpoint;
2. no repeated hint loop unless the user asks to remain;
3. questions and corrections grounded only in already revealed material;
4. explicit separation of source text, translation, reader interpretation, and coach inference;
5. transparent extraction and figure limitations;
6. no silent persistence of user reading data;
7. harness-neutral core behavior.

## Development

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

If available:

```bash
uvx --from skills-ref agentskills validate skills/paper-coach
```

## Pull requests

- Keep `SKILL.md` focused; move detailed material into `references/`.
- Add or update tests for behavioral rules or scripts.
- Update `CHANGELOG.md` for user-visible changes.
- Do not include private papers, copyrighted transcripts, credentials, personal paths, or generated reading logs.
- Explain which harnesses or paper types were tested.

## Attribution

Do not imply endorsement by Andrew Ng, Stanford, or deeplearning.ai. The project may cite the public CS230 lecture and summarize its method in original wording, but must not redistribute the transcript.
