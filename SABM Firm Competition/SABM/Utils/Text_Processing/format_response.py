import re
from SABM.Utils.Implement_Tools.display import display_error

def match_number_int(response:str, exception = 0):
    matches = re.findall(r'\d+', response)
    if matches:
        return int(matches[0])
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