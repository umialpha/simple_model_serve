# Simple Model Serve

## Prerequisite

为了运行在容器环境。必须首先安装docker/containerd等容器运行时。
如果节点是GPU机型，还需要安装Nvdia Container Toolkit

## Architecture

### RESTFUL API

fastapi作为api层，定义端口、输入、输出、负责做validation等工作。
为了扩展不同版本的api，因此将代码放入 app/router_v1beta1.py

### 模型推理runtime
有许多方式实现模型推理层，例如 pytorch native，triton serve， torchserve， onnx runtime，
对模型的保存方式也有多种，例如.pth，torchscript, 转换成onnx格式。
由于没有任何的上下文，第一版本选择最简单的形式，即pytorch native。

### observability
实现了简单的可观测。
1. promthues middleware, 对所有的api请求做 latency和
2. 对核心函数记录耗时。
3. 统计对模型指标，对于simplemodel，我假设输出是正确率，因此统计了"acc_simplemodel"

### OpenAPI
通过`localhost:${PORT}/docs`可以访问OpenAPI，用以测试和试用。


## How to Build the Image

To build the Docker image, run the following command in the root directory of the project:

```sh

make build
```

## How to Run it on Docker

To run the Docker container, use the following command:

```sh
make run
```

## 如何保证7x24，并支持模型更新
我们需要分情况讨论：
1. 有k8s环境：

保证7x24: 
采用deployment部署形式。

模型更新：
采用deployment rollingupdate的形式进行滚动更新，确保服务稳定性。
如果需要基于流量控制的更新形式，例如金丝雀发布、蓝绿发布等，需要集群支持服务网格，例如istio、traefik等。

2. 没有k8s环境：

7x24：如果是单机情况，很难做到7x24
模型更新：
利用开源reverse proxy: traefik[https://traefik.io/traefik/]作为gateway，
通过路由转发到后端。

traefik: expose 8080  ----100%----> primary version v0
                      |------0%----> canery version v0

when rolling update:

1. traefik: expose 8080  -----90%----> primary version v0
                        |-----10%----> canery version v1


如果一切指标正常，则继续修改流量
traefik: expose 8080  -----80%----> primary version v0
                        |-----20%----> canery version v1
直到 

traefik: expose 8080  -----0%----> primary version v0
                        |-----100%----> canery version v1

```


一些优化的点
1. dockerfile先拷贝requirements.txt
2. 使用gunicorn preload避免多次加载模型。
