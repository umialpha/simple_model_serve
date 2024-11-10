# Simple Model Serve

## [Prerequisites](./prerequisites.md) 

1. Install docker or other container runtimes.
2. If the node has gpu, install `Nvidia Container Toolkit`.


## Get Started
1. Build the image
```bash
make build
```
2. Run
- Run a single-point service using gpu
    ```bash
    make run-gpu
    ```
- Run a single-point service using cpu
    ```bash
    make run-cpu
    ```

- Run in HA mode, with a proxy and 2 backend services using different gpus.
    ```bash
    make run-ha
    ```
3. visit `localhost:8088/docs`

[optional] Run tests
```bash
make test
```

## Features

1. Multiple fastapi workers accept API requests, but only one model is loaded, reducing memory/GPU memory usage.
2. HA & Rolling Update. Achieve HA through the proxy and multiple backends. Implement canary deployment by leveraging proxy traffic weight adjustment.
3. Observability. Expose HTTP request and model-related metrics, see `localhost:8088/metrics`.
4. OpenAPI, see `localhost:8088/docs`.

## Demo
Try out the HA Simple Model Serving already deployed on Alibaba Cloud.
`http://115.29.205.101:8088/docs`  : Simple Model Openapi.
`http://115.29.205.101:8080/ ` : Proxy Dashboard.

## [More Specification](./spec.md)
