import uuid
from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Dict, Any


# ============================================================
# Error Severity Classification
# ============================================================

class ErrorSeverity(str, Enum):
    """
    Represents the severity level of an internal application error.

    This enum is intentionally simple but extensible.
    """

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ============================================================
# Error Source Classification
# ============================================================

class ErrorSource(str, Enum):
    """
    Describes where the error originated from.

    This helps distinguish between:
    - user-triggered failures
    - background task failures
    - system-level issues
    """

    COMMAND = "COMMAND"
    EVENT = "EVENT"
    TASK = "TASK"
    SYSTEM = "SYSTEM"
    UNKNOWN = "UNKNOWN"


# ============================================================
# Error Context (Immutable Data Object)
# ============================================================

@dataclass(frozen=True)
class ErrorContext:
    """
    Immutable data container representing a single runtime error.

    Purpose:
    - Transport structured error data between handlers, loggers and reporters
    - Provide a unified, extensible error format
    - Act as a stable contract between system layers

    Design principles:
    - NO business logic
    - NO side effects
    - PURE data object
    """

    # ========================================================
    # Core Metadata
    # ========================================================

    #: Unique identifier for this error occurrence
    error_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    #: Timestamp when the error occurred (UTC, timezone-aware)
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    #: Severity level of the error
    severity: ErrorSeverity = ErrorSeverity.ERROR

    #: Source of the error
    source: ErrorSource = ErrorSource.UNKNOWN

    # ========================================================
    # Execution Context
    # ========================================================

    #: Slash command name (if applicable)
    command_name: str | None = None

    #: Discord guild identifier
    guild_id: int | None = None

    #: Discord user identifier
    user_id: int | None = None

    # ========================================================
    # Exception Details
    # ========================================================

    #: Exception class name
    exception_type: str | None = None

    #: Exception message
    exception_message: str | None = None

    #: Full traceback (string, optional)
    traceback: str | None = None

    # ========================================================
    # Extension Metadata (Forward Compatibility)
    # ========================================================

    #: Arbitrary extra metadata for future integrations
    metadata: Dict[str, Any] = field(default_factory=dict)
