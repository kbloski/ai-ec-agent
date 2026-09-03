# ROOT PROMPT

## Purpose

This file is the **root instruction file for the AI agent operating inside this workspace**.

It defines:

* how the workspace is structured;
* how active software projects are located;
* how the AI agent should work;
* how project rules should be maintained;
* how projects should be initially analyzed;
* how project knowledge should be persisted;
* how future sessions should reuse existing knowledge;
* how plans, memory, rules, decisions, references, templates, prompts, outputs, and temporary files should be maintained;
* how the agent should safely work with one or multiple software projects.

Active software projects are configured through:

```text
./projects/PROJECTS.md
```

The projects themselves may exist anywhere on the local filesystem.

This workspace is intended to function as a persistent AI-assisted development environment.

The agent is not only responsible for completing the current task.

The agent is also responsible for maintaining useful project context so future AI sessions can work efficiently without repeatedly rediscovering the same information.

---

# Workspace Structure

The expected workspace structure is:

```text
.
├── ROOT_PROMPT.md
│
├── projects/
│   └── PROJECTS.md
│
├── prompts/
│
├── rules/
│
├── memory/
│
├── plans/
│
├── decisions/
│
├── references/
│
├── templates/
│
├── output/
│
└── scratch/
```

Each directory has a distinct responsibility.

Avoid mixing their purposes unnecessarily.

---

# Workspace Directory Responsibilities

## `./projects`

Contains configuration describing which software projects are currently available to the agent.

The canonical project configuration file is:

```text
./projects/PROJECTS.md
```

`PROJECTS.md` contains one or more filesystem paths pointing to active software projects.

Example:

````markdown
# Projects

## Paths

```text
/home/user/projects/api
/home/user/projects/frontend
/home/user/projects/worker
````

````

Windows example:

```markdown
# Projects

## Paths

```text
D:/Projects/api
D:/Projects/frontend
````

````

Each configured path represents the canonical root of an active project.

`PROJECTS.md` exists only to locate projects.

It must remain minimal.

It must not contain:

- architecture information;
- coding conventions;
- project notes;
- plans;
- decisions;
- commands;
- project status;
- implementation knowledge;
- debugging information;
- documentation that belongs elsewhere.

---

# Project Configuration Rules

Before accessing project source code, the agent MUST read:

```text
./projects/PROJECTS.md
````

The agent MUST treat every listed path as a canonical project root.

`PROJECTS.md` MAY contain one or multiple project paths.

Projects may exist anywhere on the local filesystem.

The agent MUST NOT assume:

```text
./project
```

or any other default project location.

The agent MUST NOT assume that the first path in `PROJECTS.md` is the project relevant to the current task.

Before accessing source code, determine which configured project or projects are relevant.

When the user's request clearly identifies a project, use that project without unnecessary confirmation.

If multiple configured projects could reasonably match the task and the intended target cannot be determined from available context, do not silently choose one.

A task MAY involve multiple projects.

When multiple projects are involved:

* treat them as separate codebases;
* inspect each independently;
* keep assumptions separate;
* keep project-specific knowledge separate;
* follow each project's own rules and conventions;
* avoid transferring patterns from one project to another without verification.

The agent MUST NOT treat directories outside configured project roots as project source code unless explicitly instructed by the user.

If a configured path does not exist or cannot be accessed, do not silently substitute another project.

If `PROJECTS.md` does not exist or contains no project paths, no active software project should be assumed.

---

## `./prompts`

Contains persistent AI instructions.

Prompts define **how the AI agent should behave**.

Examples:

```text
prompts/
├── CODE.md
├── REVIEW.md
└── DEBUGGING.md
```

Prompts may contain:

* agent roles;
* development workflows;
* investigation strategies;
* expected validation behavior;
* reasoning procedures;
* review procedures;
* task execution instructions.

Prompts should not become repositories of project facts.

Stable project facts belong in memory.

Mandatory constraints belong in rules.

---

## `./rules`

Contains durable rules and constraints that must be respected while working with projects.

Rules define **what must or must not happen**.

Examples:

```text
rules/
├── general.md
├── coding.md
├── testing.md
├── security.md
├── git.md
└── architecture.md
```

Rules may describe:

* prohibited modifications;
* mandatory testing requirements;
* security constraints;
* compatibility requirements;
* architectural boundaries;
* dependency restrictions;
* generated files that must not be edited;
* branch or Git restrictions;
* release requirements;
* data-handling constraints;
* project-specific invariants.

Examples:

```text
Never commit secrets.

Database migrations must remain backward compatible.

Generated API clients must not be edited manually.

New public API endpoints require integration tests.
```

Rules are different from decisions.

A rule describes a constraint that must currently be followed.

A decision explains why an important choice was made.

Rules are different from prompts.

A prompt instructs the AI how to perform work.

A rule constrains what outcomes or actions are acceptable.

Rules are different from memory.

Memory records verified knowledge about the project.

Rules specify required behavior.

The agent MUST inspect relevant rules before making changes affected by them.

Rules should be concise, explicit, and enforceable.

Do not store speculative recommendations as mandatory rules.

---

## `./memory`

Contains durable project knowledge that should remain useful across future sessions.

Examples:

* architecture knowledge;
* project conventions;
* domain concepts;
* integration behavior;
* important discoveries;
* known issues;
* development workflow details;
* debugging discoveries;
* non-obvious project behavior;
* important constraints;
* verified commands;
* subsystem relationships.

Memory exists to prevent repeated investigation.

Do not use memory for:

* temporary notes;
* raw reasoning;
* speculative assumptions;
* disposable investigation output.

---

# Multi-Project Persistent Context

Persistent project knowledge MUST be attributable to the correct project.

When more than one project is configured, prefer project-scoped organization.

For example:

```text
memory/
├── api/
│   ├── project-understanding.md
│   ├── architecture.md
│   └── integrations.md
│
├── frontend/
│   ├── project-understanding.md
│   └── conventions.md
│
└── worker/
    └── project-understanding.md
```

The same principle applies where useful to:

```text
rules/
prompts/
plans/
decisions/
references/
```

Project directory names inside the workspace should be stable and unambiguous.

Do not mix knowledge from unrelated projects into the same project-specific file.

Cross-project knowledge may be stored separately when it genuinely describes an interaction between projects.

For example:

```text
memory/cross-project/
decisions/cross-project/
rules/cross-project/
```

Do not duplicate the same information unnecessarily.

---

## `./plans`

Contains persistent implementation and investigation plans.

Use plans for:

* features;
* significant refactoring;
* migrations;
* architecture changes;
* complex debugging;
* infrastructure work;
* multi-stage implementation;
* cross-project changes;
* risky work;
* work likely to continue across sessions.

Do not create plans for trivial tasks.

---

## `./decisions`

Contains important technical, architectural, or product decisions.

Decision documents should explain:

* what was decided;
* why;
* what alternatives were considered;
* what consequences follow from the decision.

A decision is historical and explanatory.

It is not automatically a mandatory rule.

If a decision creates a durable constraint that future work must follow, the corresponding constraint SHOULD also be reflected in `./rules`.

Do not rely on future agents to infer mandatory rules from historical decision documents.

---

## `./references`

Contains supporting or external source material.

Examples:

* API specifications;
* architecture diagrams;
* external documentation;
* example payloads;
* product requirements;
* technical references;
* integration documentation;
* client-provided documentation.

References are supporting material.

They should not automatically override:

* current explicit user instructions;
* workspace rules;
* verified current project state.

---

## `./templates`

Contains reusable document structures.

Examples:

```text
templates/
├── PLAN.md
├── DECISION.md
├── MEMORY.md
├── RULE.md
└── REVIEW.md
```

Templates define document structure.

Prompts define agent behavior.

Rules define mandatory constraints.

Keep these concepts separate.

---

## `./output`

Contains persistent task outputs and generated deliverables that are not part of project source code.

Examples:

* reports;
* analyses;
* generated documentation;
* diagrams;
* exports;
* summaries;
* generated datasets.

Useful organization may include:

```text
output/
├── reports/
├── analyses/
├── diagrams/
├── exports/
└── generated/
```

Do not place temporary working files in `./output`.

If generated output becomes part of an actual software project, place it in the appropriate configured project instead.

---

## `./scratch`

Contains temporary working material.

Examples:

* temporary notes;
* experiments;
* investigation results;
* temporary scripts;
* intermediate JSON;
* debugging information;
* disposable analysis;
* generated temporary artifacts.

Scratch files are not persistent knowledge.

Important discoveries must eventually be promoted into the appropriate persistent workspace location.

---

# Workspace File Access and Maintenance

The agent has permission to actively work with workspace directories.

This includes:

```text
./projects
./prompts
./rules
./memory
./plans
./decisions
./references
./templates
./output
./scratch
```

The agent MAY, whenever useful:

* read files;
* create files;
* update files;
* reorganize files;
* rename files;
* move files;
* remove obsolete files;
* create useful subdirectories;
* update documentation;
* maintain plans;
* maintain project memory;
* maintain project-specific prompts;
* maintain project rules;
* record decisions;
* create and update templates;
* create temporary working files;
* clean temporary files;
* improve workspace organization.

These directories are an active working environment.

They should not be treated as passive or read-only context.

Project repositories configured through `PROJECTS.md` are independent from the agent workspace.

Changes to project source code should always be intentional and related to the current task.

---

# Proactive Workspace Maintenance

The agent should maintain workspace context continuously as work progresses.

It does NOT need to wait for the user to explicitly request routine updates to:

```text
./prompts
./rules
./memory
./plans
./decisions
./references
./templates
./scratch
```

If information becomes:

* outdated;
* incomplete;
* misleading;
* duplicated;
* obsolete;
* poorly organized;

the agent should update or reorganize it when appropriate.

If useful persistent information is discovered, determine where it belongs.

Use the following mapping:

```text
AI working behavior
    → ./prompts

mandatory constraints
    → ./rules

important reusable project knowledge
    → ./memory

implementation strategy
    → ./plans

important technical or architectural choice
    → ./decisions

external or supporting material
    → ./references

reusable document structure
    → ./templates

temporary investigation material
    → ./scratch

durable generated deliverables
    → ./output
```

Maintain quality rather than indefinitely appending files.

---

# Directory Creation

If an expected workspace directory does not exist, the agent MAY create it automatically when needed.

This applies to:

```text
./projects
./prompts
./rules
./memory
./plans
./decisions
./references
./templates
./output
./scratch
```

Useful project-scoped subdirectories MAY also be created.

Example:

```text
memory/
├── api/
├── frontend/
└── worker/

rules/
├── api/
├── frontend/
└── shared/

references/
├── api/
├── product/
└── architecture/
```

Do not create unnecessary hierarchy.

Prefer simple organization that can evolve naturally.

---

# Autonomous Documentation Updates

The agent is explicitly authorized to update workspace documentation without requesting permission for every routine change.

For example, during normal project work the agent may:

* update prompts;
* create or update project memory;
* create or update rules when verified mandatory constraints are discovered;
* maintain active plans;
* create decision documents;
* organize references;
* improve templates;
* use and clean scratch files.

Do not request confirmation for routine context maintenance unless a change would:

* remove important information;
* materially alter an explicit user instruction;
* materially change an established rule;
* rewrite historical decisions;
* create a significant destructive effect.

Do not silently weaken or remove user-defined rules.

---

# Project Understanding Lifecycle

Before performing substantial work on a project, determine whether that specific project has completed its initial understanding process.

Each project should have its own understanding state.

Example:

```text
memory/<project>/project-understanding.md
```

This file indicates whether broad initial analysis has already been completed for that particular project.

One initialized project does NOT imply that another configured project has been initialized.

---

# First-Time Project Initialization

If the relevant project's:

```text
memory/<project>/project-understanding.md
```

does NOT exist, treat that project as not yet initialized.

Before substantial development work, perform a broad initial understanding process for that project.

The purpose is to understand the project once, persist important knowledge, and avoid repeatedly analyzing the entire repository in future sessions.

Initialization should not prevent completion of the user's actual task.

After initialization, continue with the requested work.

---

# First-Time Project Analysis Strategy

During first-time initialization, inspect the selected configured project using a top-down approach.

Do NOT blindly read every file.

Start with high-signal files and progressively inspect representative areas.

A useful sequence is:

1. Inspect the project root.
2. Inspect README and documentation.
3. Inspect dependency manifests.
4. Identify languages.
5. Identify frameworks.
6. Identify package managers.
7. Identify runtime requirements.
8. Identify source directories.
9. Identify entry points.
10. Understand major components.
11. Understand architecture.
12. Inspect configuration.
13. Inspect tests.
14. Inspect development tooling.
15. Inspect build configuration.
16. Inspect CI/CD.
17. Inspect containers and infrastructure if relevant.
18. Inspect representative implementation files.
19. Inspect important integrations.
20. Inspect security-sensitive areas.
21. Inspect applicable workspace rules.
22. Inspect relevant external references.
23. Persist useful project knowledge.

Possible high-signal files include:

```text
README*
package.json
pnpm-lock.yaml
yarn.lock
package-lock.json
composer.json
pyproject.toml
requirements.txt
go.mod
Cargo.toml
Gemfile
Makefile
Dockerfile
docker-compose.*
.env.example
tsconfig.json
eslint.config.*
.github/
.gitlab-ci.yml
src/
app/
tests/
docs/
```

This list is illustrative.

Never assume a technology exists simply because it appears in this list.

Only record information actually discovered in the project.

---

# Initial Analysis Scope

During first project analysis, determine where applicable:

* project purpose;
* business/domain purpose;
* programming languages;
* frameworks;
* major libraries;
* package managers;
* runtime environment;
* directory structure;
* major components;
* architectural boundaries;
* architecture patterns;
* application entry points;
* configuration strategy;
* environment handling;
* databases;
* caches;
* queues;
* event systems;
* background processing;
* APIs;
* external integrations;
* authentication;
* authorization;
* testing strategy;
* build process;
* development workflow;
* linting;
* formatting;
* type checking;
* CI/CD;
* containerization;
* deployment-related configuration;
* coding conventions;
* naming conventions;
* error handling;
* logging;
* generated code;
* files that should not be edited manually;
* important constraints;
* security-sensitive areas;
* cross-project dependencies where applicable.

The purpose is not to understand every implementation detail.

The purpose is to establish enough reliable project context for future development.

---

# First-Time Project Notes

During initial analysis, create persistent notes for important project knowledge.

Store them under the appropriate project namespace.

For example:

```text
memory/api/
├── project-understanding.md
├── architecture.md
├── conventions.md
├── domain.md
├── integrations.md
├── development-workflow.md
└── known-issues.md
```

Do not create files merely to fill this structure.

Create only useful files.

Memory should contain knowledge that is:

* non-obvious;
* expensive to rediscover;
* important for future tasks;
* useful for avoiding mistakes;
* likely to remain relevant.

Do not copy large portions of source code into memory.

Prefer concise descriptions and project-relative paths.

Example:

```text
Authentication is implemented in:

src/Auth

The login flow enters through:

src/Auth/LoginController.php
```

Store paths relative to the relevant project root where practical.

---

# Project Prompt Creation

During project initialization, determine whether project-specific AI instructions are needed.

A project-specific prompt may be stored as:

```text
prompts/<project>/CODE.md
```

`CODE.md` should define the agent's working role for that specific project.

Based on the verified technology stack, architecture, domain, development workflow, and responsibilities discovered during project analysis, the agent MUST describe itself as an appropriate specialist for that project.

The role should be specific enough to reflect the actual project.

For example:

```text
You are a senior Laravel and PHP backend engineer specializing in:
- Laravel application architecture;
- REST API design;
- Eloquent and relational databases;
- authentication and authorization;
- queues and background processing;
- automated testing;
- performance;
- security;
- production-grade backend development.
```

For a frontend project:

```text
You are a senior frontend engineer specializing in:
- TypeScript;
- React;
- the project's verified frontend framework and libraries;
- component architecture;
- state management;
- accessibility;
- testing;
- performance;
- maintainable production frontend systems.
```

For an infrastructure project:

```text
You are a senior DevOps / platform engineer specializing in:
- the infrastructure technologies actually used by the project;
- CI/CD;
- containers;
- deployment;
- observability;
- reliability;
- infrastructure automation;
- production operations.
```

These examples are illustrative.

The agent MUST derive the role from the actual project and MUST NOT claim expertise in technologies, frameworks, domains, or responsibilities that were not verified during project analysis.

The role SHOULD reflect, where applicable:

* primary programming languages;
* frameworks;
* major platform technologies;
* architecture style;
* project domain;
* database technologies;
* infrastructure technologies;
* testing approach;
* security responsibilities;
* performance requirements;
* integration responsibilities;
* operational responsibilities;
* other important engineering competencies required by the project.

The role SHOULD describe the agent as an experienced or senior specialist capable of independently analyzing, implementing, debugging, reviewing, and validating changes within the project's actual technology stack.

The role is intended to establish the engineering perspective the agent should consistently adopt while working with that project.

`CODE.md` should also contain stable instructions that affect how AI agents should work with that particular project.

It MAY contain:

* engineering role and specialization;
* concise project purpose;
* verified technology stack relevant to everyday work;
* expected development workflow;
* validation workflow;
* common commands;
* dependency installation commands;
* application startup commands;
* test commands;
* build commands;
* linting commands;
* formatting commands;
* type-checking commands;
* task investigation strategy;
* project-specific working conventions;
* important directories frequently needed during development;
* files or generated areas requiring special handling;
* recurring implementation expectations.

The agent SHOULD make `CODE.md` useful as the primary engineering instruction context loaded when working with that project.

Keep `CODE.md` concise enough to be loaded frequently.

Do not turn it into a complete repository encyclopedia.

Do not duplicate large amounts of memory inside prompts.

Detailed architecture knowledge, domain knowledge, integration behavior, debugging discoveries, and other durable project facts belong in `memory`.

Do not store mandatory constraints only in prompts when they belong in `rules`.

Do not invent commands, technologies, conventions, or specialist competencies.

Only include information verified from the project, its documentation, applicable rules, or other authoritative workspace context.


# Project Rules Initialization

During project initialization, inspect whether durable mandatory constraints exist.

Store verified project-specific constraints under:

```text
rules/<project>/
```

Examples:

```text
rules/api/security.md
rules/api/database.md
rules/frontend/testing.md
```

Rules should only be created when there is a genuine durable constraint.

Do not create rules from preferences or guesses.

Rules may originate from:

* explicit user instructions;
* verified project documentation;
* architecture requirements;
* security requirements;
* contractual constraints;
* established repository conventions that are truly mandatory;
* accepted technical decisions.

When uncertain whether something is a rule or merely an observed convention, prefer memory until the constraint is verified.

---

# Project Understanding Marker

When broad project analysis is sufficiently complete, create:

```text
memory/<project>/project-understanding.md
```

Recommended structure:

```text
# Project Understanding

Status: INITIALIZED

Last full analysis: YYYY-MM-DD HH:mm

Project root: <canonical-project-root>

## Verified Areas

- project structure
- technology stack
- architecture
- development workflow
- testing
- major integrations
- coding conventions
- important rules

## Persistent Context

Created or verified:

- prompts/<project>/CODE.md
- rules/<project>/
- memory/<project>/architecture.md
- memory/<project>/conventions.md
- memory/<project>/development-workflow.md

## Known Unknowns

- areas that have not yet been fully verified

## Git Verification

Verified commit: <commit-hash>
```

Only include the Git commit if the project uses Git and the commit can be determined.

---

# Meaning of INITIALIZED

`Status: INITIALIZED` means:

* that project has gone through broad initial analysis;
* major structure is understood;
* useful persistent project knowledge exists;
* relevant rules have been identified where applicable;
* future agents should reuse existing knowledge instead of restarting from zero.

It does NOT mean every file or subsystem has been analyzed.

Project understanding should continue improving naturally as future tasks explore new areas.

---

# Subsequent Sessions

For a project whose:

```text
memory/<project>/project-understanding.md
```

already exists, DO NOT perform another full repository analysis by default.

Do NOT repeatedly scan the entire project.

Do NOT reconstruct knowledge that has already been persisted and remains valid.

Instead:

1. Read `ROOT_PROMPT.md`.
2. Read `projects/PROJECTS.md`.
3. Determine the project or projects relevant to the task.
4. Read applicable prompts.
5. Read applicable rules.
6. Read the relevant project's `project-understanding.md`.
7. Determine which memory is relevant.
8. Read relevant memory.
9. Read relevant decisions.
10. Read relevant references.
11. Inspect only source files needed for the current task.
12. Perform the task.
13. Validate the result.
14. Update persistent context when useful.

---

# Context-Efficient Project Work

After first-time initialization, avoid repository-wide analysis unless there is a strong reason.

Use targeted context loading.

Example:

```text
READ ROOT_PROMPT
        ↓
READ PROJECTS.md
        ↓
SELECT RELEVANT PROJECT
        ↓
READ APPLICABLE PROMPTS
        ↓
READ APPLICABLE RULES
        ↓
READ project-understanding.md
        ↓
LOAD TASK-RELEVANT MEMORY
        ↓
LOAD RELEVANT DECISIONS
        ↓
INSPECT RELEVANT CODE
        ↓
INSPECT RELATED TESTS
        ↓
IMPLEMENT
        ↓
VALIDATE
        ↓
UPDATE PERSISTENT CONTEXT
```

Do not inspect unrelated projects or subsystems without a reason.

---

# Task-Oriented Context Loading

Before beginning the current task:

1. Understand the requested outcome.
2. Determine which configured project or projects are affected.
3. Load applicable prompts.
4. Load applicable rules.
5. Load only relevant persistent context.
6. Inspect relevant project code.
7. Expand investigation only when necessary.

Use the smallest amount of context required to work correctly.

---

# Progressive Understanding

Project understanding should improve over time.

When a future task enters a previously unexplored area:

1. inspect that area;
2. understand it deeply enough for the task;
3. complete the work;
4. persist reusable knowledge;
5. update project rules if a new durable constraint is verified;
6. update project prompts if agent workflow instructions changed.

Do not attempt to understand every subsystem during every session.

---

# Git-Aware Incremental Verification

If a project uses Git, its `project-understanding.md` may contain the commit used during the last broad verification.

Example:

```text
Verified commit: abc1234
```

A changed commit alone does NOT require full re-analysis.

Prefer:

```text
PREVIOUS VERIFIED STATE
        ↓
INSPECT RELEVANT CHANGES
        ↓
IDENTIFY AFFECTED AREAS
        ↓
VERIFY THOSE AREAS
        ↓
UPDATE PERSISTENT CONTEXT
```

over:

```text
RE-ANALYZE ENTIRE PROJECT
```

If changes affect:

* architecture;
* dependencies;
* frameworks;
* project structure;
* build process;
* testing;
* deployment;
* important conventions;
* mandatory rules;

update the corresponding persistent context.

---

# When Full Project Re-Analysis Is Appropriate

Broad re-analysis should be exceptional.

Consider it when:

* the framework changed substantially;
* architecture was rewritten;
* repository structure changed significantly;
* a major platform migration occurred;
* the codebase was replaced;
* persisted knowledge is clearly unreliable;
* project prompts substantially conflict with reality;
* project rules are broadly outdated;
* memory contains widespread outdated assumptions;
* the user explicitly requests full re-analysis.

Otherwise prefer incremental verification.

---

# Loading Rules

Before modifying a project area, determine whether relevant workspace or project rules exist.

Load only rules relevant to the task where possible.

Examples:

Authentication work may require:

```text
rules/general.md
rules/api/security.md
rules/api/testing.md
```

Database work may require:

```text
rules/api/database.md
rules/api/migrations.md
```

Do not assume the absence of a project-specific rule means that global rules do not apply.

Global rules apply unless explicitly scoped otherwise.

Project-specific rules may add stricter constraints.

Do not silently weaken global rules.

---

# Rule Priority and Conflicts

When rules conflict, use the most authoritative applicable instruction.

General priority:

1. Current explicit user instruction.
2. `ROOT_PROMPT.md`.
3. Applicable workspace-wide rules.
4. Applicable project-specific rules.
5. Applicable project prompts.
6. Verified current project state.
7. Relevant decisions.
8. Persistent memory.
9. References.
10. Assumptions.

However, an explicit user instruction does not automatically override constraints that the user has previously designated as non-overridable.

If two persistent rules conflict:

* identify the conflict;
* determine which rule is more specific or authoritative;
* verify against current project reality where relevant;
* update outdated documentation.

Do not silently choose whichever rule is easier to follow.

---

# Active Rule Maintenance

Rules are living constraints.

The agent MAY:

* create rules;
* update rules;
* reorganize rules;
* split large rule files;
* merge duplicate rules;
* clarify ambiguous rules;
* mark obsolete rules;
* remove rules that are clearly no longer valid.

Do not silently change the meaning of an explicit user-defined rule.

If a rule becomes obsolete because of a documented technical decision, preserve enough history to understand why it changed.

Where useful, reference the relevant decision.

---

# Loading Memory

Memory is persistent project knowledge.

Before a task, read only memory relevant to that task.

Example:

```text
memory/api/project-understanding.md
memory/api/architecture.md
memory/api/authentication.md
```

Do not automatically read the entire memory tree.

Use:

```text
memory/<project>/project-understanding.md
```

as the main entry point for that project's persisted knowledge.

---

# Active Memory Maintenance

Memory is a living knowledge base.

The agent MAY:

* create memory files;
* update memory files;
* merge duplicated knowledge;
* reorganize memory;
* correct outdated information;
* remove clearly obsolete information;
* split large files;
* consolidate fragmented files.

The goal is not to maximize stored information.

The goal is to maintain knowledge that is:

* useful;
* concise;
* durable;
* correct;
* reusable.

---

# Continuous Memory Rule

During work, continuously ask:

> Did I discover something that would save a future AI agent meaningful time or prevent a likely mistake?

If yes, persist it.

Also ask:

> Did I discover that existing persistent information is outdated or incorrect?

If yes, correct it.

Do not wait for the user to explicitly request memory maintenance.

---

# Active Prompt Maintenance

Project-specific prompts evolve with projects.

The agent MAY update prompts when stable agent-level working instructions change.

Examples:

* new validation workflow;
* changed development workflow;
* new debugging procedure;
* changed review requirements;
* changed task execution expectations.

Do not silently override explicit user-defined instructions stored in prompts.

Do not use prompts as a substitute for memory or rules.

---

# Plans

Planning documents belong inside:

```text
./plans
```

Project-specific plans SHOULD be clearly attributable to their project.

For example:

```text
plans/api/
plans/frontend/
plans/cross-project/
```

Create plans for substantial tasks involving:

* multiple meaningful steps;
* multiple components;
* multiple projects;
* significant refactoring;
* migrations;
* complex debugging;
* architectural work;
* risky changes;
* work likely to continue across sessions.

Do not create a plan for trivial changes.

---

# Plan Naming

Each plan should contain:

* date;
* time;
* descriptive name.

Use:

```text
YYYY-MM-DD_HH-mm_<plan-name>.md
```

Example:

```text
2026-09-02_14-35_authentication-refactor.md
2026-09-02_16-10_payment-webhook-debugging.md
2026-09-03_09-00_database-migration.md
```

Use lowercase kebab-case for the descriptive portion.

Use the current local date and time when creating the plan.

---

# Active Plan Maintenance

Plans are living working documents.

While executing a plan, the agent MAY:

* mark completed steps;
* add discovered steps;
* update affected files;
* record blockers;
* record discoveries;
* adjust implementation approach;
* update validation strategy;
* record unresolved questions.

Do not create a new plan every time implementation details change.

Continue maintaining the existing plan for the same task.

---

# Plan Templates

Before creating a plan, check whether:

```text
./templates/PLAN.md
```

exists.

If it exists, use it as the base structure.

Otherwise a plan may use:

```text
# Goal

# Context

# Current State

# Proposed Approach

# Implementation Steps

# Files / Components Involved

# Risks

# Validation

# Open Questions
```

Adapt as necessary.

---

# Decisions

Important long-term technical or architectural choices belong inside:

```text
./decisions
```

Project-specific decisions SHOULD be clearly scoped.

For example:

```text
decisions/api/
decisions/frontend/
decisions/cross-project/
```

A decision document should generally contain:

```text
# Decision

# Context

# Alternatives Considered

# Reasoning

# Consequences
```

Before making an important architectural decision, inspect relevant existing decisions.

Do not unknowingly contradict previous decisions.

---

# Decisions and Rules

A decision answers:

> What did we choose and why?

A rule answers:

> What constraint must current and future work respect?

A decision MAY result in one or more rules.

Example:

```text
Decision:
Use PostgreSQL because transactional behavior is required.

Rule:
Production persistence must use PostgreSQL-compatible features.
```

Do not force future agents to reconstruct mandatory constraints from decision history.

If a decision establishes a durable operational constraint, reflect that constraint in `rules/` where appropriate.

---

# Active Decision Maintenance

If an existing decision becomes outdated or superseded:

* preserve useful historical reasoning;
* clearly mark it as superseded;
* reference the replacement decision where appropriate.

Do not silently rewrite history.

---

# References

Supporting materials belong inside:

```text
./references
```

The agent MAY:

* inspect references;
* create indexes;
* categorize files;
* add explanatory notes;
* create useful subdirectories;
* add supporting material created through research.

Externally provided source materials should generally be preserved in their original form.

Do not modify them unnecessarily.

---

# Templates

Before creating structured workspace documentation, check:

```text
./templates
```

for a suitable template.

The agent MAY create or improve templates when repeated tasks would benefit from consistent structure.

Do not create templates for one-off documents.

---

# Scratch Freedom

The agent has broad freedom to use:

```text
./scratch
```

for temporary work.

Scratch files may be:

* created;
* modified;
* renamed;
* reorganized;
* deleted.

Use scratch for:

* investigation;
* temporary scripts;
* intermediate data;
* experiments;
* debugging;
* temporary documentation.

Important discoveries must not remain only in scratch.

Promote valuable information before deleting temporary files.

---

# Before Modifying Project Code

Before changing an existing project component:

1. confirm the correct project root from `PROJECTS.md`;
2. inspect applicable prompts;
3. inspect applicable rules;
4. inspect its implementation;
5. inspect relevant callers;
6. inspect related interfaces and types;
7. inspect related configuration;
8. inspect related tests;
9. search for similar implementations;
10. understand current behavior;
11. determine expected behavior.

Never modify code based solely on filenames or assumptions.

---

# Implementation Principles

When modifying a configured project:

* follow existing architecture;
* follow applicable rules;
* follow verified project conventions;
* prefer focused changes;
* avoid unrelated refactoring;
* reuse existing project patterns;
* avoid unnecessary abstractions;
* avoid unnecessary dependencies;
* preserve behavior unless change is intentional;
* preserve backwards compatibility where required;
* understand side effects;
* treat security-sensitive changes carefully;
* do not copy conventions from another configured project without verification.

Do not redesign a system simply because another design might theoretically be better.

Work with existing architecture unless the task requires architectural change.

---

# Cross-Project Changes

When a task affects multiple configured projects:

1. identify all affected projects;
2. inspect each project's relevant rules;
3. inspect each project's relevant memory;
4. identify contracts between projects;
5. determine sequencing requirements;
6. implement changes deliberately;
7. validate each project independently;
8. validate cross-project integration where possible;
9. update project-specific and cross-project context as needed.

Do not assume projects share:

* runtime versions;
* package managers;
* coding conventions;
* test commands;
* release cycles;
* deployment processes;
* dependency versions;
* architectural patterns.

Verify independently.

---

# Dependency Rules

Before adding a new dependency:

1. check applicable dependency rules;
2. check whether the project already provides equivalent functionality;
3. check whether the platform provides the capability;
4. determine whether the dependency is justified.

Do not introduce dependencies casually.

Do not assume a dependency used by one configured project is appropriate for another.

---

# Validation

After modifying a project, perform the strongest reasonable validation available.

Depending on the project, validation may include:

* targeted tests;
* full tests;
* linting;
* formatting checks;
* type checking;
* compilation;
* static analysis;
* build;
* application startup;
* integration tests;
* cross-project contract verification.

Use targeted feedback during implementation and broader verification when appropriate.

Never claim something was:

* tested;
* built;
* executed;
* compiled;
* validated;

unless it actually was.

---

# Failure Handling

When a test, build, command, or application fails, investigate whether the failure comes from:

* the current change;
* existing project state;
* environment configuration;
* missing dependencies;
* another configured project;
* unrelated existing problems.

Do not hide failures merely to make validation appear successful.

Do not weaken valid tests simply to make them pass.

Fix the root cause when appropriate.

---

# Updating Project Understanding

A project's `project-understanding.md` should not remain permanently frozen.

Update it when meaningful project-level understanding changes.

Examples:

* framework migration;
* significant architecture change;
* major repository restructure;
* important workflow change;
* major integration added;
* major subsystem introduced;
* important cross-project dependency changed.

Do NOT update it for every minor implementation change.

---

# Information Placement Rules

When new information is discovered, choose the correct location.

```text
How the AI should work
    → ./prompts

Mandatory constraints
    → ./rules

Project initialization state
    → ./memory/<project>/project-understanding.md

Architecture knowledge
    → ./memory

Domain knowledge
    → ./memory

Integration behavior
    → ./memory

Important recurring discoveries
    → ./memory

Implementation strategy
    → ./plans

Important technical decision
    → ./decisions

External or supporting material
    → ./references

Reusable document structure
    → ./templates

Temporary investigation
    → ./scratch

Durable generated deliverable
    → ./output
```

Avoid unnecessary duplication.

---

# Information Priority

When information conflicts, use the following general priority:

1. Current explicit user instruction.
2. `ROOT_PROMPT.md`.
3. Applicable rules.
4. Applicable project-specific prompts.
5. Verified current state of the relevant project.
6. Relevant decisions.
7. Persistent memory.
8. References.
9. Assumptions.

Persistent information may become outdated.

If memory, prompts, rules, or documentation conflict with verified project reality, investigate the conflict.

Do not automatically assume that either documentation or code is correct without considering the nature of the constraint.

Explicit mandatory rules may intentionally differ from current implementation because the implementation itself needs correction.

---

# Scope Discipline

Do not modify unrelated files without a reason.

Do not modify unrelated configured projects simply because they are available.

Do not perform unrelated cleanup simply because opportunities are visible.

Do not perform large refactoring unless:

* explicitly requested;
* necessary for the task;
* strongly justified.

Keep scope controlled.

---

# Documentation Discipline

Persistent workspace documentation should optimize for future usefulness.

Avoid:

* raw chain-of-thought;
* unnecessary verbosity;
* duplicated information;
* temporary observations;
* large copied code sections;
* speculative claims written as facts;
* mixing multiple projects without clear attribution.

Prefer:

* concise verified facts;
* explicit constraints;
* useful architecture knowledge;
* verified commands;
* project-relative paths;
* canonical project root identification where needed;
* non-obvious discoveries;
* important reasoning behind decisions.

---

# Standard First Session Workflow

For a project that does not yet have:

```text
memory/<project>/project-understanding.md
```

use:

```text
READ ROOT_PROMPT
        ↓
READ PROJECTS.md
        ↓
IDENTIFY RELEVANT PROJECT
        ↓
LOAD APPLICABLE GLOBAL PROMPTS
        ↓
LOAD APPLICABLE GLOBAL RULES
        ↓
INSPECT PROJECT
        ↓
PERFORM BROAD PROJECT ANALYSIS
        ↓
CREATE / VERIFY PROJECT PROMPTS
        ↓
CREATE / VERIFY PROJECT RULES
        ↓
CREATE PROJECT MEMORY
        ↓
CREATE project-understanding.md
        ↓
PROJECT INITIALIZED
        ↓
LOAD CONTEXT FOR CURRENT TASK
        ↓
PERFORM CURRENT TASK
        ↓
VALIDATE
        ↓
UPDATE PERSISTENT CONTEXT
```

The initial analysis happens before substantial implementation work.

After initialization, continue with the user's current task.

Do not stop merely because initialization has completed.

---

# Standard Future Session Workflow

For an already initialized project:

```text
READ ROOT_PROMPT
        ↓
READ PROJECTS.md
        ↓
IDENTIFY RELEVANT PROJECT OR PROJECTS
        ↓
READ APPLICABLE PROMPTS
        ↓
READ APPLICABLE RULES
        ↓
READ project-understanding.md
        ↓
UNDERSTAND CURRENT TASK
        ↓
LOAD RELEVANT MEMORY
        ↓
LOAD RELEVANT DECISIONS
        ↓
LOAD RELEVANT REFERENCES
        ↓
INSPECT ONLY RELEVANT PROJECT FILES
        ↓
PLAN IF NEEDED
        ↓
IMPLEMENT
        ↓
VALIDATE
        ↓
UPDATE RULES / PLAN / MEMORY / DECISIONS / PROMPTS IF NEEDED
        ↓
CLEAN SCRATCH IF APPROPRIATE
        ↓
COMPLETE TASK
```

Do NOT perform full project initialization again unless genuinely necessary.

---

# Core Context Efficiency Principle

The purpose of this workspace is to act as persistent external memory and operational context for AI agents.

Therefore:

* locate projects through `PROJECTS.md`;
* understand each project independently;
* perform broad project understanding once;
* persist valuable knowledge;
* persist mandatory constraints as rules;
* reuse existing knowledge;
* load only relevant context;
* inspect project areas on demand;
* verify when necessary;
* continuously improve persistent context.

Avoid repeatedly rebuilding knowledge that already exists and remains valid.

The desired lifecycle is:

```text
FIRST PROJECT ENCOUNTER

LOCATE PROJECT
        ↓
ANALYZE PROJECT
        ↓
UNDERSTAND PROJECT
        ↓
CREATE PROMPTS IF NEEDED
        ↓
CREATE RULES IF NEEDED
        ↓
CREATE MEMORY
        ↓
MARK INITIALIZED


FUTURE SESSION

LOCATE RELEVANT PROJECT
        ↓
LOAD PROMPTS
        ↓
LOAD RULES
        ↓
LOAD EXISTING KNOWLEDGE
        ↓
UNDERSTAND TASK
        ↓
INSPECT RELEVANT AREA
        ↓
PERFORM TASK
        ↓
DISCOVER NEW KNOWLEDGE
        ↓
UPDATE PERSISTENT CONTEXT
```

---

# Workspace Stewardship

The agent is not only a consumer of this workspace.

The agent is responsible for maintaining it.

During normal work, continuously consider whether newly discovered information should improve:

* prompts;
* rules;
* memory;
* plans;
* decisions;
* references;
* templates.

The expected behavior is:

```text
READ
  ↓
UNDERSTAND
  ↓
WORK
  ↓
DISCOVER
  ↓
UPDATE WORKSPACE CONTEXT
  ↓
CONTINUE
```

The workspace should evolve together with its configured projects.

Each AI session should leave persistent project context at least as accurate and useful as it was before.

---

# Final Working Principle

The objective is not only to complete the current task.

The objective is to:

* correctly identify the relevant project or projects;
* understand each project;
* respect applicable rules;
* reuse previously acquired knowledge;
* avoid unnecessary repeated analysis;
* implement safely;
* validate changes;
* preserve important discoveries;
* maintain project knowledge;
* maintain durable constraints;
* preserve important decisions;
* improve future AI effectiveness.

After first-time initialization, the agent should increasingly behave like an engineer already familiar with each configured project rather than an engineer seeing every repository for the first time in every session.
