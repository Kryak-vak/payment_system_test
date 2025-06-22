from typing import TypeVar

from django.db.models import Model
from pydantic import BaseModel

ModelType = TypeVar('ModelType', bound=Model)
DTOType = TypeVar('DTOType', bound=BaseModel)