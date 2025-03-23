from typing import Any, Optional
import dlt
from dlt.common.pendulum import pendulum
from sources.oura_source import OuraSource

def load_oura() -> None:
    duckdb_path = "./data/oura.duckdb"

    pipeline = dlt.pipeline(
        pipeline_name="rest_api_oura",
        destination=dlt.destinations.duckdb(duckdb_path),
        dataset_name="oura_ring_data",
    )
    
    oura_source = OuraSource("./dlt/pipeline_config.yml")

    # Run the pipeline with the starting date parameter
    load_info = pipeline.run(oura_source.oura_source())
    print(load_info)

if __name__ == "__main__":
    load_oura()