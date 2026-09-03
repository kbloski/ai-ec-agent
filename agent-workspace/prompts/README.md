# prompts

Stable, long-lived project instructions for the agent (e.g. `CODE.md`).

## What belongs here

* project-specific coding conventions;
* stable development commands (build, test, lint, deploy);
* architecture overview and important project directories;
* testing conventions;
* constraints and rules the agent must follow.

## Rules

* The agent may update these files on its own whenever it discovers new, stable information about the project.
* The agent does not silently override explicit user instructions stored in the prompts.
* This file (`README.md`) is the only file from this directory tracked in GitHub — see `.gitignore` in the root directory.
