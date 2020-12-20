from pydantic import BaseModel

from models.common import IDModelMixin, DateTimeModelMixin

class Task(IDModelMixin, DateTimeModelMixin):
    is_complete: bool
    description: str
    category: str # TODO: this will be an enum or a foreign key
