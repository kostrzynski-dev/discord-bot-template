import logging
from typing import Optional
from bot.settings import Settings


# ============================================================
# Logging Configuration
# ============================================================

"""
This module is responsible for configuring Python's logging
infrastructure for the application.

It defines:
- Global log levels
- Default handlers
- Log formatting rules

IMPORTANT DISTINCTION:
- This file CONFIGURES logging
- logger.py USES logging

Users are encouraged to extend this file to:
- Add file-based logging
- Integrate external services (Sentry, Datadog, etc.)
- Customize formats per environment
"""


# ============================================================
# Public API
# ============================================================

def configure_logging(
    *,
    level: Optional[int] = None,
) -> None:
    """
    Configures the global logging system.

    This function SHOULD be called once at application startup
    (typically from main.py).

    Args:
        level:
            Optional explicit log level.
            If not provided, the level is determined automatically
            based on the current environment.
    """

    # --------------------------------------------------------
    # Resolve log level
    # --------------------------------------------------------

    if level is not None:
        log_level = level
    else:
        # Default behavior based on environment
        log_level = logging.DEBUG if Settings.IS_DEV else logging.INFO

    # --------------------------------------------------------
    # Root logger configuration
    # --------------------------------------------------------

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Prevent duplicate handlers when reloading in DEV
    if root_logger.handlers:
        return

    # --------------------------------------------------------
    # Console handler (default)
    # --------------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # --------------------------------------------------------
    # Log format
    # --------------------------------------------------------

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # --------------------------------------------------------
    # Optional: quiet down noisy third-party loggers
    # --------------------------------------------------------

    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.getLogger("discord.http").setLevel(logging.WARNING)

    # --------------------------------------------------------
    # Startup confirmation (DEV only)
    # --------------------------------------------------------

    if Settings.IS_DEV:
        root_logger.debug("Logging configured in DEV mode")


# ============================================================
# Extension Notes (for users of the template)
# ============================================================

"""
EXTENDING THIS MODULE:

Common extensions include:

1. File logging:
   - Add logging.FileHandler
   - Useful for production diagnostics

2. JSON logging:
   - Replace Formatter with structured JSON output
   - Ideal for log aggregation platforms

3. External services:
   - Forward logs to Sentry, Datadog, Logstash, etc.

This module is intentionally minimal and safe by default.
"""
