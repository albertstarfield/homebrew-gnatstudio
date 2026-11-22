# Humanizer pass-through attempts

The local OpenAI-compatible endpoint at `http://localhost:1234/v1` is reachable. `GET /v1/models` returned HTTP 200 with model `humanizer-1B-OptiQ-4bit` (`evidence/local-v1-probe-parent.log:1`).

Two full README passes were made with `POST /v1/chat/completions`:

- `evidence/humanizer-response-Alire.json` (first pass, model id `humanizer`): 6,801 characters, looped on `to alire to alire ...`, dropped the fenced commands.
- `evidence/humanizer-response-Alire-v2.json` (second pass, correct model id, frequency and presence penalties): 129 characters, no code blocks, no one-line install.
- `evidence/humanizer-response-GNATStudio-v2.json`: 5,703 characters, but the one-line install commands are absent and upstream names are garbled (`gnu apple`, `albert`).

None of those outputs preserved the commands, so they were not applied. The READMEs in this repository were rewritten by hand using the humanizer skill's rules, and the exact commands were kept. The endpoint attempt is retained here as evidence, not as the source of the shipped text.
