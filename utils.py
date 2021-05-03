import re
import uuid

def validation_error():
    raise ValueError("Email is not valid!")

def validate_email(email: str):
    parts = email.split('@')
    if len(parts) != 2:
        validation_error()

    name_part = parts[0]
    domain_part = parts[1]
    # TODO: check that name_part consists of at least one symbol except '_'
    pattern = re.compile("^[a-zA-Z0-9_]+$]")
    for part in name_part.split('.'):
        if len(part) == 0:
            validation_error()
        if not pattern.match(part):
            validation_error()
    # TODO: is it enough?
    pattern = re.compile("^[a-zA-Z0-9]+$]")
    for part in domain_part.split('.'):
        if len(part) == 0:
            validation_error()
        if not pattern.match(part):
            validation_error()

def has_fields(params: dict, fields: tuple, error=True) -> bool:
    params_missing = []
    for name in fields:
        if not params[name]:
            params_missing.append(name)
    if params_missing and error:
        err_msg = f'Missing parameters: {params_missing}'
        raise ValueError(err_msg)
    return not params_missing


def check_uuid(val):
    if not isinstance(val, uuid.UUID):
        try:
            uuid.UUID(val)
        except:
            raise ValueError('Invalid uuid string!')