# output

Persistent outputs and generated artifacts produced by the agent while working on the project.

## What belongs here

* reports, analyses, and summaries;
* generated documentation;
* diagrams and visual artifacts;
* exports and generated data files;
* other persistent task results that are not part of the project source code;
* topical subdirectories when useful, e.g.:

```text
output/
├── reports/
├── analyses/
├── diagrams/
├── exports/
└── generated/
```

## Rules

* Use this directory for persistent deliverables, not temporary working files.
* Temporary investigation files belong in `../scratch/`.
* Knowledge that should be remembered across sessions belongs in `../memory/`.
* Files that are part of the actual software project belong in `../project/`.
* The agent may create, update, reorganize, rename, and remove obsolete output files as needed.
* This file (`README.md`) is the only file from this directory tracked in GitHub — see `.gitignore` in the root directory.
