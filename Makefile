#!make

# ENV VARIABLES IMPORT
include .env

DOCKER_IMG=${ART_LOCATION}-docker.pkg.dev/${GCP_PRJ_ID}/${ART_REPO}/${ART_IMG}



# ----------------------------------
# Google Cloud Platform
# ----------------------------------

gcloud_config_activate:
	@echo "ACTIVATING GCLOUD CONFIGURATION..."
	@gcloud config configurations activate ${GCP_CONFIG}


gcloud_run_deploy: gcloud_config_activate
	@gcloud run deploy --image ${DOCKER_IMG} --allow-unauthenticated



# ----------------------------------
#     DOCKER
# ----------------------------------

docker_config:
	@echo "CONFIGURING DOCKER..."
	@gcloud auth configure-docker ${ART_LOCATION}-docker.pkg.dev

docker_build:
	@docker build -t ${DOCKER_IMG} .

docker_run_local:
	@docker run -p 6501:6501 --rm -e PORT=6501 ${DOCKER_IMG}

docker_push:
	@docker push ${DOCKER_IMG}
