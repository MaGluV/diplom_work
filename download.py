import urllib,urllib2
def event(proxy_name,data,obs_id):
    url="ftp://legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/xrt/event/" % (data,obs_id)
    print url
    proxies = {"http": proxy_name,"ftp": proxy_name}
    try:
        data=urllib.urlopen(url,proxies=proxies).readlines()
    except:
        try:
            data=urllib2.urlopen(url).readlines()
        except urllib2.URLError:
            pass
    for line in data:
        try :
            praw=parse_raw(line)
            name=find_file(praw)
            if name[14:16]=="pc":
                if name[21:23]=="cl":
                    url1=url+name
                    try:
                        try:
                            data1=urllib.urlopen(url1,proxies=proxies).read()
                        except:
                            data1=urllib2.urlopen(url1).read()    
                        with open(name, "wb") as code:
                            code.write(data1)
                    except urllib2.URLError:
                        pass
        except:
            pass

def parse_raw(raw):
    new_raw=raw.split(' ')
    mas=[string for string in new_raw if string!='']
    return mas
def find_file(raw):
    j=0
    while raw[j][0:2]!='sw':
        j += 1
    return raw[j][0:len(raw[j])-2]
    
if __name__=='__main__':
    #data='2015_04' #raw_input('Input start time:')
    #obs_id='00092116003' #raw_input('Input obs_id:')
    proxy_name=' ' #raw_input('Input proxy_name:')
    #event(proxy_name,data,obs_id)
    rd=open('id.dat','r').read()
    s=rd.split('\n')
    n=len(s)-4
    c=[s[i+2].split('|') for i in range(n)]
    f=[c[i][5][0:7].replace('-','_') for i in range(n)]
    for i in xrange(n):
        print proxy_name,' ',f[i],' ',c[i][2]
        event(proxy_name,f[i],c[i][2])
