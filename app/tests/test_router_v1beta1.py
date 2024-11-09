#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi.exceptions import RequestValidationError
import pytest
from fastapi.testclient import TestClient

from ..router_v1beta1 import router
from ..models import init_models

@pytest.fixture
def client():
    with TestClient(router) as c:
        yield c

def test_simple_model_predict(client):
    init_models()

    # test with valid input
    response = client.post("/simple_model/predict", json={"data": [[1.0, 2.0], [3.0, 4.0]]})
    assert response.status_code == 200
    assert len(response.json()["result"]) == 2

    # test with invalid input
    try:
        response = client.post("/simple_model/predict", json={"data": [[1.0, 2.0], [3.0]]})
    except Exception as e:
        assert isinstance(e, RequestValidationError)

