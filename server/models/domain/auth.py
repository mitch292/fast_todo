from typing import Optional

from models.common import DateTimeModelMixin, IDModelMixin


class User(IDModelMixin, DateTimeModelMixin):
    username: str
    is_disabled: bool = False
    hashed_password: str
