from typing import Any, Protocol


class Processor(Protocol):
    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Process a validated generic payload."""


class MockProcessor:
    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "processor": "mock",
            "message": "Mock processing completed",
        }
