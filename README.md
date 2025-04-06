## Project

This project is under development and will be updated from time to time to add more datasets and functionalities, as for example:
* orchestration
* modularization of dlt pipeline with more endpoints parsed
* transformation capabilities with dbt
* visualization/frontend

## How to run 

1. in your local `.dlt` folder add a `secrets.toml` file and add the variables indicated in the `secrets.toml.example` file
2. go to the [oura dev website](https://cloud.ouraring.com/personal-access-tokens) and create a personal access token, copy it, and palce it in the `secrets.toml` file
3. run `make docker-build` to build the image if you haven't
4. run `make docker-start` to spin up the container 
5. run `make docker-shell` to enter the interactive shell of the container and issue commands from there
5. run the python script to load the data in your local duckdb instance with `python dltrest_api_pipeline.py` from the docker shell
6. once you are done, exit the container and run `make docker-stop` to spin down the container

The data you downloaded should be available within the `data` folder!

## Apache superset

Once the container is up, you can access your DuckDB data at localhost:8088 through [apache superset](https://superset.apache.org/). The local database should be correctly mounted to the container and superset should be able to access it. Feel free to create charts and dashboards that can be persisted in your local superset db instance (if you run the project successfully, you should see a `test_chart` and `test_dashboard` being populated).