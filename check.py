import re
import os

def Char(_value)->bool:
    if type(_value) != str:
        return False
    if len(_value) != 1:
        return False
    return True

def NaturalNumber(_value:int, include0=True)->bool:
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

def ValidFolder(_path):
    return os.path.exists(_path) and os.path.isdir(_path)

def ValidFile(_path):
    return os.path.exists(_path) and os.path.isfile(_path)

def CanCreateFolder(_path):
    try:
        os.makedirs(_path, exist_ok=True)
        os.removedirs(_path)
        return True
    except OSError:
        return False