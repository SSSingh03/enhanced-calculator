"""
operations.py

Defines arithmetic operation classes for the calculator.

Each operation is implemented as its own class so we can:
- keep logic small and testable
- use polymorphism (all operations share the same interface)
- plug operations into a Factory for clean command handling
"""

from abc import ABC, abstractmethod

from app.exceptions import OperationError


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
    
class Subtract(Operation):
    """Subtract second number from first."""

    name = "subtract"

    def execute(self, a: float, b: float) -> float:
        return a - b
    
class Multiply(Operation):
    """Multiply two numbers."""

    name = "multiply"

    def execute(self, a: float, b: float) -> float:
        return a * b
    
class Divide(Operation):
    """Divide first number by second."""

    name = "divide"

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Division by zero is not allowed.")
        return a / b
    
class OperationFactory:
    """
    Factory responsible for creating operation instances
    based on a command name.
    """

    _registry = {
        Add.name: Add,
        Subtract.name: Subtract,
        Multiply.name: Multiply,
        Divide.name: Divide,
    }

    @classmethod
    def create(cls, operation_name: str) -> Operation:
        """
        Create an operation instance by name.

        Raises OperationError if operation is not supported.
        """
        operation_name = operation_name.lower()

        if operation_name not in cls._registry:
            raise OperationError(f"Unsupported operation: '{operation_name}'")

        return cls._registry[operation_name]()