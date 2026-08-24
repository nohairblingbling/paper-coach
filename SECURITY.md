# Security Policy

## Supported versions

Security fixes are applied to the latest release.

## Reporting a vulnerability

Please open a private GitHub security advisory for the repository rather than a public issue when the report involves:

- credential exposure;
- command injection in helper scripts;
- unsafe path handling;
- malicious or hidden instructions in packaged skill files;
- unintended disclosure of private paper content or reading logs.

## Data-handling posture

Paper Coach is an instruction skill. The core workflow does not require a network service and does not automatically persist paper content, user answers, or reading logs. Optional extraction is performed by capabilities available in the host agent or by the local helper selected by the user/agent.

Third-party agent harnesses and document parsers have their own security and privacy properties. Review them before using private or unpublished papers.
