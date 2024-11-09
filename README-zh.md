# Simple Model Serve

## Prerequisite

1. 安装docker/containerd等容器运行时。
2. 如果节点是GPU机型，安装Nvdia Container Toolkit


## Get Started
1. Build the image
```bash
make build
```
2. Run
```bash
# run a single restful service
make run
```
or

```bash
# run a proxy and two containers for HA and rolling update.
make run-ha
```

[optional] Run tests
```bash
make test
```

## Features

1. 多个fastapi workers接受api请求，但只有一个模型被加载，减少内存/显存使用。
2. HA & Rolling Update. 通过 proxy + many servers的形式实现HA，同时通过proxy的流量权重调整实现金丝雀发布。
3. 可观测性。暴露HTTP请求和模型相关指标，参见 localhost:8088/metrics
4. OpenAPI, 参见 localhost:8088/docs

## Demo
阿里云试一试已经部署好的HA Simple Model Serving.
http://115.29.205.101:8088/docs : simple model openapi.
http://115.29.205.101:8080/ : proxy dashboard.


## 灰度更新
1. 灰度更新要求运行`make run-ha`
2. 打开 `manifests/dynamic-traefik.yaml`文件
设置 `http.services.simple-model.weighted.services[1].weight` to `0`,
如下述yaml
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
          - name:  simple-model-v2@docker
            weight: 0 # set 0 to upgrade simple-model-v2
```
假设我们需要升级到镜像 `simplemodel:dev`
3. 打开 `manifests/docker-compose.yaml`, 
设置 `simple-model-v2.image` 到 `simplemodel:dev`

4. 执行 
```bash
docker compose -f manifests/docker-compose.yaml pull
docker compose -f manifests/docker-compose.yaml up -d
```
5. 打开`manifests/dynamic-traefik.yaml`，修改
设置 `http.services.simple-model.weighted.services[1].weight` to `50`
设置 `http.services.simple-model.weighted.services[0].weight` to `0`

6. 打开 `manifests/docker-compose.yaml`
设置 `simple-model-v1.image` to `simplemodel:dev`

7. 打开`manifests/dynamic-traefik.yaml`
设置 `http.services.simple-model.weighted.services[0].weight` to `50`