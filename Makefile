help:
	@echo "Makefile Help"
	@echo ""
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


##############################
#     Container helpers      #
##############################
docker-build:  ## build the docker image
	docker-compose -f docker-compose.yml build --force-rm

docker-start: ## start the docker container
	docker-compose -f docker-compose.yml up -d

docker-stop:  ## stops the running docker service
	docker-compose -f docker-compose.yml down -v

docker-shell:  ## open a terminal session in the container
	docker-compose -f docker-compose.yml run --rm oura_pipeline


##############################
#     		E2E run    	 	 #
##############################
project-run: ## runs project end-to-end
	docker-compose -f docker-compose.yml run --rm oura_pipeline /bin/bash -c "\
	python dlt/rest_api_pipeline.py && \
	sqlmesh -p sqlmesh run"