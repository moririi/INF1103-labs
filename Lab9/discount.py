from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Every discount has the same apply() method, so Order doesn't care which one it has."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """e.g. PercentageDiscount(10) takes 10% off the total."""

    def __init__(self, percentage: float):
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return round(total * (1 - self.__percentage / 100), 2)


class BulkDiscount(DiscountStrategy):
    """e.g. BulkDiscount(200, 20) takes $20 off any total of $200 or more."""

    def __init__(self, threshold: float, amount: float):
        if threshold <= 0 or amount <= 0:
            raise ValueError("Threshold and amount must be greater than zero.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return round(total - self.__amount, 2)
        return total


class StudentDiscount(DiscountStrategy):
    """Fixed 5% off for students. Added in 2.4 without touching Order at all."""

    STUDENT_RATE: float = 5

    def apply(self, total: float) -> float:
        return round(total * (1 - self.STUDENT_RATE / 100), 2)