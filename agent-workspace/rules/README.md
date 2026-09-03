# rules

Contains durable rules and constraints that the agent must follow while working with configured projects.

## What belongs here

* mandatory project constraints;
* coding rules;
* testing requirements;
* security requirements;
* architectural boundaries;
* dependency restrictions;
* compatibility requirements;
* Git and release rules;
* data-handling constraints;
* rules describing files or areas that must not be modified manually;
* other durable requirements that future agents must consistently respect.

Rules should describe **what must or must not happen**.

They should be explicit, stable, and enforceable.

Instructions describing how the agent should perform work belong in `prompts`.

## Rules

* The agent MUST read rules relevant to the current task before modifying affected project code.
* Rules may apply globally or to a specific configured project.
* Project-specific rules must be clearly attributable to the project they apply to.
* Rules for one project MUST NOT automatically be applied to another project.
* Global rules apply to all configured projects unless explicitly scoped otherwise.
* Project-specific rules may introduce additional or stricter constraints.
* The agent MUST NOT silently ignore, weaken, or override an applicable rule.
* New rules should only be added when a durable mandatory constraint has been verified.
* Preferences, temporary observations, recommendations, and unverified assumptions must not be stored as rules.
* If an existing rule becomes outdated, incorrect, duplicated, or obsolete, the agent should update or reorganize it when appropriate.
* Explicit user-defined rules must not be materially changed or removed without a valid reason.
* If a rule is superseded by an important technical or architectural decision, preserve the relevant reasoning in `decisions` where appropriate.
* This file (`README.md`) is the only file from this directory that is expected to be tracked by default when no project-specific rules have yet been created — see `.gitignore` in the root directory if applicable.
