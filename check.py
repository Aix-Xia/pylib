import re

def Char(_value)->bool:
    if type(_value) != str:
        return False
    if len(_value) != 1:
        return False
    return True
def NaturalNumber(_value, include0=True)->bool:
    if type(_value) != int:
        return False
    limit = 0 if include0 else 1
    if _value < limit:
        return False
    return True

def NamingRule(name:str)->bool:
    if type(name) != str:
        return False
    if len(name) <= 0:
        return False
    if not bool(re.fullmatch('[a-zA-Z0-9_]+', name)):
        return False
    if name[0].isdigit():
        return False
    return True