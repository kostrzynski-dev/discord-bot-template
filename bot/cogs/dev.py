import discord
from discord.ext import commands
from discord import app_commands

from bot.settings import Settings
from bot.utils.error_handler import handle_interaction_error
from bot.utils.helpers import safe_respond
from bot.utils.theme import COLOR_WARNING


# ============================================================
# Developer Utilities Cog
# ============================================================

class DevCog(commands.Cog):
    """
    Developer-only utilities.

    This cog provides tools intended strictly for development
    and testing environments.

    Primary use cases:
    - Verifying developer access control
    - Testing the global error handling pipeline
    - Simulating controlled failure scenarios

    SECURITY NOTE:
    - This cog is automatically DISABLED in production mode
    - Developer identity alone is NOT sufficient in PROD
    """

    def __init__(self, bot: commands.Bot) -> None:
        """
        Initializes the DevCog.

        Args:
            bot: The main Discord bot client instance
        """
        self.bot = bot

    # ========================================================
    # Internal guards
    # ========================================================

    def _is_dev_environment(self) -> bool:
        """
        Checks whether the application is running in DEV mode.
        """
        return Settings.IS_DEV

    def _is_developer(self, interaction: discord.Interaction) -> bool:
        """
        Checks whether the invoking user is an authorized developer.

        Authorization source:
        - Settings.DEVELOPER_IDS (environment-based)

        Returns:
            bool: True if user is a developer, otherwise False
        """
        if not interaction.user:
            return False

        return interaction.user.id in Settings.DEVELOPER_IDS

    def _is_authorized(self, interaction: discord.Interaction) -> bool:
        """
        Combined authorization guard.

        DEV commands are allowed ONLY when:
        - Application runs in DEV mode
        - User is listed as a developer
        """
        return self._is_dev_environment() and self._is_developer(interaction)

    # ========================================================
    # /dev_ping
    # ========================================================

    @app_commands.command(
        name="dev_ping",
        description="Developer-only diagnostic ping",
    )
    async def dev_ping(self, interaction: discord.Interaction) -> None:
        """
        Simple developer-only diagnostic command.

        Purpose:
        - Validate DEV environment enforcement
        - Confirm developer access control
        - Verify DevCog is loaded correctly
        """

        try:
            if not self._is_authorized(interaction):
                await safe_respond(
                    interaction,
                    content="Developer access denied.",
                    ephemeral=True,
                )
                return

            embed = discord.Embed(
                title="Developer Access Confirmed",
                description=(
                    "The developer-only command set is operational.\n"
                    "DEV environment enforcement is active."
                ),
                color=COLOR_WARNING,
            )

            await safe_respond(
                interaction,
                embed=embed,
                ephemeral=True,
            )

        except Exception as error:
            await handle_interaction_error(interaction, error)

    # ========================================================
    # /dev_error
    # ========================================================

    @app_commands.command(
        name="dev_error",
        description="Trigger a simulated error (DEV ONLY)",
    )
    @app_commands.describe(
        error_type="Type of error to simulate",
    )
    @app_commands.choices(
        error_type=[
            app_commands.Choice(name="ZeroDivisionError", value="zero"),
            app_commands.Choice(name="AttributeError", value="attribute"),
            app_commands.Choice(name="RuntimeError", value="runtime"),
            app_commands.Choice(name="PermissionError", value="permission"),
        ]
    )
    async def dev_error(
        self,
        interaction: discord.Interaction,
        error_type: app_commands.Choice[str],
    ) -> None:
        """
        Intentionally raises different exception types.

        Design principles:
        - NO try/except around the raised exception
        - The exception MUST propagate to the global error handler
        - Used to validate logging, reporting and user-facing UX

        This command is a critical testing tool for the template.
        """

        if not self._is_authorized(interaction):
            await safe_respond(
                interaction,
                content="Developer access denied.",
                ephemeral=True,
            )
            return

        # ----------------------------------------------------
        # Simulated failures
        # ----------------------------------------------------

        if error_type.value == "zero":
            1 / 0

        elif error_type.value == "attribute":
            obj = None
            obj.non_existent_attribute  # noqa

        elif error_type.value == "runtime":
            raise RuntimeError("Simulated runtime error")

        elif error_type.value == "permission":
            raise PermissionError("Simulated permission error")

        # This line should never be reached
        await safe_respond(
            interaction,
            content="Error simulation did not execute as expected.",
            ephemeral=True,
        )
