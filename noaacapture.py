import time
import pypredict
import subprocess

satellites = ['NOAA-18','NOAA-19','NOAA-15']
freqs = [137912500, 137100000, 137620000]
sample = '44100'
wavrate='11025'

def runForDuration(cmdline, duration):
    try:
        child = subprocess.Popen(cmdline)
        time.sleep(duration)
        child.terminate()
    except OSError as e:
        print "OS Error during command: "+" ".join(cmdline)
        print "OS Error: "+e.strerror

def recordFM(freq, fname, duration):
    # still experimenting with options - unsure as to best settings
    cmdline = ['rtl_fm',\
               '-f',str(freq),\
               '-s',sample,\
               '-g','40',\
               '-F','9',\
               '-A','fast',\
               '-E','deemp',\
               '-E','dc',\
               fname+'.raw']
    runForDuration(cmdline, duration)

def transcode(fname):
    cmdline = ['sox','-t','raw','-r',sample,'-es','-b','16','-c','1','-V1',fname+'.raw',fname+'.wav','rate',wavrate]
    subprocess.call(cmdline)

def decode(fname):
    cmdline = ['/root/atpdec-1.7/atpdec',fname+'.wav']
    subprocess.call(cmdline)

def recordWAV(freq,fname,duration):
    recordFM(freq,fname,duration)
    transcode(fname)

def spectrum(fname,duration):
    cmdline = ['rtl_power','-f','137000000:138000000:1000','-i','1m','-g','40',fname+'.csv']
    runForDuration(cmdline,duration)

def findNextPass():
    predictions = [pypredict.aoslos(s) for s in satellites]
    aoses = [p[0] for p in predictions]
    nextIndex = aoses.index(min(aoses))
    return (satellites[nextIndex],\
            freqs[nextIndex],\
            predictions[nextIndex]) 

while True:
    (satName, freq, (aosTime, losTime)) = findNextPass()
    now = time.time()
    towait = aosTime-now
    if towait>0:
        print "waiting "+str(towait)+" seconds for "+satName
        time.sleep(towait)
    # dir= sat name and filename = start time 
    fname='./'+satName+'/'+str(aosTime)
    print "beginning pass "+fname+" predicted end "+str(losTime)
    recordWAV(freq,fname,losTime-aosTime)
    decode(fname) # make picture
    # spectrum(fname,losTime-aosTime)
    print "finished pass "+fname+" at "+str(time.time())
    time.sleep(60.0)

