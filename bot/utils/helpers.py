from typing import Optional
import discord

from bot.settings import Settings


# ============================================================
# Generic Helpers & Guards
# ============================================================

"""
This module provides small, reusable helper functions
used across the application.

Design goals:
- Keep helpers stateless and predictable
- Avoid business logic
- Avoid Discord side effects
- Provide safe defaults
- Be easy to extend without modifying core logic

This module is intentionally lightweight and generic.
"""


# ============================================================
# Interaction Context Helpers
# ============================================================

def is_guild_interaction(
    interaction: discord.Interaction,
) -> bool:
    """
    Checks whether the interaction was executed inside a guild.

    Useful for commands that must not be used in DMs.
    """
    return interaction.guild is not None


def is_dm_interaction(
    interaction: discord.Interaction,
) -> bool:
    """
    Checks whether the interaction was executed in a direct message.
    """
    return interaction.guild is None


# ============================================================
# Permission Helpers (Discord-level)
# ============================================================

def has_administrator_permissions(
    interaction: discord.Interaction,
) -> bool:
    """
    Checks whether the interacting user has administrator permissions.

    Returns:
        False if the interaction user is not a guild member.
    """
    if not isinstance(interaction.user, discord.Member):
        return False

    return interaction.user.guild_permissions.administrator


def has_manage_guild_permissions(
    interaction: discord.Interaction,
) -> bool:
    """
    Checks whether the interacting user has permission
    to manage the guild.
    """
    if not isinstance(interaction.user, discord.Member):
        return False

    return interaction.user.guild_permissions.manage_guild


# ============================================================
# Environment & Identity Guards
# ============================================================

def is_dev_environment() -> bool:
    """
    Checks whether the application is running in DEV mode.
    """
    return Settings.IS_DEV


def is_developer(
    interaction: Optional[discord.Interaction],
) -> bool:
    """
    Checks whether the interacting user is listed
    as a developer in environment configuration.
    """
    if interaction is None or not interaction.user:
        return False

    return interaction.user.id in Settings.DEVELOPER_IDS


def is_dev_authorized(
    interaction: Optional[discord.Interaction],
) -> bool:
    """
    Combined DEV authorization guard.

    DEV access is granted ONLY when:
    - Application runs in DEV mode
    - User is listed as a developer
    """
    return is_dev_environment() and is_developer(interaction)


# ============================================================
# Safe Response Utilities
# ============================================================

async def safe_respond(
    interaction: Optional[discord.Interaction],
    *,
    content: Optional[str] = None,
    embed: Optional[discord.Embed] = None,
    ephemeral: bool = True,
) -> None:
    """
    Safely responds to an interaction without raising
    'interaction already responded' errors.

    This helper SHOULD be used when responding from:
    - shared utilities
    - deeply nested logic
    - error handling paths

    Args:
        interaction: Discord interaction instance
        content: Optional message content
        embed: Optional embed
        ephemeral: Whether the response should be ephemeral
    """
    if interaction is None:
        return

    if interaction.response.is_done():
        await interaction.followup.send(
            content=content,
            embed=embed,
            ephemeral=ephemeral,
        )
    else:
        await interaction.response.send_message(
            content=content,
            embed=embed,
            ephemeral=ephemeral,
        )


# ============================================================
# Extension Notes
# ============================================================

"""
COMMON EXTENSIONS:

Users may extend this module with:
- Role-based access checks
- Feature flags
- License / subscription validation
- Rate-limit guards
- Server-specific configuration lookups

IMPORTANT:
- Keep this module simple
- Avoid side effects
- Move complex logic into dedicated services
"""
