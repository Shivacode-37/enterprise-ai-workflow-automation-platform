from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssetBase(BaseModel):
    asset_type: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=100)
    serial_number: str = Field(..., min_length=2, max_length=100)
    location: str | None = Field(None, max_length=100)


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    asset_type: str | None = Field(None, min_length=2, max_length=50)
    name: str | None = Field(None, min_length=2, max_length=100)
    serial_number: str | None = Field(None, min_length=2, max_length=100)
    status: str | None = Field(None, min_length=2, max_length=50)
    location: str | None = Field(None, max_length=100)


class AssetResponse(AssetBase):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
