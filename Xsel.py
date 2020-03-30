#!/usr/bin/python    

import os,glob
from astropy.io import fits

def radius(name):
    filt=open(name,'r').read()
    c=filt.split('\n')
    rd=c[3][6:].replace(',',':').replace('(',' ').replace(')',' ').replace('"',' ')
    ra_dec=rd.split(':')
    return float(ra_dec[6])

def make_param(name_dir,energy):
    os.chdir(name_dir)
    dir_list=os.listdir(name_dir)
    names = glob.glob('*xpcw*po_cl.evt')
    
    for name in names:
        print name,' ',name_dir,' ',energy
        rad_lc=radius(name+'lc.reg')
        rad_bkg=radius(name+'bkg.reg')
        areas_ratio=(rad_lc/rad_bkg)**2
        ft=fits.open(name)
        time=3
        dat_file='param'+name[2:13]+'.dat'
        wt=open(dat_file,'w')
        namec_lc='curve_'+name[2:13]+'.lc'
        namec_bkg='bkg_'+name[2:13]+'.lc'
        namec_spec='spec_'+name[2:13]+'.pha'
        namec_sp_bkg='sp_bkg_'+name[2:13]+'.pha'
        commands_filter='xsel'+'\n'+'read events'+' '+name+'\n'+'.//'+'\n'+'yes'+'\n'#+'extract image'+'\n'+'save image image_'+name[2:13]+'.img'+'\n'
        commands_lc='filter region ' + name + 'lc.reg'+'\n'+'filter pha_cutoff '+energy+'\n'+'set binsize '+str(time)+'\n'+'extract curve'+'\n'+'save curve '+namec_lc+'\n'+'clear region'+'\n'
        commands_bkg='filter region ' + name + 'bkg.reg'+'\n'+'extract curve'+'\n'+'save curve '+namec_bkg+'\n'+'clear region'+'\n'#'set binsize '+str(time)+'\n'+
        commands_spectr='filter region ' + name + 'lc.reg'+'\n'+'extract spectrum'+'\n'+'save spectrum '+namec_spec+'\n'+'clear region'+'\n'
        commands_sp_bkg='filter region ' + name + 'bkg.reg'+'\n'+'extract spectrum'+'\n'+'save spectrum '+namec_sp_bkg+'\n'+'clear region'+'\n'
        end='exit'+'\n'+'no'+'\n'
        sum_command=commands_filter+commands_spectr+commands_sp_bkg+commands_lc+commands_bkg+end
        wt.write(sum_command)
        wt.close()
        reduc='reduc'+name[2:13]+'.dat'
        wt=open(reduc,'w')
        bkg_reduc=namec_lc+'\n'+namec_bkg+'\n'+'red_'+namec_lc+'\n'+'1'+'\n'+str(areas_ratio)+'\n'+'no'+'\n'
        wt.write(bkg_reduc)
        wt.close()
        
def level2(dir_name,home_dir,dat_name,reduc):
    os.chdir(home_dir)
    heas_dir = glob.glob('heasoft-*')
    os.chdir(home_dir + '/' + heas_dir[0])
    init_dir = glob.glob('x86_64-*')
    final_dest = home_dir + '/' + heas_dir[0] + '/' + init_dir[0]
    os.chdir(dir_name)
    cmd = 'export HEADAS=%s ;. %s/headas-init.sh;cat %s | xselect ' % (final_dest,final_dest,dat_name)
    proc = os.system(cmd)
    cmd1 = 'export HEADAS=%s ;. %s/headas-init.sh;cat %s | lcmath ' % (final_dest,final_dest,reduc)
    proc1 = os.system(cmd1)
    lc = glob.glob('*'+dat_name[5:16]+'*lc.reg')
    bkg = glob.glob('*'+dat_name[5:16]+'*bkg.reg')
    os.remove(lc[0])
    os.remove(bkg[0])

if __name__ == '__main__':

    name="/home/max/Documents/SAO_pract/Second_shot" #raw_input('input name:')
    i=2 #input('input_energy(1,2 or 3:)')
    energy=["30 100","100 1000","30 1000"]
    home_dir="/home/max" #raw_input('home_dir:')

    os.chdir(name)
    try:
        bk=glob.glob('bkg_*.lc')
        cu=glob.glob('curve_*.lc')
        for i in xrange(len(bk)):
            os.remove(bk[i])
            os.remove(cu[i])
        rd_cu=glob.glob('red_curve_*.lc')
        for name_rd in rd_cu:
            os.remove(name_rd)
        os.remove('xselect.log')
    except:
        pass
    make_param(name,energy[i-1])
    log_existing=glob.glob('xselect.log')
    dat_names=glob.glob('param*.dat')
    i=0
    for dat_name in dat_names:
        reduc=dat_name.replace('param','reduc')
        try :
            if log_existing[0] == 'xselect.log':
                os.remove('xselect.log')
                level2(name,home_dir,dat_name,reduc)
        except:
            level2(name,home_dir,dat_name,reduc)
        os.remove(dat_name)
        os.remove(reduc)
        i=i+1
        procent=i*100/float(len(dat_names))
        print procent,"%"
