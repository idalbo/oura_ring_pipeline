import yaml
import pendulum
import datetime
import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources
from typing import Dict, Any


def _load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML configuration: {e}")


def _set_config(oura_api_key: str, config: Dict[str, Any]) -> RESTAPIConfig:
    """Parse YAML config and convert it to RESTAPIConfig format."""
    yaml_config = config.get("oura_api_config", {})
    base_url = yaml_config.get("client", {}).get("base_url", "")
    base_pagination = yaml_config.get("client", {}).get("paginator", "auto")

    # Validate base_url
    if not base_url:
        raise ValueError("Base URL is missing in the configuration.")

    # Collect enabled resources
    resources = [
        resource["name"]
        for resource in yaml_config.get("resources", [])
        if resource.get("enabled", True)
    ]

    # Default parameters
    default_params = yaml_config.get("resource_defaults", {}).get("endpoint", {}).get("params", {})
    if "start_date" in default_params and isinstance(default_params["start_date"], datetime.date):
        default_params["start_date"] = default_params["start_date"].strftime("%Y-%m-%d")
    if "end_date" not in default_params:
        default_params["end_date"] = pendulum.now().to_date_string()

    # Build RESTAPIConfig
    return {
        "client": {
            "base_url": base_url,
            "auth": {
                "type": "bearer",
                "token": oura_api_key,
            },
            "paginator": base_pagination,
        },
        "resource_defaults": {
            "primary_key": yaml_config.get("resource_defaults", {}).get("primary_key", "id"),
            "write_disposition": yaml_config.get("resource_defaults", {}).get("write_disposition", "merge"),
            "endpoint": {
                "params": default_params
            }
        },
        "resources": resources
    }


@dlt.source
def load_oura_source(oura_api_key: str = dlt.secrets.value, config_path: str = "./.dlt/pipeline_config.yml"):
    """DLT source for Oura Ring data."""
    # Load configuration
    config = _load_config(config_path)

    # Get REST API configuration
    rest_config = _set_config(oura_api_key, config)

    # Yield resources
    yield from rest_api_resources(rest_config)