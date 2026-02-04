from datetime import timezone

import discord

from bot.settings import Settings
from bot.logging.error_context import ErrorContext, ErrorSeverity
from bot.utils.theme import COLOR_ERROR


# ============================================================
# System Error Reporter (Discord-facing / Support-only)
# ============================================================

class ErrorReporter:
    """
    Reports system-level errors to a designated Discord channel.

    Responsibilities:
    - Send ERROR / CRITICAL events to a support or system channel
    - Present structured, diagnostic-friendly error information
    - Avoid exposing sensitive data (e.g. tracebacks)

    Design principles:
    - Discord-specific (embeds, channels)
    - NO logging responsibility (handled by SystemLogger)
    - NO user-facing UX logic
    - SUPPORT / OPERATIONS visibility only
    """

    def __init__(self, bot: discord.Client):
        """
        Args:
            bot: Active Discord client instance
        """
        self.bot = bot

    # ========================================================
    # Public API
    # ========================================================

    async def report(self, context: ErrorContext) -> None:
        """
        Sends a system error report to the configured support channel.

        Conditions:
        - A valid SYSTEM_ERROR_CHANNEL_ID must be configured
        - Error severity must be ERROR or CRITICAL

        This method is intentionally silent on failure.
        """

        # ----------------------------------------------------
        # Configuration guard
        # ----------------------------------------------------

        channel_id = Settings.SYSTEM_ERROR_CHANNEL_ID
        if not channel_id:
            return

        if context.severity not in (
            ErrorSeverity.ERROR,
            ErrorSeverity.CRITICAL,
        ):
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        # ----------------------------------------------------
        # Timestamp (single source of truth)
        # ----------------------------------------------------

        timestamp = context.timestamp.astimezone(
            timezone.utc
        ).strftime("%Y-%m-%d %H:%M UTC")

        # ----------------------------------------------------
        # Embed construction (support-oriented)
        # ----------------------------------------------------

        embed = discord.Embed(
            title="System Error Detected",
            color=COLOR_ERROR,
        )

        embed.add_field(
            name="Timestamp",
            value=timestamp,
            inline=False,
        )

        embed.add_field(
            name="Severity",
            value=context.severity.value,
            inline=True,
        )

        embed.add_field(
            name="Source",
            value=context.source.value,
            inline=True,
        )

        # ----------------------------------------------------
        # Contextual metadata
        # ----------------------------------------------------

        if context.command_name:
            embed.add_field(
                name="Command",
                value=context.command_name,
                inline=False,
            )

        if context.user_id:
            embed.add_field(
                name="User ID",
                value=f"`{context.user_id}`",
                inline=True,
            )

        if context.guild_id:
            embed.add_field(
                name="Guild ID",
                value=f"`{context.guild_id}`",
                inline=True,
            )

        embed.add_field(
            name="Error Type",
            value=context.exception_type or "Unknown",
            inline=False,
        )

        embed.add_field(
            name="Error Message",
            value=context.exception_message or "No details provided.",
            inline=False,
        )

        embed.add_field(
            name="Error ID",
            value=f"`{context.error_id}`",
            inline=False,
        )

        embed.add_field(
            name="Recommended Action",
            value=(
                "Check application logs for full context.\n"
                "Investigate the affected module or command.\n"
                "Escalate if the issue repeats."
            ),
            inline=False,
        )

        # ----------------------------------------------------
        # Dispatch
        # ----------------------------------------------------

        await channel.send(embed=embed)
