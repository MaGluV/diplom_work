import urllib,urllib2,os,glob,shutil
from astropy.io import fits
def files(proxy_name,data,obs_id):
    url1="ftp://legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/auxil/" % (data,obs_id)
    url2="ftp://legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/xrt/hk/" % (data,obs_id)
    proxies = {"http": proxy_name,"ftp": proxy_name}
    try:
        try :
            data=urllib.urlopen(url1,proxies=proxies).readlines()
        except:
            try:
                data=urllib2.urlopen(url1).readlines()
            except urllib2.URLError:
                pass
        name='sw'+obs_id+'*cl.evt'
        files=glob.glob(name)
        attfile={'100':'sat','110':'pat'}#,'111':'uat','101':'uat'}
        try:
            data2=urllib.urlopen(url2,proxies=proxies).readlines()
        except:
            data2=urllib2.urlopen(url2).readlines()
        for file_ in files:
            rd=fits.open(file_)
            attflag=rd["EVENTS"].header["attflag"]
            try:
                print attfile[attflag],attflag,file_
            except:
                print attflag,file_
            for line in data:
                try :
                    praw=parse_raw(line)
                    name=find_file(praw)
                    if name[13:16]==attfile[str(attflag)]:
                        url_d1=url1+name
                        try:
                            data1=urllib.urlopen(url_d1,proxies=proxies).read()
                            proc1 = os.system(open_file(name,data1))
                        except:
                            try:
                                data1=urllib2.urlopen(url_d1).read()
                                proc1 = os.system(open_file(name,data1))
                            except urllib2.URLError:
                                 pass
                except:
                    pass
    
            for line in data2:
                if (attflag!="111") or (attflag!="101"): 
                    try :
                        praw=parse_raw(line)
                        name=find_file(praw)
                        if name[13:16]=="xhd":
                            url_d2=url2+name
                            try:
                                data2=urllib.urlopen(url_d2,proxies=proxies).read()
                                proc1 = os.system(open_file(name,data2))
                            except:
                                try:
                                    data2=urllib2.urlopen(url_d2).read()
                                    proc1 = os.system(open_file(name,data2))
                                except urllib2.URLError:
                                    pass
                    except:
                        pass
    except:
        pass

def search_rmf(caldb,grade,data,obs_id):
    dir_n=os.getcwd()+'/'
    #print dir_n 
    path="%s/data/swift/xrt/cpf/rmf/" % caldb
    os.chdir(path)
    name="swxpc"+grade+"*.rmf"
    rmfs=glob.glob(name)
    rmfs_sort=sorted(rmfs)
    rmfs_dat=[name.split('_') for name in rmfs_sort]
    #print rmfs_dat
    i=len(rmfs_dat)-1
    t0=float(data[0:4])
    t1=float(rmfs_dat[i-1][1][0:4])
    print t0,t1
    while t0<=t1:
        i=i-1
        t1=float(rmfs_dat[i][1][0:4])
    name_cur=path+rmfs_sort[i]
    name_dest=dir_n+rmfs_sort[i]
    print name_cur,name_dest
    shutil.copy(name_cur,name_dest)
    os.chdir(dir_n)
    new_name='sw'+obs_id+'.rmf'
    os.rename(rmfs_sort[i],new_name)

def parse_raw(raw):
    new_raw=raw.split(' ')
    mas=[string for string in new_raw if string!='']
    return mas
def find_file(raw):
    j=0
    while raw[j][0:2]!='sw':
        j += 1
    return raw[j][0:len(raw[j])-2]

def open_file(name,data):
    print name
    with open(name, "wb") as code:
        code.write(data)
        cmd1 = "gunzip %s" % (name)
    return cmd1
                
if __name__=='__main__':
    data="2008_04"#raw_input('Input start time:')
    obs_id="00090041003"#raw_input('Input obs_id:')
    proxy_name="http://relay.sao.ru:8080"#raw_input('Input proxy_name:')
    #files(proxy_name,data,obs_id)
    caldb="/home/max"
    g=input('Input grade(0,1 or 2):')
    grade=["0","0to4","0to12"]
    search_rmf(caldb,grade[g],data,obs_id)
