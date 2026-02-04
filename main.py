import sys
import logging

from bot.client import BotClient
from bot.settings import Settings
from bot.logging_config import configure_logging


# ============================================================
# Application Entry Point
# ============================================================

"""
This file is the main entry point of the Discord Bot Template.

Responsibilities:
- Configure application-wide logging
- Validate runtime environment configuration
- Initialize the Discord bot client
- Start the Discord connection
- Handle fatal startup errors gracefully

Design principles:
- Minimal and explicit startup flow
- No business logic
- No Discord-specific implementation details
- Predictable behavior and fail-fast validation
"""


# ============================================================
# Bootstrap Helpers
# ============================================================

def _validate_environment() -> None:
    """
    Validates critical environment configuration before startup.

    This prevents undefined behavior later in the application lifecycle
    by ensuring all required settings are present and valid.
    """

    try:
        Settings.validate()
    except Exception as exc:
        logging.critical("Startup configuration validation failed.")
        logging.critical(str(exc))
        sys.exit(1)


# ============================================================
# Main Execution
# ============================================================

def main() -> None:
    """
    Application bootstrap sequence.

    Execution order:
    1. Configure global logging infrastructure
    2. Validate environment configuration
    3. Initialize the bot client
    4. Start the Discord connection
    """

    # --------------------------------------------------------
    # Logging configuration
    # --------------------------------------------------------

    configure_logging()

    logging.info("Starting Discord Bot Template...")

    # --------------------------------------------------------
    # Environment validation
    # --------------------------------------------------------

    _validate_environment()

    # --------------------------------------------------------
    # Bot startup
    # --------------------------------------------------------

    try:
        bot = BotClient()
        bot.run(Settings.DISCORD_TOKEN)

    except KeyboardInterrupt:
        logging.info("Shutdown requested by user (KeyboardInterrupt).")

    except Exception as exc:
        logging.critical("Fatal error during bot startup.")
        logging.critical(str(exc))
        sys.exit(1)


# ============================================================
# Script Guard
# ============================================================

if __name__ == "__main__":
    main()
