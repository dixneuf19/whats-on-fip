.PHONY: shell install install-dev dev build run push release release-multi deploy

PACKAGE_NAME=whats_on_fip
DOCKER_REPOSITERY=dixneuf19
IMAGE_NAME=whats-on-fip
IMAGE_TAG=$(shell git rev-parse --short HEAD)
DOCKER_IMAGE_PATH=$(DOCKER_REPOSITERY)/$(IMAGE_NAME):$(IMAGE_TAG)
APP_NAME=whats-on-fip
KUBE_NAMESPACE=fip

# Default target
all: dev

install:
	rye sync --no-dev

install-dev:
	rye sync

install-ci:
	rye sync --no-lock

dev:
	rye run uvicorn ${PACKAGE_NAME}.main:app --reload

format:
	rye run isort .
	rye run black .

check-format:
	rye run isort --check .
	rye run black --check .
	rye run ruff .
	rye run pyright

test:
	rye run pytest --cov=${PACKAGE_NAME} --cov-report=xml tests

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
