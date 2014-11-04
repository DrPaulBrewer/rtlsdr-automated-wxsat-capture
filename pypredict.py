import subprocess
import sys
import time


class missingSatellitePredictionError(Exception):
    def __init__(self):
        self.description = "predict did not return data for the satellite"
        
    def __str__(self):
        return self.description
    
def aoslos(satname):
    lines = subprocess.check_output(['predict','-p',satname]).split("\n")
    try:
        aosTime=int(lines[0].split()[0])
        losTime=int(lines[-2].split()[0])
        if losTime>aosTime:
            return (aosTime,losTime)
    except Exception:
        pass
    raise missingSatellitePredictionError()

def groundtrack(satname, start=None, end=None):
    if start is None:
        start = int(time.time())
    if end is None:
        end = start+60*60*24
    command = ['predict','-f',satname,str(start),str(end)+'m']
    lines = subprocess.check_output(command).split("\n")
    result = []
    for line in lines:
        try:
            data = line.split()
            if len(data)==12:  # expect 12 columns, pick out time, lat, lon
                result.extend([int(data[j]) for j in [0,6,7] ])
        except:
            pass
    if len(result)==0:
        raise missingSatellitePredictionError()
    return result




