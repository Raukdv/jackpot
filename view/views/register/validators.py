from wsgiref import validate

TYPE_VALIDATE = [
        'claimer',
        'defendant',
        'talentshow',
        'creator',
        'witness',
        'respondant'
    ]

def path_user_type_validator(path):
    
    value = str(path).split('/')

    validated = value[3].lower() if len(value) == 4 else None

    if validated and validated in TYPE_VALIDATE:
        pass
    else:
        validated = validated

    return validated