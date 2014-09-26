rtlsdr-automated-wxsat-capture
==============================

Automate Recording of Low Earth Orbit NOAA Weather Satellites

These are some automation scripts I am developing in python for weather satellite hobbyist use.

License:  GPLv2 or any later version

assumptions: Linux-based computer, rtl-sdr usb dongle, stationary antenna

goal:  record wav files for later processing

prerequistes:  working rtl-sdr, predict (text based, not gpredict) setup with correct ground station coordinates, sox

LICENSE - General Public License version 2.0, or any later version

dotpredict-predict.tle
    Modification of PREDICT's TLE file to provide orbit data for weather satellites NOAA-18,NOAA-19
    Copy as follows:  `mv dotpredict-predict.tle ~/.predict/predict.tle` 
    to get coverage of NOAA-18 and NOAA-19 that is missing in predict's default config

noaacapture.py
	This is the main python script.  It will calculate the time
of the next pass for recording.  It expects to call rtl_fm to do the
recording and sox to convert the file to .wav

pypredict.py
	This is a short python module for extracting the AOS/LOS times
of the next pass for a specified satellite.  It calls predict -p and extracts
the times from the first and last lines.

update-keps.sh
	This is a short shell script to update the keps, which are orbital
parameters needed by the predict program.  It is mostly copied from the PREDICT man
page. PREDICT was written by John Magliacane, KD2BD and released under the
GPL license.
