#!/bin/bash
# mostly from PREDICT man page by KB2BD
# Suitable as a cron.weekly script
mkdir -p /tmp/keps
cd /tmp/keps
rm -f amateur.txt visual.txt weather.txt
wget -qr www.celestrak.com/NORAD/elements/amateur.txt -O amateur.txt
wget -qr www.celestrak.com/NORAD/elements/visual.txt -O visual.txt
wget -qr www.celestrak.com/NORAD/elements/weather.txt -O weather.txt
/usr/bin/predict -u amateur.txt visual.txt weather.txt

