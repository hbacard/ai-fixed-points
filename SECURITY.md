# Security Policy

## Reporting a vulnerability

If you find a security vulnerability in this project, please report it
**privately** before opening a public issue, so we can address it before it is
widely disclosed.

- **Email**: hugo.bacard@ijclab.in2p3.fr
- **Subject**: `[ai-fixed-points] Security vulnerability`

Please include as much of the following as possible:

- A description of the vulnerability and the affected version(s).
- Steps to reproduce it.
- Any proof-of-concept code (without credentials or secrets).
- The impact you believe the flaw has.

We aim to acknowledge reports within 5 business days and will keep you informed
as we work on a fix.

## Supported versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | ✅ (current)       |

## Security considerations

The project loads secrets from a gitignored `.env` file and machine-specific
settings from a gitignored `config.yaml`. Never commit these files; a template
(`config.yaml.example`) is provided instead.
