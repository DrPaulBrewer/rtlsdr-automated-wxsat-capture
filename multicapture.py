import math
import time
import pypredict
import subprocess

children = []

def pollall():
    global children
    try:
        dead = [child for child in children if child.poll() is not None];
        for child in dead:
            children.remove(child)
    except Exception as e:
        print "Exception: "+str(e)

def runForDuration(cmdline, duration):
    try:
        child = subprocess.Popen(cmdline)
        time.sleep(duration)
        child.terminate()
    except OSError as e:
        print "OS Error during command: "+" ".join(cmdline)
        print "OS Error: "+e.strerror


def recordSDR(fname, freq, duration):
    sdrOffset = -50000
    sdrRate = 20800*11
    sdrFreq = int(freq)+int(sdrOffset)
    cmdline = ['rtl_sdr',\
               '-f', str(sdrFreq),\
               '-s', str(sdrRate),\
               fname+'.sdr']
    runForDuration(cmdline, duration)

def rawFM(fname, freq, duration):
    sample = 20800
    cmdline = ['rtl_fm',\
               '-f',str(freq),\
               '-M','raw',\
               '-s',str(sample),\
               '-g', '47',\
               '-F','9',\
#               '-A','fast',\
               '-E','dc',\
               fname+'M.raw']
    runForDuration(cmdline, duration)

def decode(fname):
#    cmdline = ['atpdec',fname+'.wav']
#    subprocess.call(cmdline)
    cmdline = ['python','-m','cqwx.APT',fname+'X5.wav',fname+'R.png',fname+'F.png']
    try:
        children.append(subprocess.Popen(cmdline)) # run in background
    except OSError as e:
        print e.strerror

def spectrum(fname,freq,duration):
    flow = freq - 10000
    fhigh = freq + 10000
    fstep = 100
    fparam = ":".join(map(str,[flow,fhigh,fstep]))
    cmdline = ['rtl_power','-f',fparam,'-i','1m','-g','40',fname+'.csv']
    runForDuration(cmdline,duration)

satellites = [\
	{'name': 'NOAA-18',\
	'freq': 137912500,\
	'listen': rawFM },\
	{'name': 'NOAA-19',\
 	'freq': 137100000,\
	'postProcess': decode },\
	{'name': 'NOAA-15',\
	'freq': 137620000,\
	'postProcess': decode },\
#        {'name': 'OSCAR-7',\
#         'freq': 145950000, \
#         'listen': recordSDR },\
        {'name': 'FUNCUBE-1',\
         'freq': 145950000, \
         'listen': recordSDR },\
#        {'name': 'OSCAR-29',
#         'freq': 435850000, \
#         'listen': recordSDR },\
#	{'name': 'OSCAR-50',\
#	 'freq': 436795000,\
#        },\
#        {'name': 'ISS',\
#         'freq': 145800000 }\
]
	
sample = '20800'
wavrate='11025'
wav5rate ='20800'

def recordFM(freq, fname, duration):
    # still experimenting with options - unsure as to best settings
    cmdline = ['rtl_fm',\
               '-f',str(freq),\
               '-s',sample,\
               '-g', '47',\
               '-F','9',\
#               '-A','fast',\
               '-E','dc',\
               fname+'.raw']
    runForDuration(cmdline, duration)

def transcode(fname):
#    todolist = [('.wav', wavrate), ('X5.wav', wav5rate)]
    todolist = [('X5.wav', wav5rate)]
    for (ext,rate) in todolist:
        try: 
            cmdline = ['sox','-t','raw','-r',sample,'-es','-b','16','-c','1','-V1',fname+'.raw',fname+ext,'rate',rate]
            subprocess.call(cmdline)
        except OSError, e:
            print "OSError on :"+" ".join(cmdline)
            print "OSError:"+e.strerror

def recordWAV(freq,fname,duration):
    recordFM(freq,fname,duration)
    transcode(fname)

def findNextPass():
    predictions = [pypredict.aoslos(s['name']) for s in satellites]
    aoses = [p[0] for p in predictions]
    nextIndex = aoses.index(min(aoses))
    return (satellites[nextIndex],\
            predictions[nextIndex]) 

while True:
    pollall()
    (sat, (aosTime, losTime)) = findNextPass()
    satName = sat['name']
    freq = sat['freq']
    now = time.time()
    towait = aosTime-now
    if towait>0:
        print "waiting "+str(towait)+" seconds for "+satName
        time.sleep(towait)
    # dir= sat name and filename = start time 
    fname='./'+satName+'/'+str(aosTime)
    print "beginning pass "+fname+" predicted end "+str(losTime)
    if 'listen' in sat:
        sat['listen'](fname, freq, losTime-aosTime)
    else:
        recordWAV(freq,fname,losTime-aosTime)
    if 'postProcess' in sat:
        sat['postProcess'](fname) # analyze, make pictures, graphs, etc.
    print "finished pass "+fname+" at "+str(time.time())
    time.sleep(60.0)

