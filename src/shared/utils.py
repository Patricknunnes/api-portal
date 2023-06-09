from datetime import date
from re import search, sub
from requests import get
from starlette.requests import Request
from typing import Union
from uuid import UUID
from validate_docbr import CNPJ, CPF, CNH, RENAVAM

from src.exceptions.exceptions import BadRequestException, NotFoundException
from src.schemas.utils_schema import ValidateDocs


class UtilService:
    @staticmethod
    def validate_doc(docs_data: ValidateDocs):
        validate_doc = {
            'cpf': CPF().validate(docs_data.number),
            'cnpj': CNPJ().validate(docs_data.number),
            'cnh': CNH().validate(docs_data.number),
            'renavam': RENAVAM().validate(docs_data.number)
        }

        if not validate_doc[f'{docs_data.type_doc}']:
            raise BadRequestException(detail='Documento invalido.')
        return True

    @staticmethod
    def validate_cep(cep_number: int = None):
        if len(str(cep_number)) != 8:
            raise BadRequestException('O códigos Postal no Brasil consistem em 8 números')

        result = get(f'https://viacep.com.br/ws/{cep_number}/json/').json()

        if result.get('erro'):
            raise NotFoundException('Cep não encontrado.')
        return result

    @staticmethod
    def validate_email(email: str = None):
        regex = '^[\\w.\\-#_$%*]{2,50}@\\w+[.\\-_]?\\w+.\\w{2,3}[.\\w{2}]?$'

        if email is None:
            raise BadRequestException('Por favor informe o e-mail a ser validado.')
        elif search(regex, email):
            return True
        else:
            raise BadRequestException('Email invalido.')

    @staticmethod
    def validate_phone(phone: Union[str, int] = None):
        regex = '^\\(?\\d{2}\\)?[ ]?\\d{1}[. ]?\\d{4}[- ]?\\d{4}$'

        if not phone:
            raise BadRequestException('Por favor informe o telefone a ser validado.')
        elif search(regex, str(phone)):
            return True
        else:
            raise BadRequestException('Telefone invalido.')

    @staticmethod
    def remove_none_in_form(form):
        return {key: value for key, value in form.__dict__.items()
                if not (value in [None, '', 'string', date.today()])
                and not key.startswith('_')}

    @staticmethod
    def validate_schema(schema_base, form):
        not_optional = []
        for key, value in schema_base.__annotations__.items():
            if key not in form:
                not_optional.append(key)
        if len(not_optional):
            raise BadRequestException(
                detail=f'Campos obrigatorios: ({", ".join(not_optional)}) .'
            )

    @staticmethod
    def validate_str_as_uuid(string: str, key: str):
        if type(string) != UUID:
            raise BadRequestException(detail=f'{key} deve ser um UUID.')


class GetPathAndMethod:
    def __call__(self, request: Request) -> dict:
        url = request.scope['path']
        url = sub(r'/\w{8}-(\w{4}-){3}\w+', '/{id}', url)

        return {
            'method': request.method.lower(),
            'path': url
        }
