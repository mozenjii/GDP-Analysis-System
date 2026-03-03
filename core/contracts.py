from typing import Protocol, List, Any, runtime_checkable

@runtime_checkable
class DataSink(Protocol):
    """
    Outbound Abstraction.
    Core calls this to send processed results.
    """
    def write(self, records: dict) -> None:
        ...


@runtime_checkable
class PipelineService(Protocol):
    """
    Inbound Abstraction.
    Input plugins call this to send raw data into the Core.
    """
    def execute(self, raw_data: List[Any]) -> None:
        ...