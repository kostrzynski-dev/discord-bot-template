import discord
from discord import app_commands

from bot.utils.error_handler import handle_interaction_error


# ============================================================
# Global Application Command Error Interceptor
# ============================================================

"""
This module acts as a global safety net for ALL application command errors.

It is registered once on the CommandTree and guarantees that:
- No AppCommandError is ever left unhandled
- Wrapped exceptions are correctly unwrapped
- All errors are routed through the centralized error handler

This file should remain:
- Small
- Predictable
- Free of business logic
"""


# ============================================================
# Public API
# ============================================================

async def global_app_command_error_handler(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
) -> None:
    """
    Global interceptor for ALL application command errors.

    Execution flow:
    1. Receive AppCommandError from Discord
    2. Unwrap original exception if present
    3. Delegate full handling to the central error handler

    Notes:
    - Discord wraps real exceptions inside AppCommandError
    - The original exception is usually available via `error.original`
    - This function MUST NOT contain any logging or UI logic
    """

    # --------------------------------------------------------
    # Extract original exception (if wrapped)
    # --------------------------------------------------------

    original_error: Exception = error

    if hasattr(error, "original") and error.original:
        original_error = error.original

    # --------------------------------------------------------
    # Delegate handling to centralized error pipeline
    # --------------------------------------------------------

    await handle_interaction_error(interaction, original_error)
