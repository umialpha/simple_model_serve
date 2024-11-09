# Makefile

IMAGE_NAME := simplemodel
TAG := latest

.PHONY: build

build:
	docker build -t $(IMAGE_NAME):$(TAG) . -f manifests/Dockerfile

.PHONY: run

run:
	docker run -d --network host $(IMAGE_NAME):$(TAG)