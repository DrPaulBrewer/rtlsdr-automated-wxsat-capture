#!/usr/bin/gawk -f 
# converts rtl_power format to CSV file with DATE, TIME, FREQ, DB
BEGIN { FS="," }
{ 
    f0=$3;
    f1=$4;
    fs=$5;
    i0=7;
    i1=NF;
    for(i=i0;i<i1;++i) print $1","$2","(f0+(i-i0)*fs)","$i
}


