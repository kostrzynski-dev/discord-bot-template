import logging

from bot.logging.error_context import ErrorContext, ErrorSeverity
from bot.settings import Settings


# ============================================================
# System Logger (Backend / Infrastructure Layer)
# ============================================================

class SystemLogger:
    """
    Centralized backend logger for the application.

    Responsibilities:
    - Log structured ErrorContext objects
    - Control verbosity based on environment (DEV / PROD)
    - Provide a single, consistent logging entry point

    Design principles:
    - NO Discord awareness
    - NO user-facing logic
    - NO business rules
    - Infrastructure-level only
    """

    DEFAULT_LOGGER_NAME = "discord_bot_template"

    def __init__(self, name: str = DEFAULT_LOGGER_NAME) -> None:
        """
        Initializes the system logger.

        Args:
            name:
                Logical logger name used by Python logging subsystem.
                Important for log aggregation and filtering.
        """

        self._logger = logging.getLogger(name)
        self._configure()

    # ========================================================
    # Internal configuration
    # ========================================================

    def _configure(self) -> None:
        """
        Configures logger handlers and formatters.

        This method is intentionally isolated to make extension easy.

        Common extensions:
        - FileHandler (persistent logs)
        - RotatingFileHandler
        - External logging services (Sentry, ELK, Loki, etc.)
        """

        # Prevent duplicate handlers (important in dev reload scenarios)
        if self._logger.handlers:
            return

        # Base logger level
        self._logger.setLevel(logging.INFO)

        # ----------------------------------------------------
        # Console handler (default, always enabled)
        # ----------------------------------------------------

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # ----------------------------------------------------
        # Extension point
        # ----------------------------------------------------
        # Add file handlers or external services here if needed.

    # ========================================================
    # Public API
    # ========================================================

    def log_error(self, context: ErrorContext) -> None:
        """
        Logs an ErrorContext instance.

        Behavior:
        - Always logs structured metadata
        - Severity-aware routing
        - Tracebacks are logged ONLY in DEV environment
        """

        message = (
            f"error_id={context.error_id} "
            f"severity={context.severity.value} "
            f"source={context.source.value} "
            f"command={context.command_name} "
            f"user={context.user_id} "
            f"guild={context.guild_id} "
            f"exception={context.exception_type} "
            f"message={context.exception_message}"
        )

        # ----------------------------------------------------
        # Severity-based routing
        # ----------------------------------------------------

        if context.severity in (ErrorSeverity.CRITICAL, ErrorSeverity.ERROR):
            self._logger.error(message)

        elif context.severity == ErrorSeverity.WARNING:
            self._logger.warning(message)

        else:
            self._logger.info(message)

        # ----------------------------------------------------
        # DEV-only traceback (explicit, never silent)
        # ----------------------------------------------------

        if Settings.IS_DEV and context.traceback:
            self._logger.error("Traceback:")
            self._logger.error(context.traceback)


# ============================================================
# Singleton instance
# ============================================================

# Single shared logger instance used across the application
logger = SystemLogger()
