from enum import Enum

from pydantic import BaseModel

from models.common import IDModelMixin, DateTimeModelMixin

class CategoryType(str, Enum):
    TESTING_TASK = "testing_task"
    PRODUCT_REQUEST = "product_request"
    REFACTOR = "refactor"
    DEV_TASK = "development_task"
    DESIGN_REQUEST = "design_request"
    MISC = "miscellaneous"

class Task(IDModelMixin, DateTimeModelMixin):
    is_complete: bool
    description: str
    category: CategoryType