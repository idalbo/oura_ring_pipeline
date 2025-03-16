# How to run 

1. in your local `.dlt` folder add a `secrets.toml` file and add the variables indicated in the `secrets.toml.example` file
2. go to the (oura dev website)[https://cloud.ouraring.com/personal-access-tokens] and create a personal access token, copy it, and palce it in the `secrets.toml` file
3. open a terminal and run `docker-compose up -d` (if you get an error, first build the image with `docker-compose build`)
3. enter the container shell by running `docker-compose exec oura_pipeline bash`
5. run the python script to load the data in your local duckdb instance with `python rest_api_pipeline.py` from the docker shell
6. once you are done, exit the container and run `docker-compose down`

The data you downloaded should be available within the `data` folder!