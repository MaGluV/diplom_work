import glob,os,getpass,shutil

def heas_dest(home_dir):
    os.chdir(home_dir)
    heas_dir = glob.glob('heasoft-*')
    os.chdir(home_dir + '/' + heas_dir[0])
    init_dir = glob.glob('x86_64-*')
    final_dest = home_dir + '/' + heas_dir[0] + '/' + init_dir[0]
    return final_dest

def exp_map(home_dir,caldb,file_,sat,hd):
    cmd = 'export HEADASNOQUERY= ; export HEADASPROMPT=/dev/null ; export HEADAS=%s ; . %s/headas-init.sh ; . %s/data/swift/software/tools/caldbinit.sh ; caldbinfo INST SWIFT XRT ; CALDB=%s ; xrtexpomap infile=%s attfile=%s hdfile=%s outdir=./ ' % (heas_dest(home_dir),heas_dest(home_dir),home_dir,caldb,file_,sat,hd) 
    proc = os.system(cmd)
    print proc
    return proc
    
def arf_build(home_dir,caldb,arf,pha,img):
    cmd = 'export HEADASNOQUERY= ; export HEADASPROMPT=/dev/null ; export HEADAS=%s ; . %s/headas-init.sh ; . %s/data/swift/software/tools/caldbinit.sh ; caldbinfo INST SWIFT XRT ; CALDB=%s ; xrtmkarf  outfile=%s phafile=%s expofile=%s srcx=-1 srcy=-1 psfflag=yes ' % (heas_dest(home_dir),heas_dest(home_dir),home_dir,caldb,arf,pha,img)
    proc = os.system(cmd)
    print proc
    
def grppha(curr,home_dir,pha,min_,bkg,arf,rmf):
    pha_n=curr+'/n_'+pha[len(curr)+1:len(pha)]
    commands = pha + '\n' + pha_n + '\n' + 'group min ' + min_ + '\n' + 'chkey backfile ' + bkg + '\n' + 'chkey ancrfile ' + arf + '\n' + 'chkey respfile ' + rmf + '\n' + 'exit' + '\n'
    wt=open('cmd.dat','w')
    wt.write(commands)
    wt.close()
    cmd = 'export HEADAS=%s ;. %s/headas-init.sh; cat cmd.dat | grppha' % (heas_dest(home_dir),heas_dest(home_dir))
    proc=os.system(cmd)
    print proc

def arf_without_expomap(home_dir,caldb,arf,pha):
    print arf,' ',pha,' ',caldb,' ',home_dir,' ',heas_dest(home_dir)
    cmd = 'export HEADASNOQUERY= ; export HEADASPROMPT=/dev/null ; export HEADAS=%s ; . %s/headas-init.sh ; . %s/data/swift/software/tools/caldbinit.sh ; caldbinfo INST SWIFT XRT ; CALDB=%s ; xrtmkarf  outfile=%s phafile=%s srcx=-1 srcy=-1 psfflag=yes expofile=NONE ' % (heas_dest(home_dir),heas_dest(home_dir),home_dir,caldb,arf,pha)
    proc = os.system(cmd)
    print proc
    
if __name__=='__main__':
    home_dir='/home/'+getpass.getuser()
    caldb=home_dir
    file_names=glob.glob('sw*xpcw*po_cl.evt')
    for file_ in file_names:
        name_at=file_[0:13]+'*at.fits'
        
        at=glob.glob(name_at)[0]
        print name_at,' ',os.getcwd(),' ',at
        hd=file_[0:13]+'xhd.hk'
        arf=file_[0:13]+'.arf'
        pha='spec_'+file_[2:13]+'.pha'
        bkg='sp_bkg_'+file_[2:13]+'.pha'
        img=file_[0:21]+'ex.img'
        img_arc=file_[0:21]+'rawinstr.img.gz'
        min_='1'
        rmf=file_[0:13]+'.rmf'
        delete=input('Delete files?[0 or 1]')
        if delete==1:
            try:
                if glob.glob(arf)[0] == arf:
                    os.remove(arf)
                    print arf,'removed'
            except:
                pass
            try:
                if glob.glob(img)[0] == img:
                    os.remove(img)
                    print img,'removed'
            except:
                pass
            try:
                if glob.glob(img_arc)[0] == img_arc:
                    os.remove(img_arc)
                    print img_arc,'removed'
            except:
                pass
            try:
                new='n_'+pha
                if glob.glob(new)[0] == new:
                    os.remove(new)
                    print new,'removed'
            except:
                pass
        print file_
        #exp_map(home_dir,caldb,file_,at,hd)
        #arf_without_expomap(home_dir,caldb,arf,pha)
        #grppha(home_dir,pha,min_,bkg,arf,rmf)
