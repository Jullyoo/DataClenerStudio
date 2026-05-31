import re
import phonenumbers

from validate_docbr import CPF
from validate_docbr import CNPJ


class DataValidator:

    cpf_validator = CPF()
    cnpj_validator = CNPJ()

    @staticmethod
    def validate_cpf(document):

        return DataValidator.cpf_validator.validate(
            document
        )

    @staticmethod
    def validate_cnpj(document):

        return DataValidator.cnpj_validator.validate(
            document
        )

    @staticmethod
    def validate_email(email):

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        return bool(
            re.match(pattern, str(email))
        )

    @staticmethod
    def validate_phone(phone):

        try:

            parsed = phonenumbers.parse(
                phone,
                'BR'
            )

            return phonenumbers.is_valid_number(
                parsed
            )

        except:
            return False