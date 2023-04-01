from pydantic import BaseModel, Field
from typing import List, Union


# BASE MODELS
###################################################
class AI_input_1(BaseModel):
    """
    Base AI Model
    """

    model: str = Field(default="julie", title="Default_1", max_length=20)
    limit: int = Field(default=5, gt=0, description="Default_2")
    similar: bool = Field(default=1, description="Default_3")


class DefaultGeom(BaseModel):
    fid: str = Field(default="x", title="Default_1")
    aminity: str = Field(default="x", title="Default_2")
    lat: float = Field(default=0.0, title="Default_3")
    lon: float = Field(default=0.0, title="Default_4")
    addressline: str = Field(default="x", title="Default_5")
    type: str = Field(default="x", title="Default_6")
    info: str = Field(default="{'x':'a'}", title="Default_7")
