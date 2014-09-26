import subprocess
import sys

class missingSatellitePredictionError(Exception):
    def __init__(self):
        self.description = "predict could not find aos, los of next pass"
        
    def __str__(self):
        return self.description
    
def aoslos(satname):
    lines = subprocess.check_output(['predict','-p',satname]).split("\n")
    try:
        aosTime=int(lines[0].split(" ")[0])
        losTime=int(lines[-2].split(" ")[0])
        if losTime>aosTime:
            return (aosTime,losTime)
    except Exception:
        pass
    raise missingSatellitePredictionError()





