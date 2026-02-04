import traceback
import discord

from bot.logging.error_context import (
    ErrorContext,
    ErrorSeverity,
    ErrorSource,
)
from bot.logging.logger import logger
from bot.logging.reporter import ErrorReporter
from bot.utils.theme import COLOR_WARNING, COLOR_ERROR, COLOR_INFO


# ============================================================
# Centralized Interaction Error Handling
# ============================================================

"""
This module is the single, authoritative entry point for handling
ALL interaction-related errors (slash commands, context menus, etc.).

Design goals:
- One source of truth for error processing
- Full error context propagation
- Consistent UX for end users
- Clear separation of responsibilities

This module intentionally:
- DOES NOT swallow exceptions silently
- DOES NOT apply product-specific logic
- DOES NOT enforce branding or narrative tone
"""


# ============================================================
# Severity → Visual Mapping (UX Layer)
# ============================================================

def _color_for_severity(severity: ErrorSeverity) -> discord.Color:
    """
    Maps error severity to a visual color.

    UX rule:
    - INFO / WARNING → non-alarming
    - ERROR / CRITICAL → explicit failure
    """

    if severity in (ErrorSeverity.ERROR, ErrorSeverity.CRITICAL):
        return COLOR_ERROR

    if severity == ErrorSeverity.WARNING:
        return COLOR_WARNING

    return COLOR_INFO


# ============================================================
# Severity Classification
# ============================================================

def _classify_severity(error: Exception) -> ErrorSeverity:
    """
    Classifies exception severity.

    This logic is intentionally conservative and extensible.
    """

    if isinstance(error, PermissionError):
        return ErrorSeverity.WARNING

    if isinstance(error, ValueError):
        return ErrorSeverity.WARNING

    if isinstance(error, discord.Forbidden):
        return ErrorSeverity.ERROR

    return ErrorSeverity.ERROR


# ============================================================
# Public API
# ============================================================

async def handle_interaction_error(
    interaction: discord.Interaction,
    error: Exception,
) -> None:
    """
    Central handler for all interaction-related exceptions.

    Execution flow:
    1. Classify severity
    2. Build structured ErrorContext
    3. Log error to backend logger
    4. Report error via reporting layer (optional)
    5. Send user-facing feedback (ephemeral)
    """

    severity = _classify_severity(error)

    # --------------------------------------------------------
    # Build error context
    # --------------------------------------------------------

    context = ErrorContext(
        severity=severity,
        source=ErrorSource.COMMAND,
        command_name=interaction.command.name if interaction.command else None,
        guild_id=interaction.guild.id if interaction.guild else None,
        user_id=interaction.user.id if interaction.user else None,
        exception_type=type(error).__name__,
        exception_message=str(error),
        traceback=traceback.format_exc(),
    )

    # --------------------------------------------------------
    # Backend logging
    # --------------------------------------------------------

    logger.log_error(context)

    # --------------------------------------------------------
    # Optional system reporting
    # --------------------------------------------------------

    if interaction.client:
        reporter = ErrorReporter(interaction.client)
        await reporter.report(context)

    # --------------------------------------------------------
    # User-facing response (UX layer)
    # --------------------------------------------------------

    embed = discord.Embed(
        title="An error occurred",
        description=(
            "The request could not be completed due to an internal error.\n\n"
            f"**Error ID:** `{context.error_id}`"
        ),
        color=_color_for_severity(context.severity),
    )

    embed.set_footer(
        text="If this issue persists, please contact the system administrator."
    )

    # --------------------------------------------------------
    # Safe interaction response
    # --------------------------------------------------------

    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)
