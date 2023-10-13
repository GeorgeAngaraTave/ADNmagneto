from abc import ABC, abstractmethod
from typing import Dict

from app.ext.generic_model import GenericModel


class BaseEntity(ABC):

    def __init__(self):
        self.model: GenericModel = None

    @abstractmethod
    def serialize(self) -> Dict:
        pass

    @abstractmethod
    def from_dict(self, _data: Dict):
        pass
