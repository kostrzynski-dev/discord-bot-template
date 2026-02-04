import os
from dotenv import load_dotenv

# ============================================================
# Environment & Runtime Configuration
# ============================================================

"""
This module defines the central runtime configuration
for the Discord Bot Template.

Design goals:
- Single source of truth for environment configuration
- Clear separation between DEV and PROD behavior
- Safe defaults for new users
- Easy extensibility without modifying core logic

IMPORTANT:
- This file contains NO business logic
- This file does NOT interact with Discord API
"""

load_dotenv()

def _parse_id_list(raw_value: str) -> list[int]:
    """
    Parses a comma-separated list of numeric IDs.

    Raises:
        ValueError: If any entry is not a valid integer.
    """
    if not raw_value:
        return []

    ids: list[int] = []
    for raw_id in raw_value.split(","):
        value = raw_id.strip()
        if not value:
            continue
        if not value.isdigit():
            raise ValueError(
                "DEVELOPER_IDS must be a comma-separated list of integers."
            )
        ids.append(int(value))
    return ids

class Settings:
    """
    Centralized runtime configuration container.

    Responsibilities:
    - Load environment variables
    - Expose environment flags (DEV / PROD)
    - Provide infrastructure-level constants
    - Validate critical configuration at startup

    This class is intentionally static and declarative.
    """

    # ========================================================
    # Environment Mode
    # ========================================================

    #: Application runtime environment ("dev" or "prod")
    ENV: str = os.getenv("APP_ENV", "dev").lower()

    #: Development mode flag
    IS_DEV: bool = ENV == "dev"

    #: Production mode flag
    IS_PROD: bool = ENV == "prod"

    # ========================================================
    # Discord Application
    # ========================================================

    #: Discord bot token (REQUIRED)
    DISCORD_TOKEN: str = (
            os.getenv("DISCORD_TOKEN")
            or os.getenv("DISCORD_BOT_TOKEN", "")
    )

    # ========================================================
    # Development Configuration
    # ========================================================

    #: Discord guild ID used for slash command sync in DEV mode
    DEVELOPER_GUILD_ID: int = int(
        os.getenv("DEVELOPER_GUILD_ID", "0")
    )

    #: Discord user IDs with developer access (optional)
    DEVELOPER_IDS: list[int] = _parse_id_list(
        os.getenv("DEVELOPER_IDS", "")
    )

    # ========================================================
    # System Channels (Optional)
    # ========================================================

    #: Channel ID for system-level error reports (optional)
    SYSTEM_ERROR_CHANNEL_ID: int = int(
        os.getenv("SYSTEM_ERROR_CHANNEL_ID", "0")
    )

    # ========================================================
    # Logging & Debugging
    # ========================================================

    #: Enable verbose debug logging (DEV only)
    DEBUG_LOGGING: bool = IS_DEV

    # ========================================================
    # Validation
    # ========================================================

    @classmethod
    def validate(cls) -> None:
        """
        Validates critical runtime configuration.

        This method SHOULD be called once during application startup.

        Raises:
            ValueError: If required configuration is missing or invalid
        """

        # ----------------------------------------------------
        # Environment validation
        # ----------------------------------------------------

        if cls.ENV not in ("dev", "prod"):
            raise ValueError(
                f"Invalid APP_ENV value: '{cls.ENV}'. "
                "Expected 'dev' or 'prod'."
            )

        # ----------------------------------------------------
        # Token validation
        # ----------------------------------------------------

        if not cls.DISCORD_TOKEN:
            raise ValueError(
                "DISCORD_TOKEN (or DISCORD_BOT_TOKEN) is not set. "
                "Please provide a valid bot token in the environment."
            )

        # ----------------------------------------------------
        # DEV-specific validation
        # ----------------------------------------------------

        if cls.IS_DEV and cls.DEVELOPER_GUILD_ID <= 0:
            raise ValueError(
                "DEVELOPER_GUILD_ID must be set when running in DEV mode."
            )
