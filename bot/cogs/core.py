import discord
from discord.ext import commands
from discord import app_commands

from bot.utils.error_handler import handle_interaction_error
from bot.utils.helpers import safe_respond
from bot.utils.theme import (
    COLOR_SUCCESS,
    COLOR_WARNING,
)


# ============================================================
# Core Commands Cog
# ============================================================

class CoreCog(commands.Cog):
    """
    Core application commands.

    This cog provides:
    - A minimal, always-available command set
    - A reference implementation for new commands
    - A safe learning ground for template users

    Design rules:
    - NO permission logic
    - NO server-specific configuration
    - NO side effects

    This file is intentionally simple and educational.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """
        Initializes the CoreCog.

        Args:
            bot: The main Discord bot client instance
        """
        self.bot = bot

    # ========================================================
    # /ping
    # ========================================================

    @app_commands.command(
        name="ping",
        description="Check if the bot is responding",
    )
    async def ping(self, interaction: discord.Interaction) -> None:
        """
        Basic health-check command.

        Purpose:
        - Verify bot connectivity
        - Validate slash command pipeline
        - Measure websocket latency

        This command is intentionally trivial and safe.
        """

        try:
            latency_ms = round(self.bot.latency * 1000)

            embed = discord.Embed(
                title="Pong",
                description=f"Latency: **{latency_ms} ms**",
                color=COLOR_SUCCESS,
            )

            await safe_respond(
                interaction,
                embed=embed,
                ephemeral=True,
            )

        except Exception as error:
            await handle_interaction_error(interaction, error)

    # ========================================================
    # /about
    # ========================================================

    @app_commands.command(
        name="about",
        description="Display information about this bot",
    )
    async def about(self, interaction: discord.Interaction) -> None:
        """
        Displays basic information about the application.

        Demonstrates:
        - Static informational embeds
        - Structured text content
        - Clean UX without permissions or state

        This command can be freely modified or removed.
        """

        try:
            embed = discord.Embed(
                title="Discord Bot Template",
                description=(
                    "This application is built using a "
                    "production-ready Discord bot template.\n\n"
                    "The template focuses on clean architecture, "
                    "modularity, and professional error handling."
                ),
                color=COLOR_WARNING,
            )

            embed.add_field(
                name="Included Features",
                value=(
                    "• Slash command architecture\n"
                    "• Centralized error handling\n"
                    "• DEV / PROD environment separation\n"
                    "• Modular cog-based structure"
                ),
                inline=False,
            )

            embed.set_footer(
                text="This content can be customized or removed."
            )

            await safe_respond(
                interaction,
                embed=embed,
                ephemeral=True,
            )

        except Exception as error:
            await handle_interaction_error(interaction, error)
