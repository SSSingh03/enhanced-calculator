"""
operations.py

Defines arithmetic operation classes for the calculator.

Each operation is implemented as its own class so we can:
- keep logic small and testable
- use polymorphism (all operations share the same interface)
- plug operations into a Factory for clean command handling
"""

from abc import ABC, abstractmethod


class Operation(ABC):
    """Base interface for all calculator operations."""

    name: str  # command name used in the REPL (e.g., "add", "power")

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Perform the operation on two numeric inputs."""
        raise NotImplementedError  # pragma: no cover
    
class Add(Operation):
    """Add two numbers."""

    name = "add"

    def execute(self, a: float, b: float) -> float:
        return a + b
    
 