from abc import abstractmethod, ABC


class StoreProtocol(ABC):

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplemented


class OrderStoreStory(StoreProtocol):

    def execute(self, total_price: float, user_id: int) -> dict:
        return {}
