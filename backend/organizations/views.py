from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.views import View
from pydantic import ValidationError
from stdnum.ru import inn as inn_utils

from .dto import PaymentDTO
from .exceptions import OrganizationNotFound, PaymentAlreadyProcessed
from .services import PaymentService


class ReceivePaymentView(View):
    service = PaymentService()
    dto_class = PaymentDTO

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            payment_dto = self.dto_class.model_validate_json(request.body)
            payment_db_dto = self.service.process_payment(payment_dto)
        
        except ValidationError as e:
            return JsonResponse({'errors': e.errors()}, status=400)
        
        except (PaymentAlreadyProcessed, OrganizationNotFound) as e:
            return e.to_response()

        return JsonResponse(payment_db_dto.model_dump(), status=200)


class ReadBalanceView(View):
    def get(self, request: HttpRequest, inn: str) -> JsonResponse:
        if not inn_utils.is_valid(inn):
            return HttpResponseBadRequest("Invalid INN.")
        
        
        

