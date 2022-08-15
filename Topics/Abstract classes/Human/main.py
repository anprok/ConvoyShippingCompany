from abc import ABC, abstractmethod


class Human(ABC):

    @abstractmethod
    def say_hello(self):
        ...