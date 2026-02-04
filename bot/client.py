import logging
import discord
from discord.ext import commands

from bot.config import INTENTS
from bot.settings import Settings
from bot.utils.global_error_handler import global_app_command_error_handler

LOGGER = logging.getLogger(__name__)

# ============================================================
# Core Discord Client
# ============================================================

class BotClient(commands.Bot):
    """
    Core Discord bot client.

    Responsibilities:
    - Manage Discord connection lifecycle
    - Register cogs (features)
    - Synchronize slash commands
    - Attach global error handlers

    Design principles:
    - No business logic
    - No per-server state management
    - Acts as orchestration layer only
    """

    def __init__(self) -> None:
        """
        Initializes the Discord bot client.

        Notes:
        - Slash-command-only by default (no prefix commands)
        - Intents are configured centrally in config.py
        """

        super().__init__(
            command_prefix=None,
            intents=INTENTS,
        )

    # ========================================================
    # Discord Lifecycle Hooks
    # ========================================================

    async def setup_hook(self) -> None:
        """
        Executed once before the bot becomes ready.

        Used for:
        - Registering cogs
        - Synchronizing application commands
        - Attaching global error handlers

        This method is guaranteed to run before on_ready().
        """

        # ----------------------------------------------------
        # Register cogs
        # ----------------------------------------------------
        # Import locally to avoid circular imports

        from bot.cogs.core import CoreCog

        await self.add_cog(CoreCog(self))

        if Settings.IS_DEV:
            from bot.cogs.dev import DevCog

            await self.add_cog(DevCog(self))

        # ----------------------------------------------------
        # Slash command synchronization
        # ----------------------------------------------------

        if Settings.IS_DEV:
            """
            DEV MODE:
            - Commands are synced to a single test guild
            - Faster iteration (instant updates)
            """

            if not Settings.DEVELOPER_GUILD_ID:
                raise RuntimeError(
                    "DEVELOPER_GUILD_ID must be set when running in DEV mode."
                )

            guild = discord.Object(id=Settings.DEVELOPER_GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

            LOGGER.info(
                f"[DEV] Slash commands synced to guild {Settings.DEVELOPER_GUILD_ID}"
            )

        else:
            """
            PROD MODE:
            - Commands are synced globally
            - Updates may take up to ~1 hour to propagate
            """

            await self.tree.sync()
            LOGGER.info(
                "[PROD] Slash commands synced globally"
            )

        # ----------------------------------------------------
        # Global error handler
        # ----------------------------------------------------

        self.tree.on_error = global_app_command_error_handler
        LOGGER.info(
            "Global application command error handler attached"
        )

    async def on_ready(self) -> None:
        """
        Fired when the bot is fully connected and ready.

        At this stage:
        - Bot user is available
        - All guilds are cached
        """

        LOGGER.info(
            "Connected as %s (ID: %s)",
            self.user,
            self.user.id,
        )

    async def on_guild_join(self, guild: discord.Guild) -> None:
        """
        Fired when the bot joins a new guild.

        This hook is intentionally minimal and safe.
        """

        LOGGER.info(
            "Joined guild: %s (%s)",
            guild.name,
            guild.id,
        )

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        """
        Fired when the bot is removed from a guild.
        """

        LOGGER.info(
            "Removed from guild: %s (%s)",
            guild.name,
            guild.id,
        )
