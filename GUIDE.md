![Discord Bot Template Banner](assets/branding/guide_banner.png)

# 🧭 Development Guide — Discord Bot Template

Welcome to the **Discord Bot Template Development Guide**.

This document is the **authoritative guide** for extending and evolving
the Discord Bot Template in a way that remains **architecturally sound,
predictable, and maintainable**.

> 🎯 Goal of this project:
> - understand *where* new code should live,
> - understand *why* certain patterns exist,
> - extend the template without breaking its foundations.

---

## 📚 Table of Contents

- [0. How to Read This Guide](#0-how-to-read-this-guide)
- [1. Mental Model of the Template](#1-mental-model-of-the-template)
- [2. Where Should This Code Live?](#2-where-should-this-code-live)
- [3. Extending Commands (Cogs)](#3-extending-commands-cogs)
- [4. Error Handling — The Right Way](#4-error-handling--the-right-way)
- [5. Logging & Observability Extensions](#5-logging--observability-extensions)
- [6. Configuration & Environment Patterns](#6-configuration--environment-patterns)
- [7. Development Utilities & Testing Patterns](#7-development-utilities--testing-patterns)
- [8. Anti-Patterns (What NOT to Do)](#8-anti-patterns-what-not-to-do)
- [9. Growing Beyond the Template](#9-growing-beyond-the-template)

---

## 0. How to Read This Guide

⬆️ [(back to table of contents)](#-table-of-contents)

This guide is **not a tutorial** and **not a step-by-step walkthrough**.

It is a **development playbook** that explains how to extend the
Discord Bot Template **without breaking its architecture**.

---

### 🎯 Who This Guide Is For

This guide is written for developers who:
- want to build **serious, long-lived Discord bots**,
- care about **code structure and predictability**,
- prefer understanding *why* something works, not just *how*.

It is suitable for:
- **junior developers** learning architectural thinking,
- **mid-level developers** building real features,
- **senior developers** evaluating or extending the foundation.

---

### 🧠 How This Guide Is Structured

Each section of this guide focuses on a **specific aspect of extension**.

You will find:
- conceptual explanations that define *how to think* about the system,
- concrete recommendations on *where code should live*,
- explicit examples using **real patterns from this template**,
- clear warnings about **anti-patterns and shortcuts**.

The sections are intentionally ordered.
Skipping ahead without understanding earlier parts
will likely lead to confusion or misuse.

---

### 🔍 How to Read Code Examples

Code examples in this guide are **intentional and opinionated**.

They are meant to:
- illustrate **recommended patterns**,
- show **common mistakes** and why they are problematic,
- demonstrate how small decisions affect long-term maintainability.

Unless explicitly stated otherwise:
- examples follow the existing project structure,
- naming conventions match the template,
- shortcuts are avoided on purpose.

---

### 🚫 What This Guide Does NOT Cover

This guide does not aim to:
- teach Python fundamentals,
- explain how Discord works internally,
- replace official `discord.py` documentation,
- provide copy-paste solutions without context.

Its goal is to help you make **good architectural decisions**
when working within this template.

⬆️ [(read again)](#0-how-to-read-this-guide)

---

## 1. Mental Model of the Template

⬆️ [(back to table of contents)](#-table-of-contents)

Before extending the template, it is critical to understand **how it is meant
to be thought about**, not just how it is structured.

This project is not organized around files or folders.
It is organized around **responsibilities and execution flow**.

---

### 🧱 The Template Is a System, Not a Script

The Discord Bot Template is designed as a **long-running system**.

It assumes:
- the bot will run continuously,
- failures will happen,
- features will grow over time,
- multiple developers may touch the codebase.

As a result:
- structure matters more than speed of implementation,
- predictability matters more than convenience,
- explicit behavior is preferred over “magic”.

---

### 🧠 Responsibility-Driven Design

Every part of the template exists to serve **one primary responsibility**.

At a high level, the system can be thought of as four conceptual layers:

- **Bootstrap layer**
  - application entry point,
  - environment validation,
  - logging initialization.

- **Application core**
  - Discord client lifecycle,
  - command registration and execution,
  - global error interception.

- **Feature layer**
  - user-facing commands,
  - feature-specific logic,
  - permission and guard checks.

- **Infrastructure layer**
  - logging and reporting,
  - error context and diagnostics,
  - shared helpers and utilities.

Each layer depends only on layers *below* it.
Dependencies never flow upward.

---

### 🔗 Dependency Direction Is Not Optional

The template enforces a **one-directional dependency model**.

This means:
- feature code may use utilities and logging,
- utilities may use infrastructure components,
- infrastructure must never depend on features.

Violating this rule leads to:
- circular dependencies,
- hidden coupling,
- fragile runtime behavior.

If a dependency feels “slightly wrong”,
it is usually a sign that the logic belongs elsewhere.

---

### 🎯 What the Template Optimizes For

This template is optimized for:
- clarity over cleverness,
- explicit behavior over convenience,
- long-term maintainability over short-term speed,
- safe extension over rapid experimentation.

It intentionally avoids:
- implicit side effects,
- global state scattered across modules,
- feature logic leaking into infrastructure code.

This means that some things may feel more verbose —
by design.

---

### 🚧 What the Template Does NOT Optimize For

The template does **not** aim to:
- be the smallest possible Discord bot,
- hide complexity behind abstractions,
- auto-generate features,
- optimize for copy-paste development.

If you are looking for a quick prototype,
this template may feel restrictive.

If you are building something meant to last,
the constraints will work in your favor.

---

### 🧭 How This Mental Model Guides Extension

When adding new code, always ask:

- *What responsibility does this logic have?*
- *Which layer should own it?*
- *Who should be allowed to depend on it?*
- *What should happen when it fails?*

Most extension decisions become obvious
once these questions are answered honestly.

⬆️ [(read again)](#1-mental-model-of-the-template)

---

## 2. Where Should This Code Live?

⬆️ [(back to table of contents)](#-table-of-contents)

One of the fastest ways to destroy an otherwise good architecture
is to place new code in the wrong location.

This section exists to prevent that.

---

### 🧭 The Core Question You Should Always Ask

Before writing any new code, ask yourself:

> **What is the primary responsibility of this logic?**

Do **not** ask:
- “Where is it easiest to put this?”
- “Where do I already have access to this?”
- “Where did I put something similar last time?”

Those questions lead to architectural drift.

---

### 🧱 Responsibility → Location Mapping

Use the following mental mapping when deciding where code should live:

- **User-facing behavior**
  - Commands, interactions, feature flow
  - → `bot/cogs/`

- **Reusable logic shared across features**
  - Guards, helpers, small pure functions
  - → `bot/utils/`

- **Runtime behavior & orchestration**
  - Client lifecycle, configuration loading
  - → `bot/client.py`, `bot/settings.py`, `bot/config.py`

- **Diagnostics & observability**
  - Logging, error context, reporting
  - → `bot/logging/`

If your code does not clearly fit one category,
it usually means the responsibility is not well defined yet.

---

### ❌ Common Mistake: Logic Inside a Cog

A very common anti-pattern is placing **business or reusable logic**
directly inside a Cog method.

❌ **Bad example:**

```python
class ExampleCog(commands.Cog):
    @app_commands.command(name="example")
    async def example(self, interaction: discord.Interaction):
        if interaction.user.id not in ALLOWED_IDS:
            raise AuthorizationError("User is not authorized")

        result = expensive_computation(interaction.user.id)
        await interaction.response.send_message(result)
```

Problems with this approach:

- logic is tightly coupled to Discord,
- cannot be reused elsewhere,
- difficult to test,
- error handling becomes inconsistent.

> The concrete error type depends on your error system; examples here are illustrative.

---

### ✅ Recommended Pattern: Thin Cog, Clear Responsibilities

A Cog should act as a boundary layer, not a logic container.

✅ **Better approach:**

```python
class ExampleCog(commands.Cog):
    @app_commands.command(name="example")
    async def example(self, interaction: discord.Interaction):
        ensure_user_is_allowed(interaction)
        result = compute_example_result(interaction.user.id)
        await interaction.response.send_message(result)
```

Where:

- permission checks live in `utils`,
- computation logic lives in a dedicated helper or service,
- the Cog only coordinates execution.

This keeps feature logic:

- readable,
- testable,
- easy to extend.

---

### 🧩 When Should Code Go Into `utils/`?

Use `bot/utils/` only for logic that is:

- small and focused,
- reusable across multiple features,
- independent of Discord-specific state,
- easy to reason about in isolation.

Good examples:

- permission guards,
- small data transformations,
- formatting helpers,
- feature flags.

If a utility starts growing:

- accumulating state,
- knowing too much about features,
- handling complex workflows,

it no longer belongs in `utils/`.

---

### 🚫 The “Miscellaneous” Trap

Never use `utils/` as a dumping ground.

If you find yourself thinking:

> “I’ll just put this in utils for now…”

Stop.

That is a sign that:

- the responsibility is unclear,
- the feature needs its own module,
- or the architecture needs to evolve.

Unclear placement today becomes technical debt tomorrow.

---

### 🧠 A Simple Decision Checklist

When in doubt, ask:

- *Is this logic user-facing?*
- *Does it depend on Discord-specific objects?*
- *Will multiple features need this?*
- *What happens when this fails?*

Answering these questions honestly
will usually point you to the correct location.

⬆️ [(read again)](#2-where-should-this-code-live)

---

## 3. Extending Commands (Cogs)

⬆️ [(back to table of contents)](#-table-of-contents)

Commands are the **primary way users interact with the bot**.
In this template, commands are implemented using **Cogs**
and treated as **feature boundaries**, not logic containers.

This section explains how to extend the bot correctly
by adding new commands and Cogs without breaking architectural rules.

---

### 🧠 What a Cog Is (and What It Is Not)

A Cog represents:
- a **feature boundary**,
- a collection of related commands,
- a coordination layer between Discord and your logic.

A Cog is **not**:
- a place for business logic,
- a utility module,
- a stateful service container.

If a Cog grows large or complex,
it is usually a sign that logic should be moved elsewhere.

---

### 📁 Where Cogs Live

All Cogs live in:

- `bot/cogs/`

Each Cog should:
- focus on a single feature or concern,
- have a clear, descriptive name,
- avoid dependencies on other Cogs.

If two Cogs need to share logic,
that logic does **not** belong in either Cog.

---

### ➕ Adding a New Cog

The recommended way to add a new feature
is to create a **new Cog file**.

Example structure:

```text
bot/cogs/
├── core.py
├── dev.py
└── example.py
```

The Cog file should:

- define one Cog class,
- expose a `setup` function,
- register commands explicitly.

---

### ❌ Common Anti-Pattern: Logic Inside Commands

A frequent mistake is implementing feature logic
directly inside command handlers.

❌ **Bad example:**

```python
class ExampleCog(commands.Cog):
    @app_commands.command(name="example")
    async def example(self, interaction: discord.Interaction):
        if interaction.user.id not in ALLOWED_IDS:
            raise AuthorizationError("User is not authorized")

        data = expensive_database_call()
        processed = complex_transformation(data)

        await interaction.response.send_message(processed)
```

Problems:

- logic is tightly coupled to Discord,
- cannot be reused or tested easily,
- error handling becomes inconsistent,
- commands become hard to reason about.

> The concrete error type depends on your error system; examples here are illustrative.

---

### ✅ Recommended Pattern: Thin Commands, Explicit Flow

Commands should be **thin orchestration layers.**

✅ **Better approach:**

```python
class ExampleCog(commands.Cog):
    @app_commands.command(name="example")
    async def example(self, interaction: discord.Interaction):
        ensure_user_is_allowed(interaction)
        result = get_example_result(interaction.user.id)
        await interaction.response.send_message(result)
```

Where:

- permission checks live in `utils`,
- feature logic lives in helpers or services,
- the command only coordinates execution.

This pattern:

- keeps commands readable,
- enables reuse,
- simplifies testing,
- integrates naturally with global error handling.

---

### 🛡️ Guards, Permissions, and Validation

Permission checks and guards should:

- be reusable,
- live outside the Cog,
- raise meaningful errors when violated.

Good places for guards:

- `bot/utils/error_handler.py`
- `bot/utils/helpers.py`

Never silently fail inside a command.
If something is not allowed, fail **explicitly**
and let the global error handler handle the response.

---

### 🧪 DEV-Only Commands and Features

The template supports **development-only behavior** by design.

Typical use cases:

- debug commands,
- test utilities,
- experimental features.

DEV-only commands should:

- live in a dedicated Cog (e.g. `dev.py`),
- be explicitly gated by environment checks,
- never be available in production.

Example strategies include:

- environment checks via settings,
- developer ID validation,
- guild-only command sync in DEV mode.

---

### ⚠️ Avoid Cross-Cog Dependencies

Cogs must remain **independent.**

Avoid:

- importing one Cog into another,
- calling methods across Cogs,
- sharing mutable state between Cogs.

If two Cogs need shared behavior,
extract that behavior into:

- a utility,
- a helper function,
- or a dedicated service module.

This preserves:

- modularity,
- testability,
- long-term maintainability.

---

### 🧭 When to Split a Cog

Split a Cog when:

- it grows beyond a single responsibility,
- commands become conceptually unrelated,
- feature logic starts leaking into the Cog.

A smaller Cog is almost always preferable
to a large, multi-purpose one.

⬆️ [(read again)](#3-extending-commands-cogs)

---

## 4. Error Handling — The Right Way

⬆️ [(back to table of contents)](#-table-of-contents)

Error handling in this template is a **core system**, not an afterthought.

The goal is not just to avoid crashes,
but to make failures **visible, consistent, and actionable**
across the entire application.

---

### 🧠 The Central Idea

This template follows a simple rule:

> **Commands do not handle errors.  
> The system does.**

Commands:
- detect invalid situations,
- raise meaningful errors,
- stop execution.

The rest is handled centrally.

---

### 🧱 Why Centralized Error Handling Matters

Scattered error handling leads to:
- inconsistent user messages,
- duplicated logic,
- swallowed exceptions,
- impossible debugging.

Centralized error handling provides:
- a single response strategy,
- structured diagnostics,
- predictable behavior,
- easier monitoring and alerting.

---

### ❌ Common Anti-Pattern: try/except Everywhere

A very common mistake is wrapping command logic
in local `try/except` blocks.

❌ **Bad example:**

```python
@app_commands.command(name="example")
async def example(self, interaction: discord.Interaction):
    try:
        result = do_something()
        await interaction.response.send_message(result)
    except Exception:
        await interaction.response.send_message("Something went wrong.")
```

Problems:

- errors lose context,
- logs lack useful information,
- all failures look the same,
- debugging becomes guesswork.

---

### ✅ Recommended Pattern: Raise, Don’t Handle

Commands should **raise errors explicitly**
and let the global error pipeline do its job.

✅ **Better approach:**

```python
@app_commands.command(name="example")
async def example(self, interaction: discord.Interaction):
    ensure_user_is_allowed(interaction)
    result = do_something_risky()
    await interaction.response.send_message(result)
```

If `ensure_user_is_allowed` or `do_something_risky`
fails, the error:

- propagates upward,
- is intercepted globally,
- is logged and reported consistently.

---

### 🧩 Using Error Context

The template provides a structured way
to attach **contextual information** to errors.

Error context allows you to capture:

- what the user was doing,
- which feature failed,
- relevant identifiers or parameters.

This makes logs:

- searchable,
- understandable,
- actionable.

When extending error handling:

- enrich context early,
- avoid catching errors prematurely,
- let the reporter decide what to expose to users.

---

### 📣 User Feedback vs Diagnostics

A key principle is **separation of concerns:**

- users receive **clear, safe messages,**
- logs contain **detailed technical information.**

Never expose:

- stack traces,
- internal identifiers,
- sensitive configuration details
- to end users.

The global error handler enforces this separation.

---

### 🧪 Handling Expected vs Unexpected Errors

Not all errors are equal.

Expected errors:

- permission violations,
- invalid input,
- unsupported operations.

Unexpected errors:

- unhandled exceptions,
- integration failures,
- programming bugs.

Expected errors should:

- raise specific error types,
- produce clear user-facing messages.

Unexpected errors should:

- be logged with full context,
- be reported for investigation,
- fail loudly, not silently.

---

### 🚫 Do Not Silence Errors

Never:

- catch an error and ignore it,
- replace it with a generic message,
- log it without context.

If an error happens,
it happened for a reason.

Your job is to make that reason visible
to the system.

---

### 🧭 When to Extend the Error System

You may want to extend error handling when:

- introducing new feature domains,
- integrating external services,
- adding operational monitoring,
- distinguishing new failure categories.

Extensions should:

- integrate with the existing pipeline,
- preserve centralized control,
- avoid feature-specific handling logic.

⬆️ [(read again)](#4-error-handling--the-right-way)

---

## 5. Logging & Observability Extensions

⬆️ [(back to table of contents)](#-table-of-contents)

Logging in this template is not just about printing messages.
It is about **observability** — the ability to understand
what the system is doing and why.

This section explains how to extend logging
without turning it into noise.

---

### 🧠 Logging as an Operational Tool

Logs exist primarily for:
- diagnosing failures,
- understanding system behavior,
- supporting incident response,
- validating assumptions in production.

They are **not** meant for:
- debugging via print statements,
- dumping arbitrary data,
- tracking feature flow step by step.

Good logs answer questions.
Bad logs create more questions.

---

### 📊 Log Levels and Their Meaning

Use log levels intentionally.

- **INFO**
  - expected lifecycle events,
  - successful operations,
  - high-level state changes.

- **WARNING**
  - unexpected but recoverable situations,
  - degraded behavior,
  - suspicious input or state.

- **ERROR**
  - failed operations,
  - unhandled exceptions,
  - data loss or corruption risks.

If everything is logged as ERROR,
nothing is an error.

---

### ❌ Common Anti-Pattern: Logging Everywhere

A frequent mistake is logging
every step of feature execution.

❌ **Bad example:**

```python
logger.info("Starting command")
logger.info("Validating user")
logger.info("Fetching data")
logger.info("Processing data")
logger.info("Sending response")
```

Problems:

- logs become noisy,
- important events are buried,
- operational signals are lost.

---

### ✅ Recommended Pattern: Log Meaningful Events

Log **state transitions** and **outcomes**, not steps.

✅ **Better approach:**

```python
logger.info(
    "Example command executed successfully",
    extra={"user_id": interaction.user.id}
)
```

This tells you:

- *what happened,*
- *that it succeeded,*
- *who triggered it.*

---

### 🧩 Contextual Logging

Logs are most useful when they include **context.**

Whenever possible, include:

- user identifiers,
- feature names,
- relevant parameters,
- environment information.

Context should be:

- structured,
- searchable,
- consistent.

Avoid embedding context only in message strings.
Prefer structured metadata where available.

---

### 🔍 Logging and Error Handling Work Together

Logging and error handling are **complementary systems.**

- expected errors may not require logs,
- unexpected errors should always be logged,
- error logs should include full context.

Never log an error and then swallow it.
If it matters enough to log,
it matters enough to propagate.

---

### 📣 Extending Observability

As the project grows, you may want to:

- add new log categories,
- integrate external monitoring,
- trigger alerts for critical failures.

When extending observability:

- build on the existing logging system,
- keep feature code unaware of log destinations,
- avoid hard-coding operational behavior in features.

Observability should remain centralized.

---

### 🚫 Avoid Log-Based Control Flow

Never make decisions based on log output.

Logs are:

- diagnostic signals,
- historical records.

They are not:

- state management,
- control mechanisms,
- feature toggles.

If logic depends on logs,
the responsibility is misplaced.

⬆️ [(read again)](#5-logging--observability-extensions)

---

## 6. Configuration & Environment Patterns

⬆️ [(back to table of contents)](#-table-of-contents)

Configuration in this template is treated as a **first-class concern**.

Runtime behavior is never inferred implicitly.
Every decision that depends on environment or configuration
is made **explicit and visible**.

---

### 🧠 Configuration Is Not Feature Logic

Configuration exists to:
- define **how** the application runs,
- control **environment-specific behavior**,
- enable or disable capabilities safely.

Configuration should **not**:
- contain business logic,
- replace feature decisions,
- be scattered across modules.

If behavior changes based on environment,
that decision must be traceable to configuration.

---

### 📁 Where Configuration Lives

Configuration responsibilities are intentionally split:

- **Environment variables**
  - provide raw runtime input,
  - live in `.env` (development only).

- **Settings layer**
  - validates and normalizes configuration,
  - exposes safe, typed access,
  - lives in `bot/settings.py`.

- **Runtime usage**
  - reads from settings,
  - never directly from environment variables.

Feature code should **never** call `os.getenv` directly.

---

### ❌ Common Anti-Pattern: Reading Environment Variables Everywhere

A frequent mistake is accessing environment variables
directly inside feature code.

❌ **Bad example:**

```python
if os.getenv("APP_ENV") == "dev":
    enable_debug_behavior()
```

Problems:

- behavior becomes implicit,
- configuration logic is duplicated,
- testing becomes difficult,
- environment usage spreads uncontrollably.

---

### ✅ Recommended Pattern: Centralized Settings Access

All configuration should be read and validated once
and then accessed via the settings layer.

✅ **Better approach:**

```python
if settings.is_dev:
    enable_debug_behavior()
```

This ensures that:

- configuration is validated at startup,
- behavior is predictable,
- changes are localized.

---

### 🧪 Environment-Aware Behavior (DEV vs PROD)

The template is designed to be **environment-aware by default.**

Typical environment-dependent behavior includes:

- command registration strategy,
- developer-only features,
- logging verbosity,
- operational safeguards.

Environment checks should:

- be explicit,
- be centralized,
- never be hidden inside helpers.

Avoid branching logic deep inside features.
Prefer high-level environment decisions.

---

### 🚦 Feature Flags and Runtime Switches

Feature flags are a powerful tool
when used carefully.

Good use cases:

- gradual feature rollout,
- experimental functionality,
- temporary operational switches.

Feature flags should:

- live in configuration,
- be documented,
- have clear defaults.

Avoid using flags as permanent conditionals.
They are meant to be temporary.

---

### 🛡️ Validation and Fail-Fast Behavior

Invalid configuration should:

- be detected early,
- fail fast,
- prevent the application from starting.

Silent misconfiguration is worse
than an explicit startup failure.

If the application starts,
configuration should be assumed valid.

---

### 🚫 Avoid Configuration Sprawl

Never:

- introduce configuration without documentation,
- add environment variables without validation,
- depend on undeclared runtime behavior.

Every new configuration option is a contract.
Treat it accordingly.

⬆️ [(read again)](#6-configuration--environment-patterns)

---

## 7. Development Utilities & Testing Patterns

⬆️ [(back to table of contents)](#-table-of-contents)

Fast iteration is important — but not at the cost of stability.

This section explains how to use **development-only tools and patterns**
to debug, test, and experiment **without compromising production safety**.

---

### 🧠 Development and Production Must Stay Separate

The template treats **development and production as distinct environments**.

Development mode exists to:
- iterate quickly,
- experiment safely,
- inspect internal behavior.

Production mode exists to:
- be stable,
- predictable,
- safe for users.

Anything that exists purely for development
must be **explicitly gated**.

---

### 🧾 Project Snapshot Utility (`tools/snapshot`)

For maintainer workflows, this template provides a local snapshot generator:

- script: `tools/snapshot/generate.py`
- default output: `tools/snapshot/docs/PROJECT_SNAP.md`

Use case examples:
- creating a one-file state snapshot before large refactors,
- sharing architecture/code state in private reviews,
- keeping an offline audit snapshot for debugging sessions.

Run:

```bash
python tools/snapshot/generate.py
```

Security and hygiene defaults:
- local `.env*` files are excluded (except `.env.example`),
- virtualenv and cache artifacts are excluded,
- generated snapshot output is gitignored by default.

Treat this utility as a **developer tool**, not as runtime application logic.

---

---

### 🧪 Development-Only Commands

A common and effective pattern
is creating commands that exist **only in development**.

Typical use cases:
- inspecting internal state,
- triggering test errors,
- simulating edge cases,
- verifying permissions and guards.

Development-only commands should:
- live in a dedicated Cog (e.g. `dev.py`),
- be guarded by environment checks,
- never be synced globally.

If a command is useful only for developers,
it should never reach production users.

---

### 🔍 Debugging Without Side Effects

When debugging features, avoid:
- adding temporary prints,
- modifying production logic,
- bypassing guards or permissions.

Instead:
- add controlled debug commands,
- log relevant context at appropriate levels,
- simulate failure paths intentionally.

Debug code should be:
- removable,
- isolated,
- clearly marked as development-only.

---

### 🧩 Simulating Errors Intentionally

Testing error handling is as important
as testing successful paths.

Good candidates for simulation:
- permission violations,
- invalid input,
- external service failures,
- unexpected exceptions.

Simulated errors should:
- flow through the global error pipeline,
- produce the same diagnostics as real failures,
- never be handled locally.

This ensures that error handling
is exercised before production issues occur.

---

### 🧪 Testing Patterns That Respect the Architecture

Testing should respect responsibility boundaries.

Prefer testing:
- utilities in isolation,
- guards and helpers as pure functions,
- feature logic outside of Cogs.

Avoid testing:
- Discord-specific glue directly,
- tightly coupled command handlers,
- internal implementation details.

Thin commands and centralized logic
make meaningful testing possible.

---

### 🛡️ Avoid DEV Logic Leaking into PROD

A dangerous pattern is allowing
development behavior to affect production.

Never:
- rely on DEV flags deep inside feature logic,
- conditionally bypass checks in production,
- keep “temporary” DEV shortcuts long-term.

If a behavior must differ by environment,
that decision should be:
- explicit,
- centralized,
- documented.

---

### 🧭 When to Remove Development Utilities

Development utilities are **temporary by nature**.

Once a feature stabilizes:
- remove debug commands,
- reduce logging verbosity,
- clean up experimental switches.

Leaving development scaffolding in production
creates long-term maintenance risk.

⬆️ [(read again)](#7-development-utilities--testing-patterns)

---

## 8. Anti-Patterns (What NOT to Do)

⬆️ [(back to table of contents)](#-table-of-contents)

This section documents **common architectural anti-patterns**
that slowly degrade the template over time.

These patterns often start as “quick fixes”
and end as long-term maintenance problems.

Avoid them deliberately.

---

### ❌ Putting Business Logic Inside Cogs

Cogs are not meant to contain business logic.

Symptoms of this anti-pattern:
- large command methods,
- duplicated logic across commands,
- complex branching inside handlers.

Why this is harmful:
- logic becomes tightly coupled to Discord,
- reuse becomes difficult,
- testing becomes painful,
- error handling becomes inconsistent.

If logic grows inside a Cog,
it belongs somewhere else.

---

### ❌ Using `utils/` as a Dumping Ground

The `utils/` package is not a miscellaneous folder.

Red flags:
- files named `misc.py` or `helpers2.py`,
- unrelated functions grouped together,
- utilities that know too much about features.

Why this is harmful:
- responsibilities become unclear,
- dependencies spread unpredictably,
- refactoring becomes risky.

If something does not clearly belong in `utils/`,
it probably needs its own module.

---

### ❌ Local `try/except` as a Control Mechanism

Catching errors locally to “handle them quickly”
is a common shortcut.

Why this is harmful:
- errors lose context,
- logs become incomplete,
- failures look identical,
- the global error pipeline is bypassed.

Errors should be **raised**, not suppressed.
Handling belongs to the system, not the feature.

---

### ❌ Reading Environment Variables in Feature Code

Accessing environment variables directly inside features
breaks configuration boundaries.

Why this is harmful:
- behavior becomes implicit,
- configuration logic spreads across the codebase,
- testing and validation become difficult.

Feature code should depend on **settings**,
not on raw environment input.

---

### ❌ Cross-Feature Dependencies

Features should not depend on each other.

Red flags:
- importing one Cog into another,
- calling methods across features,
- sharing mutable state.

Why this is harmful:
- coupling increases rapidly,
- changes ripple unpredictably,
- isolation and modularity are lost.

Shared behavior belongs in shared layers,
not in feature-to-feature calls.

---

### ❌ Leaving Development Shortcuts in Production

Temporary shortcuts tend to become permanent.

Examples:
- DEV-only flags left enabled,
- debug commands never removed,
- permission bypasses “for now”.

Why this is harmful:
- production behavior becomes unpredictable,
- security assumptions break down,
- technical debt accumulates silently.

If something is temporary,
treat it as temporary.

---

### 🧭 Recognizing Architectural Drift Early

Architectural drift often shows up as:
- uncertainty about where code belongs,
- fear of touching certain modules,
- frequent “just this once” exceptions.

These are signals to stop and reassess.

Fixing small issues early
is far cheaper than large refactors later.

⬆️ [(read again)](#8-anti-patterns-what-not-to-do)

---

## 9. Growing Beyond the Template

⬆️ [(back to table of contents)](#-table-of-contents)

This template is designed to take you far —
but not forever in its original shape.

At some point, growth requires **intentional evolution**.
This section helps you recognize when that moment arrives
and how to approach it without breaking what already works.

---

### 🧠 The Template Is a Foundation, Not a Cage

The Discord Bot Template is intentionally opinionated.

Those opinions:
- protect architectural clarity,
- enforce responsibility boundaries,
- reduce long-term maintenance cost.

However, they are not meant to limit growth.

As your project evolves:
- new concerns will emerge,
- new abstractions may become necessary,
- new operational requirements may appear.

Growth is expected.
Chaos is not.

---

### 📈 Signals That the Project Is Outgrowing the Template

Common signals include:
- utilities growing into complex workflows,
- repeated patterns across multiple features,
- increasing integration with external services,
- rising operational or performance requirements.

These are not problems.
They are indicators that the project is maturing.

Ignoring them is what creates problems.

---

### 🧱 When to Introduce New Layers or Modules

Consider introducing new layers when:
- a responsibility no longer fits existing boundaries,
- logic becomes too complex for simple helpers,
- multiple features depend on the same domain behavior.

Examples include:
- service layers for external integrations,
- domain modules for complex business logic,
- background task or scheduling systems.

New layers should:
- have explicit responsibilities,
- respect dependency direction,
- integrate with existing error and logging systems.

---

### 🔌 Evolving Toward a Framework

At scale, the template may evolve into
a **project-specific framework**.

This often includes:
- standardized feature patterns,
- shared base classes or utilities,
- enforced conventions across modules.

When this happens:
- document new rules explicitly,
- resist implicit behavior,
- preserve the clarity of the original design.

A framework should make good decisions easy —
not hide decisions altogether.

---

### 🛡️ Protecting the Original Principles

As the codebase grows, it becomes tempting
to relax rules “just this once”.

Resist that urge.

The principles defined in:
- `README.md`,
- `STRUCTURE.md`,
- this guide,
- `tools/snapshot/generate.py` (for local snapshot workflows),

exist to protect the project **over time**, not just today.

If a rule no longer fits,
change it deliberately —
never accidentally.

---

### 🚀 Final Advice

Growth is not about adding more code.
It is about adding **the right structure at the right time**.

If you:
- respect responsibility boundaries,
- keep error handling centralized,
- treat configuration as a contract,
- remain intentional about change,

this template will support you
far beyond its initial scope.

⬆️ [(read again)](#9-growing-beyond-the-template)