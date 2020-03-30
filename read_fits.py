import os,glob,numpy
from astropy.io import fits

def one_event():
    names_curve=sorted(glob.glob("red_curve_*.lc"))
    wt=open('all_events.dat','w')
    res=""
    for name_curve in names_curve:
        fits_source=fits.open(name_curve)
        time=fits_source["RATE"].data.field("TIME")
        rate=fits_source["RATE"].data.field("RATE")
        tstart=fits_source["RATE"].header["tstart"]
        start=fits_source["GTI"].data.field("START")
        stop=fits_source["GTI"].data.field("STOP")
        expos=[stop[i]-start[i] for i in xrange(len(start))]
        print name_curve,' ',len(time),' ',tstart,' ',expos
        sum_rate=0
        ts=time[0]
        n=0
        av_rate={}
        av_err={}
        av_time={}
        for i in xrange(len(time)):
            sum_rate += rate[i]
            if expos[n]>6.0:
                if time[i]-time[i-1]>3.1:
                    av_rate[str(n)] = str((sum_rate-rate[i])*3/(time[i-1]-ts))
                    av_time[str(n)] = str((time[i-1]+ts+2*tstart)/2)
                    print n,' ',av_rate[str(n)],' ',expos[n],' ',time[i-1]-ts
                    ts=time[i]
                    sum_rate=rate[i]
                    n += 1
            else:
                av_rate[str(n)] = '0.0'
                av_time[str(n)] = str((time[i-1]+ts+2*tstart)/2)
                print n,' ',av_rate[str(n)]
                ts=time[i]
                sum_rate=rate[i]
                n += 1
                
        av_rate[str(n)] = str((sum_rate-rate[len(time)-1])*3/(time[len(time)-1]-ts))
        av_time[str(n)] = str((time[len(time)-1]+ts+2*tstart)/2)
        print n,' ',av_rate[str(n)]
        n=0
        ts=time[0]
        serr=0
        for i in xrange(len(time)):
            #serr += (float(av_rate[str(n)])-rate[i])**2
            serr += rate[i]
            if expos[n]>6.0:
                if time[i]-time[i-1]>3.1:
                    av_err[str(n)] = str((serr*3/(time[i-1]-ts)**2)**0.5)
                    ts=time[i]
                    sum_rate=rate[i]
                    print n,' ',av_err[str(n)]
                    n += 1
            else: 
                av_err[str(n)] = '0.0'
                ts=time[i]
                sum_rate=rate[i]
                print n,' ',av_err[str(n)]
                n += 1
        av_err[str(n)] = str(((serr-(float(av_rate[str(n)])-rate[len(time)-1])**2)*9/(time[len(time)-1]-ts)**2)**0.5)
        for i in xrange(n+1):
            if float(av_rate[str(i)])<=0:
                av_rate[str(i)]='0.0'
                av_err[str(i)]='0.0'
            res += av_time[str(i)]+' '+av_rate[str(i)]+' '+av_err[str(i)]+' '+str(expos[i])+'\n'
        fits_source.close()
    wt=open('all_events.dat','w')
    wt.write(res)
    wt.close()

def sort(name):
    rd=open(name+'_events.dat','r').read()
    c=rd.split('\n')
    ls=[c[i].split(' ') for i in xrange(len(c)-1)]
    #print ls
    lsf=[[ float(ls[i][j]) for j in xrange(len(ls[0])) ]for i in xrange(len(c)-1)]
    sls=sorted(lsf)
    wt=open('sorted_events.dat','w')
    result = ""
    for i in xrange(len(c)-1):
        for j in xrange(len(sls[0])):
            print sls[i][1]
            if sls[i][1]<=0.4:
                color='1'
                result += str(sls[i][j])+' '
            else:
                color='2'
                result += str(sls[i][j])+' '
        result += color + '\n'
    wt.write(result)
    wt.close()

def convert():
    rd1=open('sorted_events.dat','r').read()
    rd2=open('count_to_flux.dat','r').read()
    counts=[[float(count) for count in line.split(' ') if count!=""] for line in rd1.split('\n')]
    fluxes=[[float(flux) for flux in line.split(' ') if flux !=""] for line in rd2.split('\n')]
    sort_flux=sorted(fluxes)
    print len(counts)
    i=0
    text=""
    for j in xrange(len(counts)-1):
        if counts[j][0]<sort_flux[i][0]:
            fl_rate=counts[j][1]*sort_flux[i][1]/sort_flux[i][2]
            fl_er=counts[j][2]*sort_flux[i][1]/sort_flux[i][2]
            text += str(counts[j][0])+' '+str(fl_rate)+' '+str(fl_er)+' '+str(int(counts[j][4]))+'\n'
            #print counts[j][0],' ',sort_flux[i][0]
        else:
            i += 1
            fl_rate=counts[j][1]*counts[j][3]*sort_flux[i][1]/sort_flux[i][2]
            fl_er=counts[j][2]*counts[j][3]*sort_flux[i][1]/sort_flux[i][2]
            text += str(counts[j][0])+' '+str(fl_rate)+' '+str(fl_er)+' '+str(int(counts[j][4]))+'\n'
            #print counts[j][0],' ',sort_flux[i][0]
    print text            
    wt=open('fluxed_curve.dat','w').write(text)

def rebin(bin__):
    bin_=bin__*86400
    n=0
    names_curve=sorted(glob.glob("red_curve_*.lc"))
    for name in names_curve:
        fits_source=fits.open(name)
        n += len(fits_source["RATE"].data.field("TIME"))
    print n
    massive=[[0 for i in xrange(2)] for j in xrange(n)]
    k=0
    for name in names_curve:
        fits_source=fits.open(name)
        k2=len(fits_source["RATE"].data.field("RATE"))
        mas=fits_source["RATE"].data.field("RATE")
        mas1=fits_source["RATE"].data.field("TIME")
        tstart=fits_source["RATE"].header["TSTART"]
        j=0
        for i in xrange(k,k+k2):
            massive[i][0]=mas1[j]+tstart
            massive[i][1]=mas[j]
            j += 1
        k += k2
    mas_sort=sorted(massive)
    time=[mas_sort[i][0] for i in xrange(len(massive))]
    rate=[mas_sort[i][1] for i in xrange(len(massive))]
    print time[len(time)-1],time[0]
    bin_n=int((time[len(time)-1]-time[0])/bin_)
    res=""
    k=0
    for i in xrange(1,bin_n+1):
        sum_rate=0
        t=bin_*i+time[0]
        j = k
        bin_bool=False
        expose = 0
        while time[j]<t:
            sum_rate += rate[j]
            j += 1
            bin_bool=True
        if sum_rate<0:
            sum_rate=0
        if bin_bool==True:
            av_rate=sum_rate/(j-1-k)
            print sum_rate,time[j-1],time[k]
            av_time=(t+bin_*(i-1)+time[0])/2
            av_err=((sum_rate/3.0)**0.5)/(j-1-k)
            k = j
            res += str(av_time)+' '+str(av_rate)+' '+str(av_err)+' '+str(bin_)+'\n'
    wt=open('bin_events.dat','w').write(res)
    
def convert_rebin():
    rd1=open('sorted_events.dat','r').read()
    rd2=open('count_to_flux.dat','r').read()
    counts=[[float(count) for count in line.split(' ') if count!=""] for line in rd1.split('\n')]
    fluxes=[[float(flux) for flux in line.split(' ') if flux !=""] for line in rd2.split('\n')]
    i=0
    text=""
    k=0
    for i in xrange(len(fluxes)):
        k += fluxes[i][1]/fluxes[i][2]
    koef=k/len(fluxes)
    print koef
    for j in xrange(len(counts)-1):
        fl_rate=counts[j][1]*koef#counts[j][3]*koef
        fl_er=counts[j][2]*koef#counts[j][3]*koef
        text += str(counts[j][0])+' '+str(fl_rate)+' '+str(fl_er)+' '+str(int(counts[j][4]))+'\n'
        print counts[j][0],' ',koef
    print text            
    wt=open('fluxed_bin.dat','w').write(text)

def convert_rebin1(bin__):
    rd2=open('count_to_flux.dat','r').read()
    fluxes=[[float(flux) for flux in line.split(' ') if flux !=""] for line in rd2.split('\n') if line!='']
    sort_flux=sorted(fluxes)
    bin_=bin__*86400
    n=0
    names_curve=sorted(glob.glob("red_curve_*.lc"))
    for name in names_curve:
        fits_source=fits.open(name)
        n += len(fits_source["RATE"].data.field("TIME"))
    print n
    massive=[[0 for i in xrange(2)] for j in xrange(n)]
    k=0
    for name in names_curve:
        fits_source=fits.open(name)
        k2=len(fits_source["RATE"].data.field("RATE"))
        mas=fits_source["RATE"].data.field("RATE")
        mas1=fits_source["RATE"].data.field("TIME")
        tstart=fits_source["RATE"].header["TSTART"]
        j=0
        for i in xrange(k,k+k2):
            massive[i][0]=mas1[j]+tstart
            massive[i][1]=mas[j]
            j += 1
        k += k2
    mas_sort=sorted(massive)
    time=[mas_sort[i][0] for i in xrange(len(massive))]
    rate=[mas_sort[i][1] for i in xrange(len(massive))]
    print time[len(time)-1],time[0]
    bin_n=int((time[len(time)-1]-time[0])/bin_)
    res=""
    k=0
    z=0
    g=0
    for i in xrange(1,bin_n+1):
        sum_rate=0
        s_rate = 0
        er_rate=0
        t=bin_*i+time[0]
        j = k
        l = k
        bin_bool=False
        expose = 0
        while (time[j]<t):
            while (time[j]<=sort_flux[z][0]) and (j < len(time)-1) and (z < len(sort_flux)):
                #if (j%100 == 0):
                    #print j,' ',z,' ',len(time),' ',len(sort_flux)
                sum_rate += rate[j]*sort_flux[z][1]/sort_flux[z][2]
                s_rate += rate[j]
                if (j < len(time)-1):
                    j += 1
            if (time[j]>sort_flux[z][0]) and (z < len(sort_flux)) and (j < len(time)-1):
                z += 1
            bin_bool=True
        if bin_bool==True:
            while (time[l]<t):
                while (time[l]<=sort_flux[g][0]) and (l < len(time)-1) and (g < len(sort_flux)):
                    er_rate += ((sum_rate/(j-1-k)-rate[l]*sort_flux[g][1]/sort_flux[g][2])**2)
                    if (l < len(time)-1):
                        l += 1
                if (time[l]>sort_flux[g][0]) and (g < len(sort_flux)) and (l < len(time)-1):
                    g += 1
        if sum_rate<0:
            sum_rate=0
            er_rate=0
        if bin_bool==True:
            av_rate=sum_rate/(j-1-k)
            av_c_rate = s_rate/(j-1-k)
            print sum_rate,time[j-1],time[k]
            av_time=(t+bin_*(i-1)+time[0])/2
            av_err=er_rate**0.5/(j-1-k)
            k = j
            if av_c_rate<=0.4:
                res += str(av_time)+' '+str(av_rate)+' '+str(av_err)+' '+str(1)+'\n'
            else:
                res += str(av_time)+' '+str(av_rate)+' '+str(av_err)+' '+str(2)+'\n'
    print res            
    wt=open('fluxed_bin.dat','w').write(res)

if __name__=='__main__':
    #one_event()
    #rebin(1.0)
    #sort('bin')
    convert_rebin1(1.0)
    #convert()
