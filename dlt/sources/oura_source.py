import yaml
import pendulum
import dlt
from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_resources,
)
from typing import Dict, Any

class OuraSource:

    def __init__(self, config):
        self.config = config

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def _set_config(self, oura_api_key):
        """Parse YAML config and convert to RESTAPIConfig format"""
        yaml_config = self.config['oura_api_config']
 
        base_url = yaml_config['client']['base_url']
        
        resources = []
        for resource in yaml_config['resources']:
            if resource.get('enabled', True):
                resources.append(resource['name'])

        default_params = yaml_config['resource_defaults']['endpoint']['params']

        if 'end_date' not in default_params:
            default_params['end_date'] = pendulum.now().to_date_string()

        rest_config: RESTAPIConfig = {
            "client": {
                "base_url": base_url,
                "auth": {
                    "type": "bearer",
                    "token": oura_api_key,
                }
            },
            "resource_defaults": {
                "primary_key": yaml_config['resource_defaults'].get('primary_key', 'id'),
                "write_disposition": yaml_config['resource_defaults'].get('write_disposition', 'merge'),
                "endpoint": {
                    "params": default_params
                }
            },
            "resources": resources
        }
        
        return rest_config
    
    def oura_source(self, oura_api_key=dlt.secrets.value):
        """DLT source for Oura Ring data"""
               
        # Get REST API configuration
        config = self._set_config(oura_api_key)
        
        # Yield resources
        yield from rest_api_resources(config)



        