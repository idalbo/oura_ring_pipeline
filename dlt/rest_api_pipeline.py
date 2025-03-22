from typing import Any, Optional
import dlt
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import (
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
    rest_api_source,
)

@dlt.source
def oura_source(oura_api_key=dlt.secrets.value, start_date=None):
    # If no start_date is provided, use a default date
    if start_date is None:
        start_date = "2021-01-01"  # Or any default date you prefer
    
    # Get current date for end_date parameter
    end_date = pendulum.now().to_date_string()
    
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://api.ouraring.com/v2/usercollection/",
            "auth": {
                "type": "bearer",
                "token": oura_api_key,
            }
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
            "endpoint": {
                "params": {
                    "start_date": start_date,
                    "end_date": end_date
                }
            }
        },
        "resources": [
            "sleep"  # Simple string format to define the endpoint
        ],
    }
    yield from rest_api_resources(config)

def load_oura() -> None:
    # Define default start date
    start_date = "2022-02-01"  # Your desired starting date
    duckdb_path = "data/oura_ring_data.duckdb"

    pipeline = dlt.pipeline(
        pipeline_name="rest_api_oura",
        destination=dlt.destinations.duckdb("./data/oura.duckdb"),
        dataset_name="oura_ring_data",
    )
    
    # Run the pipeline with the starting date parameter
    load_info = pipeline.run(oura_source(start_date=start_date))
    print(load_info)

if __name__ == "__main__":
    load_oura()