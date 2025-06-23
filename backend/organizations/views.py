from http import HTTPStatus

from django.http import HttpRequest, JsonResponse
from django.views import View
from stdnum.ru import inn as inn_utils

from .dto import OrganizationBalanceDTO, PaymentDTO
from .services import OrganizationService, PaymentService


class ReceivePaymentView(View):
    service = PaymentService()
    dto_class = PaymentDTO

    def post(self, request: HttpRequest) -> JsonResponse:
        payment_dto = self.dto_class.model_validate_json(request.body)
        inn_utils.validate(payment_dto.payer_inn)
        
        payment_db_dto = self.service.process_payment(payment_dto)
        return JsonResponse(payment_db_dto.model_dump(), status=HTTPStatus.OK)


class ReadBalanceView(View):
    service = OrganizationService()
    dto_class = OrganizationBalanceDTO

    def get(self, request: HttpRequest, inn: str) -> JsonResponse:
        inn_utils.validate(inn)

        org_balance_dto = self.service.get_org_balance(inn)
        return JsonResponse(org_balance_dto.model_dump(), status=HTTPStatus.OK)


        
        
        

