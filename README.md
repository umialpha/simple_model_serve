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

- Run in HA mode, with a proxy gateway and 2 backend services using different gpus.
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
2. HA & Rolling Update. Achieve HA through the proxy with multiple backends. Implement canary deployment leveraged by proxy traffic weight adjustment.
3. Observability. Expose HTTP request and model-related metrics, see `localhost:8088/metrics`.
4. OpenAPI, see `localhost:8088/docs`.

## Demo

a `Simple Model Serve` service is already deployed on ACK Serverless

see `http://47.112.99.98:8088/docs`

## [More Specification](./spec.md)
