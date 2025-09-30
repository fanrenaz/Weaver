"""Custom exception hierarchy for Weaver framework.

Having a dedicated exception layer allows higher application levels
and integrators to distinguish between configuration issues, policy
formatting problems, runtime orchestration failures and tool execution
errors. Keep the hierarchy shallow for now; expand in future phases
when adding persistence, network IO, etc.
"""

from __future__ import annotations


class WeaverError(Exception):
    """Base class for all custom Weaver exceptions."""


class ConfigurationError(WeaverError):
    """Raised when environment / model configuration is invalid."""


class PolicyError(WeaverError):
    """Raised for policy formatting or validation problems."""


class RuntimeInvocationError(WeaverError):
    """Raised when the core chain / graph invocation fails unexpectedly."""


class ToolExecutionError(WeaverError):
    """Raised when an underlying tool raises an exception."""


__all__ = [
    "WeaverError",
    "ConfigurationError",
    "PolicyError",
    "RuntimeInvocationError",
    "ToolExecutionError",
]
