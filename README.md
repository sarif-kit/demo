# sarif-kit demo

This repository is broken on purpose.

It shows what [sarif-kit](https://github.com/sarif-kit/sarif-kit) does: it takes the output
of tools that cannot emit SARIF and turns it into GitHub Code Scanning alerts. Everything
under Security, then Code scanning, came from the workflows in `.github/workflows/`. Each
one runs a single tool and converts its output with the sarif-kit action.

## What is wrong here, deliberately

| File | Problem | Tool that finds it |
|---|---|---|
| `requirements.txt` | two long-outdated packages with published advisories | pip-audit |
| `config/service.yaml` | duplicate key, bad indentation, loose spacing, a truthy value | yamllint |
| `src/billing.py` | a dozen misspellings | codespell |

Nothing here is real code. The point is the alerts, not the program.

## The shape of a workflow

Run the tool the way you already do, convert what it printed, upload the result:

```yaml
- name: Lint YAML
  run: pipx run yamllint -f parsable . > yamllint.txt || [ $? -eq 1 ]
- name: Convert to SARIF
  uses: sarif-kit/sarif-kit@v0.1.0
  with:
    tool: yamllint
    input: yamllint.txt
    output: yamllint.sarif
- name: Upload to Code Scanning
  uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: yamllint.sarif
    category: yamllint
```

The guard on the first line is the part people miss. Most linters exit nonzero when they
find something, and you want the job to carry on to the upload rather than stop at the
scan. Each tool exits differently, so the per-tool pages in the main repository give the
exact command for each one.

Each workflow uploads under its own `category`. Without that, the three tools overwrite
each other's alerts.
