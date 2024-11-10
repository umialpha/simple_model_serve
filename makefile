# Makefile

IMAGE_NAME := simplemodel
TAG := latest

.PHONY: build
build:
	docker build -t $(IMAGE_NAME):$(TAG) . -f manifests/Dockerfile

.PHONY: run-gpu
run-gpu:
	docker run -d -p 8088:8088 --gpus all $(IMAGE_NAME):$(TAG)

.PHONY: run-cpu
	docker run -d -p 8088:8088 $(IMAGE_NAME):$(TAG)
.PHONY: test
test:
	pytest app/tests

.PHONY: run-ha
run-ha:
	docker compose -f manifests/docker-compose.yaml up -d