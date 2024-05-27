# Standard Library
from enum import Enum


class EventTiming(str, Enum):
    WHILE_HUNGRY = "空腹時"
    AFTER_MEAL = "食後"
    OTHER = "その他"
