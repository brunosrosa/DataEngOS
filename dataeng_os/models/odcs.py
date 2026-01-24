from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, EmailStr

class Owner(BaseModel):
    team: str
    email: EmailStr

class Column(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    primary_key: bool = False
    pii: bool = False
    tags: List[str] = []

class SchemaConfig(BaseModel):
    additional_properties: bool = False

class Schema(BaseModel):
    config: Optional[SchemaConfig] = None
    columns: List[Column]

class QualityRule(BaseModel):
    type: str
    columns: Optional[List[str]] = None
    query: Optional[str] = None
    level: str = "error"

class SLA(BaseModel):
    frequency: str
    freshness: str

class DatasetMeta(BaseModel):
    project_code: Optional[str] = None
    cost_center: Optional[str] = None
    data_classification: Optional[str] = None
    regulatory_scope: List[str] = []

class Dataset(BaseModel):
    domain: str
    logical_name: str
    physical_name: str
    description: str
    owners: List[Owner]
    meta: Optional[DatasetMeta] = None

class DataContractSpec(BaseModel):
    dataset: Dataset
    schema_def: Schema = Field(alias="schema")
    quality: List[QualityRule] = []
    slas: Optional[SLA] = None

class DataContract(BaseModel):
    kind: str = "DataContract"
    version: str
    spec: DataContractSpec
