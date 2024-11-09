#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException
from fastapi.logger import logger


from .models import ModelZoo,SimpleModelInput,SimpleModelOutput,init_models

router = APIRouter()

SIMPLE_MODEL_DESC = f'''
simple model is a linear model with 2 input features and 1 output feature.
It takes a list of list of float as input, and return a list of float as output,
'''

@router.post('/simple_model/predict', 
          description=SIMPLE_MODEL_DESC,
          response_model=SimpleModelOutput,
          )
def predict(input: SimpleModelInput) -> SimpleModelOutput:
    """
    Perform prediction on input data
    """

    logger.info(f'API predict called , {input}')
    if not ModelZoo.Simple:
        raise HTTPException(status_code=500, detail=f"SimpleModel not loaded")
    output = ModelZoo.Simple.predict(input)
    return output
