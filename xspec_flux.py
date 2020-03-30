from astropy.io import fits
import os,glob,shutil,getpass,math
from subprocess import Popen,PIPE
from make_spec import heas_dest

def Xspec(direct,home_dir,name,model,energy,rebin_min,rebin_max):
    print os.getcwd(),' ',name
    gcwd=os.getcwd()
    energy_bin=['0.3 1.0','1.0 10.0','0.3 10.0']
    wt=open('xspec_com.dat','w')
    command_start='data 1:1 '+name+'\n'+'cpd '+name[0:13]+'.ps/ps'+'\n'+'ignore bad'+'\n'+'ignore **-'+energy_bin[energy]+'-**'+'\n'
    command_plot='setpl energy'+'\n'+'setplot rebin '+rebin_min+' '+rebin_max+'\n'+'plot ld'+'\n'
    command_model='model '+model[0]+'\n'
    for i in xrange(1,len(model)):
        command_model += model[i]+'\n'
    command_fit='stati cstat'+'\n'+'fit'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'\n'+'plot'+'\n'
    command_save='cpd none'+'\n'
    command_flux='flux'+'\n'
    command_exit='exit'+'\n'
    commands=command_start+command_plot+command_model+command_fit+command_save+command_flux+command_exit
    wt.write(commands)
    wt.close()
    cmd='cd %s; export HEADAS=%s ; . %s/headas-init.sh ; . %s/data/swift/software/tools/caldbinit.sh ; cat xspec_com.dat | xspec > %s.dat' % (os.getcwd(),heas_dest(home_dir),heas_dest(home_dir),home_dir,name[0:13])
    proc = Popen(cmd , shell=True , stdout=PIPE , stderr=PIPE)
    #proc=os.system(cmd)
    proc.wait()
    res=proc.communicate()
    print res[1]
    os.chdir(gcwd)
    open_ps=os.system('okular '+name[0:13]+'.ps')

if __name__=='__main__':
    direct=os.getcwd()
    home_dir='/home/'+getpass.getuser()
    name='n_spec_00090041003.pha'
    rebin_min='20'
    rebin_max='15'
    energy=2
    model=['diskbb+wabs*po','1.0','1.0','1e3','-2.0','1.0']
    exit_='n'
    #while exit_=='n':
    #   
    #    try:
    #        os.remove(name[0:13]+'.ps')
    #        os.remove('xspec_com.dat')
    #    except:
    #        pass
    #    Xspec(direct,home_dir,name,model,energy,rebin_min,rebin_max)
    #    exit_=raw_input('Would you like stop it[y/n]:')

    dat=name[0:13]+'.dat'
    rd=open(dat,'r').read()
    text=[[col for col in line.split(' ') if col!=''] for line in rd.split('\n')]
    (kt,tau,norm)=('','','')
    for i in xrange(len(text)):
        for j in xrange(len(text[i])):

            if text[i][j]=='Flux':
                    count=text[i][j+1]
                    flux=text[i][j+3].replace('(','')
    print count,flux
    
