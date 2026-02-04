import discord

# ============================================================
# Discord Configuration
# ============================================================

"""
This module defines Discord-specific configuration values
used by the application.

Design goals:
- Centralize Discord configuration in one place
- Avoid hardcoding values inside business logic
- Provide safe defaults suitable for most bots
- Allow easy extension by advanced users

This module:
- DOES define intents and Discord-level constants
- DOES NOT contain application logic
- DOES NOT access environment variables directly
"""


# ============================================================
# Gateway Intents
# ============================================================

"""
Intents define which events the bot will receive from Discord.

IMPORTANT:
- Only enable intents that are actually needed
- Privileged intents (members, message content) may require
  explicit enablement in the Discord Developer Portal
"""

INTENTS = discord.Intents.default()

# ------------------------------------------------------------
# Core intents (SAFE DEFAULTS)
# ------------------------------------------------------------

# Required for slash commands and interactions
INTENTS.guilds = True

# ------------------------------------------------------------
# Message-related intents (OPTIONAL)
# ------------------------------------------------------------

# Enable only if your bot actively processes message events
# (Not required for slash-command-only bots)
# INTENTS.messages = True

# Enable ONLY if your bot needs access to message content
# Requires manual enablement in Discord Developer Portal
INTENTS.message_content = False

# ------------------------------------------------------------
# Member-related intents (OPTIONAL / PRIVILEGED)
# ------------------------------------------------------------

# Enable only if your bot needs member events
# (joins, leaves, role changes, etc.)
INTENTS.members = False


# ============================================================
# Application Defaults
# ============================================================

"""
These values are safe defaults that can be referenced
by the client or other modules.

They are OPTIONAL and can be removed or extended
depending on the use case.
"""

# Default command prefix
# NOTE:
# - Not used by slash commands
# - Provided only for future prefix-command support
DEFAULT_COMMAND_PREFIX = "!"


# ============================================================
# Discord Limits & Constants
# ============================================================

"""
These constants reflect Discord platform limits.
They are provided here for reference and validation.
"""

# Maximum embed description length
EMBED_DESCRIPTION_LIMIT = 4096

# Maximum embed field value length
EMBED_FIELD_VALUE_LIMIT = 1024

# Maximum number of embed fields
EMBED_FIELD_COUNT_LIMIT = 25
