from pydantic import BaseModel, Field
from typing import List, Union



class InnerObject(BaseModel):
    lat: float
    lon : float

class OuterObject(BaseModel):
    bar: List[InnerObject]
# BASE MODELS
###################################################
class AI_input_1(BaseModel):
    """
    Base AI Model
    """
    points : List[InnerObject] = Field()


class DefaultGeom(BaseModel):
    fid: str = Field(default="x", title="Default_1")
    aminity: str = Field(default="x", title="Default_2")
    lat: float = Field(default=0.0, title="Default_3")
    lon: float = Field(default=0.0, title="Default_4")
    addressline: str = Field(default="x", title="Default_5")
    type: str = Field(default="x", title="Default_6")
    info: str = Field(default="{'x':'a'}", title="Default_7")
