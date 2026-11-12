# hEDSpace

Code for the hEDS investigation in the All of Us Researcher Workbench.

Workspace: https://workbench.verily.com/workspaces/heds-investigation

## Development workflow

Write and review code locally, push code changes to GitHub, then pull and execute
inside the Verily cloud app. This is a Git workflow, not a live remote connection.
Keep participant data and analysis outputs inside Workbench. The ignored `data/`
and `outputs/` folders are for cloud use; Git ignore rules are not an export control.
Do not commit credentials or notebook outputs containing research data.

The workspace uses the `AoU Jupyter` app, with a one-hour idle autostop requested.
App disks continue to incur charges while stopped.

## First run inside the cloud app

Open a Jupyter terminal and locate the automatically cloned `hEDSpace` directory.
If it is absent, run `wb git clone --all` from the directory where you want it.

```bash
cd hEDSpace
git pull --ff-only
python -m pip install -r requirements.txt
wb resource list
```

Find the BigQuery dataset reference for the All of Us CDR in the workspace's
Resources tab or `wb resource list`. Resolve its resource ID with
`wb resource resolve --id RESOURCE_ID`. Use the actual project.dataset;
do not assume the legacy WORKSPACE_CDR environment variable is present.

```bash
python scripts/check_environment.py \
  --project wb-spotless-pecan-6923 \
  --dataset wb-silky-artichoke-2408.C2025Q4R6
```

This checks dataset/table metadata using the cloud app's existing credentials.
It does not query participant rows or download data. If access fails, confirm the
appropriate All of Us data collection is attached and your access is current.
Do not create or download service-account keys.

## Analysis to develop next

Define the hEDS phenotype and comparison cohort before training a classifier.
An EDS diagnosis code alone should not be assumed to identify hEDS specifically.
Select the CDR release, genomic representation, inclusion criteria, covariates,
and participant-level train/test split before implementing the analysis.
Large genomic analyses may need the separate Spark/Hail app; this Jupyter app is
the starting point for environment checks and phenotype development.
