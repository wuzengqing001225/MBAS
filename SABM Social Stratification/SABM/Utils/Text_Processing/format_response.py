import re
from SABM.Utils.Implement_Tools.display import display_error

def match_number_int(response:str, exception = 0):
    matches = re.findall(r'\d+', response)
    if matches:
        return int(matches[0])
    else:
        display_error(f"match number error from {response}", type = 'STD Process')
        return exception

def match_number_int(response:str, lrange:int, rrange:int, exception = 0):
    matches = re.findall(r'\d+', response)
    if matches:
        if lrange <= int(matches[0]) <= rrange:
            return int(matches[0])
        else:
            display_error(f"match number error from {response}", type = 'STD Process')
            return exception
    else:
        display_error(f"match number error from {response}", type = 'STD Process')
        return exception

def match_number_float(response:str, exception = 0.0):
    matches = float(re.search(r"[-+]?\d*\.\d+|\d+", response).group())
    if matches:
        return float(matches)
    else:
        display_error(f"match number error from {response}", type = 'STD Process')
        return exception
    
def match_bool_yn(response:str, exception = False):
    response = response.strip().lower()
    if 'y' in response: return True
    elif 'n' in response: return False
    else:
        display_error(f"match Yes/No error from {response}", type = 'STD Process')
        return exception
