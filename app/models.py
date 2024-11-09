#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
import torch
from torch import nn

from .instruments import record_acc_simplemodel, time_elapsed


class _SimpleModel(nn.Module):

    INPUT_FEATURES = 2
    OUTPUT_FEATURES = 1
    DTYPE=torch.float32

    def __init__(self):
        super(_SimpleModel, self).__init__()
        self.fc = nn.Linear(_SimpleModel.INPUT_FEATURES, _SimpleModel.OUTPUT_FEATURES)

    def forward(self, x):
        return self.fc(x)


class SimpleModelInput(BaseModel):
    '''
    SimpleModelInput is a pydantic model that defines the input schema for the simple model
    '''
    data: list[list[float]]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": [[1.0, 2.0], [3.0, 4.0]]
                    
                }
            ]
        }
    }

    @field_validator("data")
    @classmethod
    def validate(cls, data):
        if not data:
            raise RequestValidationError("data is required")
        for row in data:
            if len(row) != _SimpleModel.INPUT_FEATURES:
                raise RequestValidationError(f"input shape must be (BATCH_SIZE, {_SimpleModel.INPUT_FEATURES}, invalid row: {row}")
        return data

class SimpleModelOutput(BaseModel):
    '''
    SimpleModelOutput is a pydantic model that defines the output schema for the simple model
    '''
    result: list[list[float]]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "results": [
                                [2.8352279663085938],
                                [6.720881462097168]
                                ]
                }
            ]
        }
    }


class SimpleModel:
    '''
    SimpleModel wraps the SimpleModel(torch.nn.Module) and provides methods for preprocessing, postprocessing and prediction
    '''
    def __init__(self, model_name:str="simple_model"):
        self.model_name = model_name
        self._model = _SimpleModel()
        
    def init(self):
        '''
        init inits model with pretrained weights
        '''
        import os
        model_path = os.path.dirname(os.path.dirname(__file__))+ "/artifacts/simple_model.pth"
        print("load simplemodel", model_path)
        self._model.load_state_dict(torch.load(model_path))
        if torch.cuda.is_available():
            self._model.to("cuda")
        # set model to evaluation mode
        self._model.eval()
    
    def preprocess(self, input: SimpleModelInput):
        '''
        preprocess converts input to torch tensor
        '''
        return torch.tensor(input.data)
    
    def postprocess(self, output):
        '''
        postprocess converts model output to SimpleModelOutput
        '''
        for acc in output:
            record_acc_simplemodel(acc[0])
        return SimpleModelOutput(result=output)
    
    @time_elapsed
    def predict(self, input: SimpleModelInput):
        '''
        predict performs prediction on input.
        it is thread safe.
        '''
        data = self.preprocess(input)
        with torch.inference_mode():
            score = self._model(data).cpu().tolist()
            return self.postprocess(score)

    

class ModelZoo:
    '''
    ModelZoo is a singleton class that holds all the models.
    Currently, it holds only SimpleModel
    N.B. Models are lock free. Do not change them!
    '''
    Simple :SimpleModel= None

def init_models():
    '''
    init_models initializes all the models, do it only once.
    '''
    simple_model = SimpleModel()
    simple_model.init()
    ModelZoo.Simple = simple_model