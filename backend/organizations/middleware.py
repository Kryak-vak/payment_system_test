from http import HTTPStatus

from django.http import JsonResponse
from pydantic import ValidationError as PydanticValidationError
from stdnum.exceptions import ValidationError

from .exceptions import OrganizationNotFound, PaymentAlreadyProcessed


class DomainExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        if isinstance(exception, (PaymentAlreadyProcessed, OrganizationNotFound)):
            return exception.to_response()

        if isinstance(exception, (PydanticValidationError)):
            return JsonResponse(
                {'errors': exception.errors()},
                status=HTTPStatus.BAD_REQUEST
            )

        if isinstance(exception, (ValidationError)):
            return JsonResponse(
                {'errors': 'Invalid inn'},
                status=HTTPStatus.BAD_REQUEST
            )

        return None