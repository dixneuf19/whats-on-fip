.PHONY: install install-dev dev build run push release release-multi deploy

DOCKER_REPOSITERY=dixneuf19
IMAGE_NAME=whatsonfip
IMAGE_TAG=$(shell git rev-parse --short HEAD)
DOCKER_IMAGE_PATH=$(DOCKER_REPOSITERY)/$(IMAGE_NAME):$(IMAGE_TAG)
APP_NAME=whats-on-fip
KUBE_NAMESPACE=fip

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt

dev:
	uvicorn whatsonfip.main:app --reload

format:
	isort --profile black .
	black .

check-format:
	isort --profile black --check .
	black --check .

test:
	PYTHONPATH=. pytest tests

build:
	docker build -t $(DOCKER_IMAGE_PATH) .

build-multi:
	docker buildx build --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7 -t $(DOCKER_IMAGE_PATH) .


run: build
	docker run -p 8000:80 --env-file=.env $(DOCKER_IMAGE_PATH)

push:
	docker push $(DOCKER_IMAGE_PATH)

release: build push

release-multi:
	docker buildx build --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7 -t $(DOCKER_IMAGE_PATH) . --push

deploy:
	kubectl apply -f $(APP_NAME).yaml

secret:
	kubectl create secret generic radio-france-api-token --from-env-file=.env

kube-credentials:
	NAMESPACE=${KUBE_NAMESPACE} ./scripts/generate-kubeconfig.sh
