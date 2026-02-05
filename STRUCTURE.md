![Discord Bot Template Banner](assets/branding/structure_banner.png)

# 🧱 Project Structure — Discord Bot Template

Welcome to the **Discord Bot Template** project structure overview.

This document explains **every folder and file** in the repository in a clear,
approachable way — from a beginner’s perspective, but with **production-grade
architecture in mind**.

> 🎯 Goal of this project:
> - Help you understand **how the project is organized**
> - Explain **responsibilities of each module**
> - Make it easy to **navigate, extend, and maintain** the codebase

---

## 📚 Table of Contents

- [1. High-Level Overview](#1-high-level-overview)
- [2. Root Directory](#2-root-directory)
- [2.1 Developer Tooling (`tools/`)](#21-developer-tooling-tools)
- [3. Project Assets](#3-project-assets)
- [4. Application Core Package](#4-application-core-package)
  - [4.1 Core Runtime Files](#41-core-runtime-files)
  - [4.2 Logging Subsystem](#42-logging-subsystem)
  - [4.3 Command Cogs](#43-command-cogs)
  - [4.4 Utility Modules](#44-utility-modules)
- [5. Design Philosophy Recap](#5-design-philosophy-recap)

---

## 1. High-Level Overview

⬆️ [(back to table of contents)](#-table-of-contents)

This project is built around a **layered, responsibility-driven architecture**
designed for long-term maintainability and predictable behavior.

Rather than thinking in terms of files, the system should be understood as
**cooperating architectural layers**, each with a clearly defined role.

---

### 🧱 Architectural Layers (Mental Model)

At a high level, the application consists of the following layers:

1. **Bootstrap & Configuration Layer**
2. **Application Core Layer**
3. **Support & Infrastructure Layer**

Each layer:
- owns a specific responsibility,
- exposes a narrow surface to higher layers,
- avoids bidirectional dependencies.

---

### ▶️ Execution Flow (From Startup to Command)

```text
main.py
  ↓
bot/client.py
  ↓
Command Cogs (features)
  ↓
Shared Utilities
  ↓
Logging & Error Infrastructure
```

How to read this flow:

- `main.py is` responsible only for **starting the system safely**
- `client.py` orchestrates Discord-specific lifecycle behavior
- Cogs implement **feature-level logic**
- Utilities provide **shared, reusable helpers**
- Logging & error handling act as **system-wide safety nets**

No layer skips another. No layer silently overrides responsibility.

---

### 🔗 Dependency Direction (Important)

Dependencies in this project are **one-directional by design:**

```text
Higher-level logic
        ↓
Lower-level infrastructure
```

This means:

- features depend on utilities,
- utilities may depend on logging,
- logging **never** depends on features.

This rule prevents:

- circular dependencies,
- hidden side effects,
- architectural erosion over time.

If a dependency feels questionable — it usually means the logic belongs lower in the stack.

---

### 🧠 Design Intent

This structure is intentionally designed to support:

- incremental feature growth,
- safe refactoring,
- clear ownership of responsibilities,
- predictable execution paths,
- professional error observability.

It is suitable for:

- small utility bots,
- complex production systems,
- commercial or portfolio-grade projects.

Nothing happens implicitly. Everything can be traced, explained, and reasoned about.

⬆️ [(read again)](#1-high-level-overview)

---

## 2. Root Directory

⬆️ [(back to table of contents)](#-table-of-contents)

The root directory contains **project-level control files**.

These files are responsible for:
- application startup,
- environment configuration,
- dependency definition,
- developer-facing documentation,
- maintainers tooling (snapshot generation).

They do **not** contain application logic.

---

### `main.py`
➡️ **Application entry point**

This file is the **only executable entry point** of the application.

Responsibilities:
- validate environment configuration **before runtime**
- configure global logging infrastructure
- initialize the Discord client
- start the Discord connection
- handle fatal startup-level errors

Architectural rules:
- ❌ no business logic
- ❌ no feature implementation
- ❌ no Discord-specific behavior beyond startup
- ✅ fail fast on misconfiguration
- ✅ explicit and predictable execution order

If the application fails here, it fails **early and intentionally**.

---

### `.env`
➡️ **Runtime environment configuration**

Contains **environment-specific values** required at runtime, such as:
- Discord bot token
- application environment (`dev` / `prod`)
- optional system-level channel IDs
- developer access configuration

Key rules:
- 🔐 must never be committed to a public repository
- 🔁 values may differ between environments
- 📌 consumed exclusively by `bot/settings.py`

This file defines **what the system runs with**, not **how it runs**.

---

### `.env.example`
➡️ **Environment configuration template**

Provides a **documented example** of all environment variables
required by the application.

Purpose:
- serve as a safe, versioned reference,
- document required and optional configuration keys,
- act as a starting point for creating a local `.env` file.

Key rules:
- ✅ must be committed to the repository
- ❌ must never contain real secrets
- 🔁 copied by users to create their local `.env`

This file defines **what must be configured** —
not the actual runtime values.

---

### `.gitignore`
➡️ **Version control safety**

Defines which files and directories are excluded from version control.

Purpose:
- prevent committing secrets
- exclude virtual environments and caches
- keep the repository clean and portable

This file protects the project from **accidental leakage and noise**.

---

### `requirements.txt`
➡️ **Dependency declaration**

Lists all Python packages required to run the application.

Responsibilities:
- define runtime dependencies
- ensure reproducible environments
- serve as the single dependency source for the project

This file contains **no version logic or environment behavior** —
only dependency declarations.

---

### `README.md`
➡️ **Project entry point**

The primary, user-facing introduction to the project.

Responsibilities:
- explain what this template is
- communicate architectural intent at a high level
- provide quick setup instructions
- showcase selected code excerpts

This file acts as a **movie trailer**:
informative, focused, and intentionally non-exhaustive.

---

### `STRUCTURE.md`
➡️ **Architectural map**

Explains how the project is structured and how responsibilities
are distributed across directories and modules.

This document answers:
- *Where does this belong?*
- *What is the role of this module?*
- *How does the system fit together?*

It does **not** explain how to extend the system.

---

### `GUIDE.md`
➡️ **Development & extension guide**

Provides step-by-step guidance for extending the template.

Responsibilities:
- show how to add new features
- demonstrate architectural extension patterns
- document supported customization paths

This is the **hands-on manual** for growing the project
without breaking its foundations.

---

### `SECURITY.md`
➡️ **Security policy & responsible disclosure**

Defines how security vulnerabilities should be reported,
evaluated, and disclosed for this repository.

Responsibilities:
- document supported security scope,
- define responsible disclosure process,
- set expectations for response and communication.

This file establishes security as a **first-class design concern**,
even though this project is a template and not a hosted service.

---

### `LICENSE`

➡️ **Project license and legal usage terms**

Defines the legal terms under which this template can be used,
modified, and redistributed.

Key characteristics:
- uses the **MIT License**
- allows commercial and non-commercial use
- requires preservation of copyright notice
- provides no warranty or liability

This file establishes clear authorship and usage rights
for anyone consuming or extending the template.

It is a **mandatory component** of any professional open-source project.

⬆️ [(read again)](#2-root-directory)

---

## 2.1 Developer Tooling (`tools/`)

⬆️ [(back to table of contents)](#-table-of-contents)

The `tools/` directory contains **maintainer-oriented utilities** that support
repository operations but are not part of runtime bot execution.

These tools are intentionally separated from application logic (`bot/`) to keep
the runtime architecture clean and predictable.

### 📁 `tools/snapshot/`
➡️ **Project snapshot utility domain**

Contains the snapshot generator and its local output location:

```text
tools/
└── snapshot/
    ├── generate.py
    └── docs/
        └── PROJECT_SNAP.md   # generated locally (gitignored)
```

Responsibilities of `tools/snapshot/generate.py`:
- build a one-file markdown snapshot of the repository,
- include full file contents for allowed files,
- exclude sensitive/local artifacts (e.g. `.env` secrets, caches, virtualenvs).

Important notes:
- `PROJECT_SNAP.md` is **not** versioned as source code,
- this utility is for developers/maintainers, not runtime bot users.

⬆️ [(read again)](#21-developer-tooling-tools)

---


## 3. Project Assets

⬆️ [(back to table of contents)](#-table-of-contents)

The `assets/` directory contains **non-runtime resources** used exclusively for
documentation, presentation, and long-term project maintenance.

These files are:
- never imported by the application,
- never loaded at runtime,
- never coupled to business or feature logic.

This strict separation keeps the runtime architecture clean and predictable.

---

### 📁 `assets/branding/`
➡️ **Visual identity & presentation assets**

Contains visual elements related to the project’s identity and documentation.

These assets are used to provide:
- visual context,
- consistent presentation,
- strong first impressions.

They do **not** affect runtime behavior
and are never referenced by application code.

---

#### Typical contents

- documentation banners
- logos or branding elements
- visuals used for portfolios or landing pages

#### Current usage

- referenced by `README.md` as the main project introduction
- referenced by `STRUCTURE.md` to visually separate architectural documentation
- referenced by `GUIDE.md` to introduce the development playbook

#### Examples

- `readme_banner.png` — banner displayed at the top of `README.md`
- `structure_banner.png` — banner displayed at the top of `STRUCTURE.md`
- `guide_banner.png` — banner displayed at the top of `GUIDE.md`
- `security_banner.png` — banner displayed at the top of `SECURITY.md`

These assets exist to improve **clarity, orientation, and presentation** —
not to influence application behavior.



---

### 📁 `assets/docs/`
➡️ **Documentation support assets**

Contains assets used by technical documentation.

Intended for:
- architecture diagrams
- screenshots used in guides
- visuals referenced in `GUIDE.md`
- future explanatory materials

Keeping documentation assets here allows:
- documentation to scale independently,
- clean separation from code,
- easier long-term maintenance.

---

### ⚠️ What Does *NOT* Belong in `assets/`

The `assets/` directory must NOT contain:
- Python files
- configuration files
- environment-specific data
- anything required for application execution

If a file is required for the bot to run,
it does **not** belong in `assets/`.

⬆️ [(read again)](#3-project-assets)

---

## 4. Application Core Package

⬆️ [(back to table of contents)](#-table-of-contents)

The `bot/` package contains **all runtime application logic**.

It is the heart of the system and defines how the Discord bot:
- initializes,
- executes features,
- handles errors,
- and enforces architectural boundaries.

Nothing outside this package influences runtime behavior.

---

### 📦 What Belongs in `bot/`

The `bot/` package is responsible for:
- Discord client orchestration
- runtime configuration handling
- command and interaction execution
- centralized error handling
- logging and observability
- shared, reusable helpers

Every piece of logic that affects **how the bot behaves at runtime**
lives somewhere inside this package.

---

### 🚫 What Does *NOT* Belong in `bot/`

The following must NOT be placed inside `bot/`:
- documentation files
- images or assets
- environment secrets (`.env`)
- dependency declarations
- build or deployment scripts

If a file is not required to **run the application**,
it does not belong in this package.

---

### 🧱 Internal Structure Overview

The `bot/` package is intentionally divided into **clear subpackages**:

```text
bot/
├── client.py           # Discord lifecycle orchestration
├── config.py           # Discord-level configuration
├── logging_config.py   # Logging system configuration
├── settings.py         # Runtime environment configuration
│
├── logging/            # Observability & diagnostics
├── cogs/               # Feature-level command logic
└── utils/              # Shared helpers & infrastructure glue
```

Each subpackage has a **single, well-defined responsibility.**
No subpackage is allowed to grow into a “miscellaneous” dumping ground.

---

### 🔗 Dependency Direction (Enforced by Convention)

Dependencies inside `bot/` are **one-directional:**

```text
client.py
  ↓
cogs/
  ↓
utils/
  ↓
logging/
```

Rules:

- higher-level layers may depend on lower-level layers
- lower-level layers must never depend on higher-level ones
- no circular dependencies are allowed

This structure ensures:

- predictable execution paths,
- safe refactoring,
- long-term architectural stability.

If a dependency feels wrong —
it usually means the logic belongs **in a different layer.**

⬆️ [(read again)](#4-application-core-package)

---

## 4.1 Core Runtime Files

⬆️ [(back to table of contents)](#-table-of-contents)

This section describes the **core runtime files** responsible for
initializing, configuring, and orchestrating the application.

These files define **how the system starts and behaves** —
not what features it provides.

---

### `bot/client.py`
➡️ **Discord client orchestration**

This module implements the **central Discord client**.

Responsibilities:
- manage the Discord connection lifecycle
- register and load command cogs
- synchronize application (slash) commands
- attach global error handlers
- provide a predictable startup sequence

Key architectural rules:
- ❌ no business logic
- ❌ no feature-specific behavior
- ❌ no per-guild state management
- ✅ orchestration only

This file acts as the **control center** of the application,
coordinating how all parts are wired together.

---

### `bot/config.py`
➡️ **Discord-level configuration**

Defines **Discord-specific constants and settings** used by the application.

Responsibilities:
- configure gateway intents
- define Discord platform limits
- centralize protocol-level constants

Important rules:
- ❌ no environment variable access
- ❌ no runtime logic
- ❌ no application behavior

This module isolates Discord API configuration
from the rest of the system.

---

### `bot/settings.py`
➡️ **Runtime environment configuration**

Acts as the **single source of truth** for runtime configuration.

Responsibilities:
- load environment variables
- expose environment flags (`IS_DEV`, `IS_PROD`)
- provide infrastructure-level settings
- validate critical configuration at startup

Key guarantees:
- configuration is validated **before runtime**
- misconfiguration fails fast and loudly
- no Discord API access

This module defines **what the system runs with** —
not how it behaves.

---

### `bot/logging_config.py`
➡️ **Logging system configuration**

Configures Python’s logging infrastructure.

Responsibilities:
- define global log levels
- configure handlers and formatters
- control verbosity based on environment

Important distinction:
> `logging_config.py` **configures** logging  
> `logger.py` **uses** logging

This separation ensures that logging behavior
can be extended or replaced without touching
application or feature logic.

⬆️ [(read again)](#41-core-runtime-files)

---

## 4.2 Logging Subsystem

⬆️ [(back to table of contents)](#-table-of-contents)

The logging subsystem is responsible for **observability, diagnostics,
and structured error tracking** across the entire application.

Its primary goal is to answer one question reliably:

> *What happened, where did it happen, and why?*

This subsystem is **infrastructure-level** and must remain
independent from business logic and feature implementation.

---

### 🧩 Subsystem Overview

```text
bot/logging/
├── error_context.py   # Structured error data model
├── logger.py          # Backend logging implementation
└── reporter.py        # Optional Discord-facing reporting
```

Each module has a **single, non-overlapping responsibility.**
Together, they form a complete error and observability pipeline.

---

### `error_context.py`

➡️ **Structured error data model**

Defines the **immutable data structures** used to represent runtime errors.

Responsibilities:

- classify error severity
- define error source categories
- provide a structured error context object

Key design principles:

- pure data only (no logic, no side effects)
- immutable by design
- acts as a contract between system layers

This file defines **what an error is** —
not how it is handled or displayed.

---

### `logger.py`

➡️ **Backend / infrastructure logging**

Implements the **central logging backend** of the application.

Responsibilities:

- log structured error data
- control verbosity based on environment
- route logs according to severity
- expose a single logging entry point

Important rules:

- ❌ no Discord API usage
- ❌ no user-facing behavior
- ❌ no business decisions

This module answers:

> *How is this error recorded for diagnostics?*

---

### `reporter.py`

➡️ **Discord-facing system reporting (optional)**

Handles **operational reporting** of critical system errors
to a designated Discord channel.

Responsibilities:

- send ERROR and CRITICAL events to Discord
- format diagnostic-friendly embeds
- avoid exposing sensitive data (e.g. tracebacks)

Key characteristics:

- optional and safe to disable
- silent on failure
- intended for operators, not end users

This module answers:

> *Who needs to be notified when something goes seriously wrong?*

---

### 🔗 Error Flow (Conceptual)

```text
Exception
  ↓
ErrorContext (structured data)
  ↓
SystemLogger (backend logging)
  ↓
ErrorReporter (optional notification)
```

Every error:

- is captured explicitly,
- is classified,
- is logged in a structured way,
- may be reported without affecting runtime stability.

No error is swallowed.
No failure is silent.

⬆️ [(read again)](#42-logging-subsystem)

---

## 4.3 Command Cogs

⬆️ [(back to table of contents)](#-table-of-contents)

Command Cogs define the **feature-level behavior** of the Discord bot.

They are responsible for:
- handling user interactions,
- implementing commands and actions,
- orchestrating feature-specific logic.

Each Cog represents a **clear functional boundary** within the system.

---

### 🧩 Cog Structure Overview

```text
bot/cogs/
├── core.py   # Public, always-available commands
└── dev.py    # Development-only utilities
```

Cogs are loaded explicitly by the Discord client
during the application startup sequence.

---

### `core.py`

➡️ **Public, safe commands**

Contains commands that:

- are available to all users,
- have no side effects,
- do not require special permissions,
- serve as reference implementations.

Primary purposes:

- provide minimal, always-available functionality,
- demonstrate correct command structure,
- act as a safe learning surface for new users.

This file should remain:

- simple,
- predictable,
- free of complex business rules.

---

### `dev.py`

➡️ **Developer-only commands**

Contains commands intended strictly for development
and testing environments.

Responsibilities:

- provide diagnostic utilities,
- simulate controlled failure scenarios,
- validate developer access control,
- test the global error handling pipeline.

Key guarantees:

- automatically disabled in production mode,
- protected by environment-based authorization,
- never exposed to regular users.

This file exists to make development safer —
not faster at the cost of security.

---

### ⚠️ What Does *NOT* Belong in Cogs

Cogs must NOT contain:

- shared helper logic (belongs in `utils/`)
- infrastructure or logging configuration
- long-running application state
- cross-feature coordination logic

If logic is reused across multiple Cogs,
it likely belongs in a **lower-level module.**

---

### 🧠 Design Intent

Cogs are intentionally kept:

- thin,
- explicit,
- focused on interaction handling.

They should delegate:

- error handling → centralized pipeline,
- shared logic → utilities,
- diagnostics → logging subsystem.

This keeps feature growth predictable
and prevents architectural coupling.

⬆️ [(read again)](#43-command-cogs)

---

## 4.4 Utility Modules

⬆️ [(back to table of contents)](#-table-of-contents)

The `utils/` package contains **shared helper modules** used across
multiple parts of the application.

These modules provide:
- reusable logic,
- safety guards,
- infrastructure glue,
- consistent UX helpers.

They do **not** implement features or business rules.

---

### 🧩 Utility Structure Overview

```text
bot/utils/
├── error_handler.py         # Centralized interaction error handling
├── global_error_handler.py  # Discord command error interception
├── helpers.py               # Generic guards and helpers
└── theme.py                 # UI & visual consistency
```

Each module has a **narrow, explicit responsibility.**
Utilities must remain small and predictable.

---

### `error_handler.py`
➡️ **Centralized interaction error handling**

Acts as the **single authoritative entry point**
for handling all interaction-related exceptions.

Responsibilities:
- classify error severity
- build structured error context
- delegate logging and reporting
- provide consistent user-facing feedback

Key guarantees:
- no silent failures
- no duplicated try/except logic
- consistent UX across all commands

This module defines **how errors are processed** —
not where they originate.

---

### `global_error_handler.py`
➡️ **Global command error interception**

Hooks into Discord’s application command error system
and forwards all errors to the centralized error handler.

Responsibilities:
- intercept all AppCommandError exceptions
- unwrap original exceptions when needed
- guarantee a single error handling path

This module acts as a **safety net**:
no command error is ever left unhandled.

---

### `helpers.py`
➡️ **Generic guards & helper functions**

Provides small, reusable helper functions such as:
- interaction context checks
- permission guards
- environment checks
- safe interaction response utilities

Design rules:
- stateless
- side-effect free
- easily reusable
- simple by design

If a helper becomes complex,
it likely belongs in a dedicated service instead.

---

### `theme.py`
➡️ **UI & visual consistency**

Defines all visual constants used across the bot.

Responsibilities:
- centralize embed colors
- provide semantic color aliases
- optionally expose embed builder helpers

Key rules:
- no hardcoded colors in commands
- all visual styling flows from this module

This ensures consistent UX
and makes future theming or rebranding trivial.

---

### ⚠️ What Does *NOT* Belong in `utils/`

The `utils/` package must NOT contain:
- feature-specific logic
- application workflows
- long-running state
- database access
- business decisions

Utilities should support the system —
never define its behavior.

⬆️ [(read again)](#44-utility-modules)

---

## 5. Design Philosophy Recap

⬆️ [(back to table of contents)](#-table-of-contents)

This project structure is the result of **intentional architectural decisions**,
not incremental growth or convenience-based organization.

Every directory and module exists to enforce:
- clear responsibility boundaries,
- predictable execution paths,
- explicit configuration and behavior,
- safe long-term evolution of the codebase.

---

### 🧠 Structure Over Convenience

This template prioritizes **structural clarity** over short-term convenience.

Logic is placed where it *belongs*, not where it is easiest to add.
As a result:
- features remain isolated,
- infrastructure stays reusable,
- refactoring does not cascade unexpectedly.

---

### 🔍 Explicit Over Implicit

Nothing in this project relies on hidden behavior or magic defaults.

- configuration is validated explicitly,
- errors are handled centrally,
- dependencies flow in one direction.

If something happens at runtime, it can be:
- traced,
- explained,
- and debugged without guesswork.

---

### 🛡️ Failure Is a First-Class Concept

Errors are not treated as edge cases.

They are:
- classified,
- structured,
- logged,
- and optionally reported.

This ensures that failures are **visible, actionable, and auditable**
instead of silent or ignored.

---

### 🚀 Designed for Growth

This structure is designed to grow without collapsing under its own weight.

New features can be added by:
- introducing new Cogs,
- extending utilities responsibly,
- enhancing infrastructure without touching feature code.

The foundation does not need to be rewritten
as the project becomes more complex.

---

### 🧩 A Shared Mental Model

Most importantly, this structure provides a **shared mental model**
for everyone working on the project.

When structure is predictable:
- onboarding becomes easier,
- collaboration becomes safer,
- architectural decisions become clearer.

This document exists to preserve that clarity over time.

⬆️ [(read again)](#5-design-philosophy-recap)