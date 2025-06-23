from enum import Enum


class PaymentStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"