def coord(teldef,attfile,eventfile,ra,dec,rand,aber):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; coordinator teldef=%s attfile=%s eventfile=%s ra=%4.4f dec=%4.4f randomize=%s aberration=%s' % (teldef,attfile,eventfile,ra,dec,rand,aber)
    proc = Popen(cmd,
                 shell=True,
                 stdout=PIPE, stderr=PIPE
    )
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'coor_result:', res[0]
    
def flagpix(outfile,eventfile,hdfile,thr):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; xrtflagpix outfile=%s infile=%s hdfile=%s thrfile=%s' % (outfile,eventfile,hdfile,thr)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'flag_result:', res[0]

def pcgrade(outfile,infile):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; xrtpcgrade outfile=%s infile=%s' % (outfile,infile)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'pcgrade_result:', res[0]

def hotpix(outfile,infile,phamin,phamax):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; xrthotpix outfile=%s infile=%s phamin=%4d phamax=%4d ' % (outfile,infile,phamin,phamax)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'hotpix_result:', res[0]

def calcpi(outfile,infile,hdfile):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; xrtcalcpi outfile=%s infile=%s hdfile=%s' % (outfile,infile,hdfile)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'calcpi_result:', res[0]

def tfilter(hdfile,outdir,attfile,alignfile,ranom,decnom):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; cd /home/max/Documents/SAO_pract/red; CALDB=/home/max; xrtfilter hdfile=%s outdir=%s attfile=%s alignfile=%s ranom=%4.4f decnom=%4.4f' % (hdfile,outdir,attfile,alignfile,ranom,decnom)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'tfilter_result:', res[0]

def screen(mkffile,createinstrgti,outfile,createattgti,infile,gtiscreen,outdir,evtscreen,gtiexpr,exprgrade,expr):
    from subprocess import Popen, PIPE
    cmd = 'CALDB=/home/max; cd /home/max/Documents/SAO_pract/red;xrtscreen mkffile=%s createinstrgti=%s outfile=%s createattgti=%s infile=%s gtiscreen=%s outdir=%s evtscreen=%s gtiexpr=%s exprgrade=%s expr=%s' % (mkffile,createinstrgti,outfile,createattgti,infile,gtiscreen,outdir,evtscreen,gtiexpr,exprgrade,expr)
    proc = Popen(
        cmd,
        shell=True,
        stdout=PIPE, stderr=PIPE
    )
    proc.wait()    
    res = proc.communicate()  
    if proc.returncode:
        print res[1]
    print 'screen_result:', res[0]
