
from abc import ABC, abstractmethod

class DNS_provider(ABC):
    @abstractmethod
    def get_ip(self) -> str:
        pass

