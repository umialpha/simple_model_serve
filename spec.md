# Simple Model Serve Spec

## Architecture

### RESTful API

- Entrypoint: app/main.py
- Multi-version Router: app/router_v1beta1.py

### Model Inference Runtime

- app/models.py: Model inference is implemented using the PyTorch native method.

Notes:
1. Enabling `model.eval()` and `torch.inference_mode()` can accelerate the inference process.
2. There are various model inference runtimes available, such as PyTorch native, Triton Serve, TorchServe, and ONNX Runtime. Due to the absence of context, the first version opts for the simplest form, which is PyTorch native.

### Observability

- Basic observability has been implemented.
    1. Prometheus middleware measures latency for all API requests.
    2. Records the time taken for core functions.
    3. Tracks model metrics; for simplemodel, it is assumed that the output is accuracy, hence the metric "acc_simplemodel" is monitored.
visit `localhost:8088/metrics` to see more.

### OpenAPI

- OpenAPI can be accessed via `localhost:8088/docs` for testing and trial purposes.


### Rolling Update

Assuming we need to upgrade to the image `simplemodel:dev`

1. Canary update requires running `make run-ha`

2. Open the `manifests/dynamic-traefik.yaml` file
Set `http.services.simple-model.weighted.services[1].weight` to `0`,
as shown in the following yaml
```yaml
http:
  routers:
    my-router:
      rule: "PathPrefix(`/`)"
      service: simple-model
  services:
    simple-model:
      weighted:
        services:
          - name: simple-model-v1@docker
            weight: 50
          - name: simple-model-v2@docker
            weight: 0 # set 0 to upgrade simple-model-v2
```
3. Open `manifests/docker-compose.yaml`, 
Set `simple-model-v2.image` to `simplemodel:dev`

4. Execute 
```bash
docker compose -f manifests/docker-compose.yaml pull
docker compose -f manifests/docker-compose.yaml up -d
```

5. Open `manifests/dynamic-traefik.yaml`
Set `http.services.simple-model.weighted.services[1].weight` to `50`
Set `http.services.simple-model.weighted.services[0].weight` to `0`

6. Open `manifests/docker-compose.yaml`
Set `simple-model-v1.image` to `simplemodel:dev`

7. Open `manifests/dynamic-traefik.yaml`
Set `http.services.simple-model.weighted.services[0].weight` to `50`

### Additional Optimizations

1. Dockerfile

    Copy the `requirements.txt` and install requirements before other files, as code modifications occur more frequently than dependency installations.

2. The gunicorn `preload` parameter is used to prevent the model from being loaded multiple times.