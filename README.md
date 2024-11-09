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
