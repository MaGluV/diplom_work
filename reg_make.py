import os
import shutil
import glob
from subprocess import Popen, PIPE
from astropy.io import fits

def make_filter(name_file,ra,dec):
    cmd = 'ds9 %s' % name_file
    proc = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    proc.wait()
    res=proc.communicate()
    if proc.returncode:
        r=res[1]
    else:
        r=res[0]
    filt=glob.glob('*.reg')
    print filt
    for i in filt:
        print i
        filt_read=open(i,'r').read()
        c=filt_read.split('\n')
        print c[3][6:].replace(',',':').replace('(',' ').replace(')',' ').replace('"',' ')
        rd=c[3][6:].replace(',',':').replace('(',' ').replace(')',' ').replace('"',' ')
        ra_dec=rd.split(':')
        if float(ra_dec[0])>=0:
            ra_1=float(ra_dec[0])+float(ra_dec[1])/60+float(ra_dec[2])/3600
        else:
            ra_1=float(ra_dec[0])-float(ra_dec[1])/60-float(ra_dec[2])/3600
        print float(ra_dec[3])
        if float(ra_dec[3])>=0:
            dec_1=float(ra_dec[3])+float(ra_dec[4])/60+float(ra_dec[5])/3600
        else:
            dec_1=float(ra_dec[3])-float(ra_dec[4])/60-float(ra_dec[5])/3600
        radius1=float(ra_dec[6])/(1.0*3600.0)
        print abs(ra_1-ra),'  ',abs(dec_1-dec),'  ',radius1 
        if (abs(ra_1-ra)<radius1/15.0):
            if (abs(dec_1-dec)<radius1):
                os.rename(i,name_file+'lc.reg')
            else:
                os.rename(i,name_file+'bkg.reg')
        else:
            os.rename(i,name_file+'bkg.reg')
    return r

def make_filter2(ref_file,ra,dec):
    make_filter(ref_file,ra,dec)
    fits_source = fits.open(ref_file)
    x_ref = fits_source["EVENTS"].header["RA_OBJ"]
    y_ref = fits_source["EVENTS"].header["DEC_OBJ"]
    fits_source.close()
    list_files = glob.glob('*.evt')
    for name in list_files:
        if name != ref_file:
            fits_source = fits.open(name)
            x_obj = fits_source["EVENTS"].header["RA_OBJ"]
            y_obj = fits_source["EVENTS"].header["DEC_OBJ"]
            fits_source.close()
            dx = x_obj - x_ref
            dy = y_obj - y_ref
            rd_obj = open(ref_file + 'lc.reg','r').read()
            i = 0
            word = rd_obj[i:i+6]
            while word != 'circle':
                i += 1
                word = rd_obj[i:i+6]
            ra_dec = rd_obj[i+7:len(rd_obj)-2].split(',')
            ra_sym = ra_dec[0].split(':')
            if float(ra_sym[0])>=0:
                ra_ref = float(ra_sym[0])*15 + float(ra_sym[1])/4.0 + float(ra_sym[2])/240.0
            else:
                ra_ref = float(ra_sym[0])*15 - float(ra_sym[1])/4.0 - float(ra_sym[2])/240.0
            ra_real = ra_ref + dx
            ra_real_sym = str(int(ra_real/15))+':'+str(abs(int(60*(ra_real/15-int(ra_real/15)))))+':'+str(abs(60*(60*(ra_real/15-int(ra_real/15))-int(60*(ra_real/15-int(ra_real/15))))))
            dec_sym = ra_dec[1].split(':')
            if float(dec_sym[0])>=0:
                dec_ref = float(dec_sym[0]) + float(dec_sym[1])/60.0 + float(dec_sym[2])/3600.0
            else:
                dec_ref = float(dec_sym[0]) - float(dec_sym[1])/60.0 - float(dec_sym[2])/3600.0
            dec_real = dec_ref + dy
            dec_real_sym = str(int(dec_real))+':'+str(abs(int(60*(dec_real-int(dec_real)))))+':'+str(abs(60*(60*(dec_real-int(dec_real))-int(60*(dec_real-int(dec_real))))))
            #print name,' ',(ra_real_sym,dec_real_sym),' ',(dx,dy)
            wrtbl = rd_obj[0:i+7] + ra_real_sym + ',' + dec_real_sym + ',' + ra_dec[2] + ')'
            wt_obj = open(name + 'lc.reg','w').write(wrtbl)

            rd_bkg = open(ref_file + 'bkg.reg','r').read()
            i = 0
            word = rd_bkg[i:i+6]
            while word != 'circle':
                i += 1
                word = rd_bkg[i:i+6]
            ra_dec = rd_bkg[i+7:len(rd_obj)-2].split(',')
            ra_sym = ra_dec[0].split(':')
            if float(ra_sym[0])>=0:
                ra_ref = float(ra_sym[0])*15 + float(ra_sym[1])/4.0 + float(ra_sym[2])/240.0
            else:
                ra_ref = float(ra_sym[0])*15 - float(ra_sym[1])/4.0 - float(ra_sym[2])/240.0
            ra_real = ra_ref + dx
            ra_real_sym = str(int(ra_real/15))+':'+str(abs(int(60*(ra_real/15-int(ra_real/15)))))+':'+str(abs(60*(60*(ra_real/15-int(ra_real/15))-int(60*(ra_real/15-int(ra_real/15))))))
            dec_sym = ra_dec[1].split(':')
            if float(dec_sym[0])>=0:
                dec_ref = float(dec_sym[0]) + float(dec_sym[1])/60.0 + float(dec_sym[2])/3600.0
            else:
                dec_ref = float(dec_sym[0]) - float(dec_sym[1])/60.0 - float(dec_sym[2])/3600.0
            dec_real = dec_ref + dy
            dec_real_sym = str(int(dec_real))+':'+str(abs(int(60*(dec_real-int(dec_real)))))+':'+str(abs(60*(60*(dec_real-int(dec_real))-int(60*(dec_real-int(dec_real))))))
            #print name,' ',(ra_real_sym,dec_real_sym),' ',(dx,dy)
            wrtbl = rd_bkg[0:i+7] + ra_real_sym + ',' + dec_real_sym + ',' + ra_dec[2] + ')'
            wt_obj = open(name + 'bkg.reg','w').write(wrtbl)
            
 
if __name__=='__main__':
    make_filter2("sw00031442004xpcw3po_cl.evt",3.3061,-66.60056)
