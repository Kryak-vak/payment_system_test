from abc import ABC
from typing import Generic, Type

from django.forms.models import model_to_dict

from .dto import OrganizationDTO, PaymentDTO, PaymentTransactionDTO
from .models import Organization, Payment, PaymentTransaction
from .types import DTOType, ModelType


class BaseMapper(ABC, Generic[ModelType, DTOType]):
    model: Type[ModelType]
    dto_class: Type[DTOType]

    @classmethod
    def to_dto(cls, model: ModelType) -> DTOType:
        return cls.dto_class.model_validate(model_to_dict(model))

    @classmethod
    def to_model(cls, dto: DTOType) -> ModelType:
        return cls.model(**dto.model_dump())


class PaymentMapper(BaseMapper[Payment, PaymentDTO]):
    model = Payment
    dto_class = PaymentDTO


class OrganizationMapper(BaseMapper[Organization, OrganizationDTO]):
    model = Organization
    dto_class = OrganizationDTO


class PaymentTransactionMapper(BaseMapper[PaymentTransaction, PaymentTransactionDTO]):
    model = PaymentTransaction
    dto_class = PaymentTransactionDTO
    
    @classmethod
    def from_payment_dto(
        cls, payment_dto: PaymentDTO, status: str
    ) -> PaymentTransactionDTO:
        base_data = payment_dto.model_dump(
                        include=cls.dto_class.model_fields.keys(),
                    )
        base_data['status'] = status
        
        return cls.dto_class(**base_data)
