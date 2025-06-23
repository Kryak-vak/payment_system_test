from abc import ABC
from http import HTTPStatus

from django.http import JsonResponse


class PaymentException(ABC, Exception):
    """Base exception for all payment related exceptions."""

    def __init__(self, obj_id: str, *args):
        self.message = obj_id

        super().__init__(*args)

    @property
    def status_code(self) -> int:
        pass

    @property
    def description(self) -> str:
        pass

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, obj_id: str) -> str:
        self._message = self.description.format(obj_id)

    def to_response(self) -> JsonResponse:
        return JsonResponse({'error': self.message}, status=self.status_code)
        

class PaymentAlreadyProcessed(PaymentException):
    """Raised when the payment with the given operation_id already exists."""
    
    @property
    def description(self) -> str:
        return 'Payment with id={} has already been processed'

    @property
    def status_code(self) -> int:
        return HTTPStatus.OK


class OrganizationNotFound(PaymentException):
    """Raised when the organization with the given inn is not found."""
    
    @property
    def description(self) -> str:
        return 'Organization with inn={} has not been found'

    @property
    def status_code(self) -> int:
        return HTTPStatus.NOT_FOUND
