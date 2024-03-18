# Standard Library
from enum import Enum


class EventTiming(str, Enum):
    WAKE_UP = "起床"
    BEFORE_BREAKFAST = "朝食前"
    AFTER_BREAKFAST = "朝食後"
    BEFORE_LUNCH = "昼食前"
    AFTER_LUNCH = "昼食後"
    BEFORE_DINNER = "夕食前"
    AFTER_DINNER = "夕食後"
    BEFORE_SNACK = "間食前"
    AFTER_SNACK = "間食後"
    BEFORE_EXERCISE = "運動前"
    AFTER_EXERCISE = "運動後"
    BEDTIME = "就寝"
    LATE_NIGHT = "深夜"
    OTHER = "その他"
