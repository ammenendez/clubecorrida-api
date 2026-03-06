class DomainException(Exception):
    """Exceção de domínio (regras de negócio)"""
    pass

class CnpjJaExisteException(DomainException):
    pass
