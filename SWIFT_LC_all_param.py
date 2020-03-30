# -*- coding: utf-8 -*-
def coord(teldef,eventext,timecol,skyxnull,skyynull,attfile,eventfile,ra,dec,randomize,aberration,follow_sun,seed,timemargin,history,chatter):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; coordinator teldef=%s eventext=%s timecol=%s skyxnull=%s skyynull=%s attfile=%s eventfile=%s ra=%s dec=%s randomize=%s aberration=%s follow_sun=%s seed=%s timemargin=%s history=%s chatter=%s' % (teldef,eventext,timecol,skyxnull,skyynull,attfile,eventfile,ra,dec,randomize,aberration,follow_sun,seed,timemargin,history,chatter)
    proc = Popen(cmd,
                 shell=True,
                 stdout=PIPE, stderr=PIPE
    )# по умолчанию: eventext = EVENT,timecol = TIME,skyxnull = 0,skyynull = 0,aberration = yes,follow_sun = yes,randomize = yes,seed = -1956,timemargin = 32.0,interpolation = LINEAR,history = yes,chatter = 1.
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'coor_result:', res[0]
    
def flagpix(outfile,infile,hdfile,thrfile,srcfile,bpfile,userbpfile,bptable,phas1thr,maxtemp,outbpfile,overstatus,chatter,clobber,history):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; xrtflagpix outfile=%s infile=%s hdfile=%s thrfile=%s srcfile=%s bpfile=%s userbpfile=%s bptable=%s phas1thr=%s maxtemp=%s outbpfile=%s overstatus=%s chatter=%s clobber=%s history=%s' % (outfile,infile,hdfile,thrfile,srcfile,bpfile,userbpfile,bptable,phas1thr,maxtemp,outbpfile,overstatus,chatter,clobber,history)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )# по умолчанию: srcfile=CALDB, bpfile=CALDB, userbpfile=NONE, bptable=CALDB,phas1thr = 80,maxtemp = 0.0,outbpfile=DEFAULT,overstatus=yes,chatter = 2,clobber = no, history = yes.
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'flag_result:', res[0]

def pcgrade(outfile,infile,hdfile,gradefile,thrfile,split,ascagrade,history,clobber,chatter):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; xrtpcgrade outfile=%s infile=%s hdfile=%s gradefile=%s thrfile=%s split=%s ascagrade=%s history=%s clobber=%s chatter=%s' % (outfile,infile,hdfile,gradefile,thrfile,split,ascagrade,history,clobber,chatter)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )# по умолчанию: gradefile = CALDB,split = -1,ascagrade = no,history=yes,clobber=no,chatter = 2.
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'pcgrade_result:', res[0]

def hotpix(infile,outfile,outbpfile,overstatus,usegoodevt,phamin,phamax,cellsize,impfac,logpos,bthresh,cleanflick,iterate,gradeiterate,hotneigh,chatter,clobber,history):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; xrthotpix infile=%s outfile=%s outbpfile=%s overstatus=%s usegoodevt=%s phamin=%s phamax=%s cellsize=%s impfac=%s logpos=%s bthresh=%s cleanflick=%s iterate=%s gradeiterate=%s hotneigh=%s chatter=%s clobber=%s history=%s ' % (infile,outfile,outbpfile,overstatus,usegoodevt,phamin,phamax,cellsize,impfac,logpos,bthresh,cleanflick,iterate,gradeiterate,hotneigh,chatter,clobber,history)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )# по умолчанию: outbpfile = DEFAULT,outbpfile = DEFAULT,usegoodevt = yes,phamin=0,phamax=4095,cellsize = 3,impfac = 1000.0,logpos = -5.3bthresh = 3.0,cleanflick = yes,iterate = yes,gradeiterate = yes,hotneigh = no,chatter = 5,clobber = no,history = yes.
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'hotpix_result:', res[0]

def calcpi(infile,outfile,hdfile,gainfile,gainnom,offset,randomflag,seed,corrtype,userctcorrpar,alpha1,alpha2,ebreak,userctipar,beta1,beta2,ecti,offsetniter,savepioffset,savepinom,clobber,history,chatter):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; xrtcalcpi infile=%s outfile=%s hdfile=%s gainfile=%s gainnom=%s offset=%s randomflag=%s seed=%s corrtype=%s userctcorrpar=%s alpha1=%s alpha2=%s ebreak=%s userctipar=%s beta1=%s beta2=%s ecti=%s offsetniter=%s savepioffset=%s savepinom=%s clobber=%s history=%s chatter=%s' % (infile,outfile,hdfile,gainfile,gainnom,offset,randomflag,seed,corrtype,userctcorrpar,alpha1,alpha2,ebreak,userctipar,beta1,beta2,ecti,offsetniter,savepioffset,savepinom,clobber,history,chatter)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )# по умолчанию:gainfile = CALDB,gainnom = -99.9 ,offset = 0.0,randomflag=yes,seed = -1457,corrtype = TOTAL,userctcorrpar = no,alpha1 = 0,alpha2 = 0,ebreak = 1,userctipar = no,offsetniter = 2,savepioffset = no,savepinom = no,clobber=no,history=yes,chatter = 2.
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'calcpi_result:', res[0]

def tfilter(hdfile,enfile,nonulls,outdir,clobber,chatter,history,attfile,alignfile,outfile,outcols,orbmode,orbfile,leapfile,rigfile,origin,interval,ranom,decnom,mkfconfigfile,configfile,hdstem,mkffile,gtiexpr):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; cd /home/max/Documents/SAO_pract/red; CALDB=/home/max; xrtfilter hdfile=%s enfile=%s nonulls=%s outdir=%s clobber=%s chatter=%s history=%s attfile=%s alignfile=%s outfile=%s outcols=%s orbmode=%s orbfile=%s leapfile=%s rigfile=%s origin=%s interval=%s ranom=%s decnom=%s mkfconfigfile=%s configfile=%s hdstem=%s mkffile=%s gtiexpr=%s' % (hdfile,enfile,nonulls,outdir,clobber,chatter,history,attfile,alignfile,outfile,outcols,orbmode,orbfile,leapfile,rigfile,origin,interval,ranom,decnom,mkfconfigfile,configfile,hdstem,mkffile,gtiexpr)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )# по умолчанию: nonulls=yes,clobber=no,chatter = 3,history=yes,outfile=DEFAULT,outcols=CALDB,orbmode=TLE_TEXT2,orbfile=$HEADAS//refdata/SWIFT_TLE_ARCHIVE.txt,leapfile=$HEADAS/refdata/leapsec.fits,rigfile=$HEADAS/refdata/rigidity.data,origin=NASA/GSFC,interval=1,mkfconfigfile = CALDB,configfile = NONE,hdstem=NONE,mkffile=DEFAULT,gtiexpr=(TIME-TIME{-1}<5.1.or.ISNULL(TIME{-1}).
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'tfilter_result:', res[0]

def screen(gtiexpr,exprgrade,expr,infile,outdir,clobber,chatter,history,createattgti,createinstrgti,gtiscreen,evtscreen,obsmodescreen,acsscreen,mkffile,gtifile,usrgtifile,hkrangefile,timecol,outfile,gtiext,evtrangefile,cleanup):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; cd /home/max/Documents/SAO_pract/red;xrtscreen gtiexpr=%s exprgrade=%s expr=%s infile=%s outdir=%s clobber=%s chatter=%s history=%s createattgti=%s createinstrgti=%s gtiscreen=%s evtscreen=%s obsmodescreen=%s acsscreen=%s mkffile=%s gtifile=%s usrgtifile=%s hkrangefile=%s timecol=%s outfile=%s gtiext=%s evtrangefile=%s cleanup=%s' % (gtiexpr,exprgrade,expr,infile,outdir,clobber,chatter,history,createattgti,createinstrgti,gtiscreen,evtscreen,obsmodescreen,acsscreen,mkffile,gtifile,usrgtifile,hkrangefile,timecol,outfile,gtiext,evtrangefile,cleanup)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )# по умолчанию: clobber=no,chatter = 3,history=yes,gtifile = DEFAULT,usrgtifile = NONE,hkrangefile = CALDB,timecol = TIME,gtiext = GTI,evtrangefile = CALDB,cleanup =yes.
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'screen_result:', res[0]

def select():
    from subprocess import Popen, PIPE
    cmd = 'xselect'
    proc = Popen(cmd,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)

    rd=open('param.dat','r')
    s=rd.read()
    c=s.split('\n')
    rd.close()
    for i in range(len(c)):
        rev=c[i]+"\n"
        proc.stdin.write(rev)
    proc.wait()
    res=proc.communicate()
    if proc.returncode:
        print res[1]
    else:
        print res[0]




