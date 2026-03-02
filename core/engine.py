from typing import List, Any
from .contracts import DataSink, PipelineService


class TransformationEngine(PipelineService):

    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config

    def execute(self, raw_data: List[Any]) -> None:
        """
        This method will:
        1. Clean data
        2. Filter data
        3. Compute analytics
        4. Send results to sink
        """

        # TEMPORARY placeholder
        results = [{"message": "Engine executed successfully"}]

        self.sink.write(results)