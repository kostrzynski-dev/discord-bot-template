# ============================================================
# UI Theme & Visual Constants
# ============================================================

import discord

"""
This module defines ALL visual constants used across the bot.

Purpose:
- Centralize embed colors and UI-related constants
- Ensure consistent visual language across commands
- Make future theming or rebranding trivial

Design principles:
- Neutral (no product-specific branding)
- Minimal but expressive
- Easy to extend (new colors, styles, presets)

IMPORTANT:
- Do NOT hardcode colors inside commands
- Always import colors from this module
"""


# ============================================================
# Core Color Palette
# ============================================================

#: Success / positive feedback (e.g. operation completed)
COLOR_SUCCESS = discord.Color.green()

#: Warning / important notice (e.g. limited access, partial action)
COLOR_WARNING = discord.Color.gold()

#: System / error / restricted actions
COLOR_ERROR = discord.Color.red()


# ============================================================
# Informational Colors
# ============================================================

#: Neutral informational messages
COLOR_INFO = discord.Color.blurple()

#: Secondary / non-critical UI elements
COLOR_SECONDARY = discord.Color.light_grey()


# ============================================================
# Semantic Aliases (Readability Layer)
# ============================================================

"""
These aliases improve readability in higher-level code.

Example:
- Use COLOR_SYSTEM instead of COLOR_ERROR when the message
  represents a system-level restriction rather than a failure.
"""

COLOR_SYSTEM = COLOR_ERROR
COLOR_NEUTRAL = COLOR_INFO


# ============================================================
# UX Helper Presets (Optional, Safe to Ignore)
# ============================================================

"""
This section is OPTIONAL.

These presets are NOT required for the template to function,
but they demonstrate how to standardize embed usage.

They can be safely removed or extended by the buyer.
"""


def build_info_embed(
    *,
    title: str | None = None,
    description: str | None = None,
) -> discord.Embed:
    """
    Builds a standardized informational embed.

    Intended usage:
    - status messages
    - confirmations
    - read-only information

    Args:
        title: Optional embed title
        description: Optional embed description

    Returns:
        discord.Embed instance
    """

    return discord.Embed(
        title=title,
        description=description,
        color=COLOR_INFO,
    )


def build_warning_embed(
    *,
    title: str | None = None,
    description: str | None = None,
) -> discord.Embed:
    """
    Builds a standardized warning embed.

    Intended usage:
    - permission warnings
    - non-critical issues
    - user guidance messages
    """

    return discord.Embed(
        title=title,
        description=description,
        color=COLOR_WARNING,
    )


def build_error_embed(
    *,
    title: str | None = None,
    description: str | None = None,
) -> discord.Embed:
    """
    Builds a standardized error/system embed.

    Intended usage:
    - blocked actions
    - system restrictions
    - unexpected failures (UX layer only)
    """

    return discord.Embed(
        title=title,
        description=description,
        color=COLOR_ERROR,
    )
