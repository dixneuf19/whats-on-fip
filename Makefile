.PHONY: shell install install-dev dev build run push release release-multi deploy

PACKAGE_NAME=whats_on_fip
DOCKER_REPOSITORY=dixneuf19
IMAGE_NAME=whats-on-fip
IMAGE_TAG=$(shell git rev-parse --short HEAD)
DOCKER_IMAGE_PATH=$(DOCKER_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_TAG)
APP_NAME=whats-on-fip
KUBE_NAMESPACE=fip

# Default target
all: dev

install:
	uv sync --no-dev

install-dev:
	uv sync

install-ci:
	uv sync --frozen

dev:
	uv run uvicorn ${PACKAGE_NAME}.main:app --reload

format:
	uv run ruff format .
	uv run ruff check --fix .

check-format:
	uv run ruff format --check .
	uv run ruff check .
	uv run ty check

test:
	uv run pytest --cov=${PACKAGE_NAME} --cov-report=xml tests

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
