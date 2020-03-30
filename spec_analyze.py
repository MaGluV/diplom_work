from astropy.io import fits
import os,glob,shutil,getpass,math
from make_spec import heas_dest
from subprocess import Popen,PIPE

def Xspec(direct,home_dir,name,model,energy,rebin_min,rebin_max):
    energy_bin=['0.3 1.0','1.0 10.0','0.3 10.0']
    wt=open('xspec_com.dat','w')
    command_start='data 1:1 '+name+'\n'+'cpd '+name[0:13]+'.ps/ps'+'\n'+'ignore bad'+'\n'+'ignore **-'+energy_bin[energy]+'-**'+'\n'
    command_plot='setpl energy'+'\n'+'setplot rebin '+rebin_min+' '+rebin_max+'\n'+'plot ld'+'\n'
    command_model='model '+model[0]+'\n'
    for i in xrange(1,len(model)):
        command_model += model[i]+'\n'
    command_fit='stati cstat'+'\n'+'fit'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'plot'+'\n'
    command_save='cpd none'+'\n'
    command_exit='exit'+'\n'
    commands=command_start+command_plot+command_model+command_fit+command_save+command_exit
    wt.write(commands)
    wt.close()
    cmd='export HEADAS=%s ; . %s/headas-init.sh ; . %s/data/swift/software/tools/caldbinit.sh ; cat xspec_com.dat | xspec > %s.dat' % (heas_dest(home_dir),heas_dest(home_dir),home_dir,name[0:13])
    proc = Popen(cmd , shell=True , stdout=PIPE , stderr=PIPE)
    #proc=os.system(cmd)
    proc.wait()
    res=proc.communicate()
    print res[1]
    open_ps=os.system('okular '+name[0:13]+'.ps')

def diskbb(name,model,energy):
    (e_min,e_max)=(min(energy,4-2*energy),min(energy+1,6-2*energy))
    en_ran=[0.3**(4.0/3.0),1.0**(4.0/3.0),10.0**(4.0/3.0)]
    dat=name[0:13]+'.dat'
    rd=open(dat,'r').read()
    text=[[col for col in line.split(' ') if col!=''] for line in rd.split('\n')]
    (tin,norm)=('','')
    for i in xrange(len(text)):
        for j in xrange(len(text[i])):
            if text[i][j]=='Tin':
                if float(text[i][j+2])!=float(model[1]):
                    tin=text[i][j+2]
                    sig_tin=text[i][j+4]
            if text[i][j]=='norm':
                if float(text[i][j+1])!=float(model[2]):
                    norm=text[i][j+1]
                    sig_norm=text[i][j+3]
    h=6.62*10**(-27)     #erg*sec
    c=3*10**(10)         #cm/sec
    pi_q=(16*math.atan(1.0))**2 #16*pi^2
    kt_h=(float(tin)/(4.136*10**(-18.0)))**(8.0/3.0) #(kt/h)^8/3, keV/(keV*sec)
    dim=((1.6*10**(-9.0))**(4.0/3.0))*(206264.8*149.6*10**10)**(-2) #(10kpc/1km)^2*erg^4/3
    flux=(3.0*(float(norm)**2.0)*pi_q*dim/(4*c**2))*kt_h*(en_ran[e_max]-en_ran[e_min])*h**(-1.0/3.0)
    print tin,norm,flux

def compLS(name,model):
    dat=name[0:13]+'.dat'
    rd=open(dat,'r').read()
    text=[[col for col in line.split(' ') if col!=''] for line in rd.split('\n')]
    (kt,tau,norm)=('','','')
    for i in xrange(len(text)):
        for j in xrange(len(text[i])):

            if text[i][j]=='kT':
                if float(text[i][j+2])!=float(model[1]):
                    kt=text[i][j+2]
                    sig_kt=text[i][j+4]
            
            if text[i][j]=='tau':
                if float(text[i][j+1])!=float(model[2]):
                    tau=text[i][j+1]
                    sig_tau=text[i][j+3]
            
            if text[i][j]=='norm':
                if float(text[i][j+1])!=float(model[3]):
                    norm=text[i][j+1]
                    sig_norm=text[i][j+3]

    print kt,tau,norm

if __name__=='__main__':
    direct=os.getcwd()
    home_dir='/home/'+getpass.getuser()
    name='n_spec_00090041003.pha'
    rebin_min='20'
    rebin_max='15'
    energy=2
    model=['diskbb','0.1','0.04']
    model2=['disk','0.1','10.0','1.01','0.1']
    exit_='n'
    while exit_=='n':
        
        try:
            os.remove(name[0:13]+'.ps')
            os.remove('xspec_com.dat')
        except:
            pass
        Xspec(direct,home_dir,name,model2,energy,rebin_min,rebin_max)
        exit_=raw_input('Would you like stop it[y/n]:')
    diskbb(name,model,energy)
