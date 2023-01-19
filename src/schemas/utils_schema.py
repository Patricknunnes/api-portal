from pydantic import BaseModel


class ValidateDocs(BaseModel):
    type_doc: str
    number: str


class ValidateDocsResponse(BaseModel):
    valid: bool


class Image(BaseModel):
    image: str


class ValidateCEP(BaseModel):
    cep: str
    logradouro: str
    complemento: str
    bairro: str
    localidade: str
    uf: str
    ibge: int
    ddd: int
