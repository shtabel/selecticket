import re

def validation_error():
    raise ValueError("Email is not valid!")

def validate_email(email):
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