#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from starlette_prometheus import metrics, PrometheusMiddleware

from .models import init_models
from . import router_v1beta1 


# @asynccontextmanager
# async def init_predictor(app):
#     """
#     Initialize models
#     """
    
#     yield

# Wrap app in a function in order to initialize models once once for multiple workers
# https://github.com/fastapi/fastapi/issues/2425#issuecomment-734790381
# Only works with gunicorn server
def init_app():
    
    init_models()

    return  FastAPI(
    title="ML Model",
    description="Simple HTTP API for ML Model",
    version="0.0.1",
    
    )

# Initialize API Server
app = init_app()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)
app.include_router(router_v1beta1.router, prefix="/v1alpha1")

if __name__ == '__main__':
    # server api
    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                reload=True, 
                )