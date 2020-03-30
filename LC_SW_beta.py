#!/usr/bin/python

from Tkinter import *
from subprocess import Popen,PIPE
import os,shutil,glob,errno,reg_make,Xsel

class Window:
    def __init__(self):
        self.tk=Tk()
        self.uniqKeys = {}
        self.serv="http://relay.sao.ru:8080"
        self.lab("RA",2,0)
        self.mainwindow("0:0:0","ra",2,1)
        self.var=IntVar()
        self.var.set(1)
        
        self.lab("Dec",3,0)
        self.mainwindow("0:0:0","dec",3,1)
        
        self.lab("radius",4,0)
        self.mainwindow("1","radius",4,1)
        
        self.lab("DIRECT",2,2)
        self.main_dir=os.getcwd()
        self.mainwindow(self.main_dir,"direct",2,3)
        
        self.lab("CALDB",3,2)
        self.mainwindow(self.main_dir,"caldb",3,3)

        self.button("OK",5,1,self.get_id)

        self.R1=Radiobutton(text="0.3-1.0 keV",variable=self.var,value=1)
        self.R1.grid(row = 6,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.R2=Radiobutton(text="1.0-10.0 keV",variable=self.var,value=2)
        self.R2.grid(row = 7,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.R3=Radiobutton(text="0.3-10.0 keV",variable=self.var,value=3)
        self.R3.grid(row = 8,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.lab("Bin length",6,1)
        self.mainwindow("10","binsize",6,2)

        self.button("OK",7,1,self.lev2_reduction)

    def lab(self , lab_name , size_row , size_col):
        lab_n = Label(text = lab_name)
        lab_n.grid(row = size_row , column = size_col)
    def mainwindow(self,value,uniqKey,size_row,size_col):
        C = StringVar()
        C.set(value)
        self.uniqKeys[ uniqKey ] = Entry(textvariable = C , width = 10 , bg = "white")
        self.uniqKeys[ uniqKey ].grid(row = size_row , column = size_col)
    def button(self , name , size_row , size_col , name_func):
        but = Button(text = name , pady = 10)
        but.grid(row = size_row , column = size_col , rowspan = 1 , columnspan = 1 , sticky = W+N+S+E)
        b=but.bind("<Button-1>",name_func)
    def checkbutton(self , name , value , size_row , size_col):
        C = StringVar()
        C.set(value)
        check = Checkbutton(variable = C , onvalue = "y" , offvalue = "n" , text = name)
        check.grid(row=size_row,column=size_col,rowspan=1,columnspan=1,sticky=W+N+S+E)
        return C.get()
    def get_id(self , event):
        cmd = "export http_proxy=%s;export ftp_proxy=%s;perl browse_extract_wget.pl table=swiftmastr position=\"%s %s\" coordinates=EQUATORIAL radius=\"%s\" format=batch > %s/id.dat" % (self.serv,self.serv,self.uniqKeys[ "ra" ].get().replace(':',' '),self.uniqKeys[ "dec" ].get().replace(':',' '),self.uniqKeys[ "radius" ].get(),self.uniqKeys[ "direct" ].get())
        proc = Popen(cmd , shell=True , stdout=PIPE)
        proc.wait()
        res = proc.communicate()
        print res[0]
        r=open('id.dat','r').read()
        print r
        #self.ls_id()
        return self.tk.destroy
    def ls_id(self):
        rd=open('id.dat','r').read()
        s=rd.split('\n')
        n=len(s)-4
        c=[s[i+2].split('|') for i in range(n)]
        f=[c[i][5][0:7].replace('-','_') for i in range(n)]
        for i in range(n):
            print f[i],' ',c[i][2],' ',c[i][7]
            cmd1 = "cd %s;export http_proxy=%s;export ftp_proxy=%s; wget --mirror --no-parent ftp://legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/xrt/; wget --mirror --no-parent ftp://legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/auxil/" % (self.uniqKeys[ "direct" ].get(),self.serv,self.serv,f[i],c[i][2],f[i],c[i][2])
            proc1 = Popen(cmd1 , shell=True , stdout=PIPE)
            proc1.wait()
            res1=proc1.communicate()
            if proc1.returncode:
                print "Error"
            else:
                print "Success"
                print res1[0]
            dir_name=os.listdir("%s/legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/xrt" % (self.uniqKeys[ "direct" ].get(),f[i],c[i][2]))
            dir_n=len(dir_name)
            auxil="%s/legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/auxil" % (self.uniqKeys[ "direct" ].get(),f[i],c[i][2])
            xrt_event="%s/legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/xrt/event" % (self.uniqKeys[ "direct" ].get(),f[i],c[i][2])
            xrt_hk="%s/legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/xrt/hk" % (self.uniqKeys[ "direct" ].get(),f[i],c[i][2])
            new_dir=self.uniqKeys[ "direct" ].get()+'/'+c[i][2]    
            try:
                os.mkdir("%s/%s" % (self.uniqKeys[ "direct" ].get(),c[i][2]))
                os.mkdir(new_dir)
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise e
                pass
            print new_dir
            for k in range(dir_n):
                if (dir_name[k] == "hk"):
                    dir_name_xrt_hk=os.listdir("%s/legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/xrt/hk" % (self.uniqKeys[ "direct" ].get(),f[i],c[i][2]))
                    os.chdir(xrt_hk)
                    for name1 in dir_name_xrt_hk:
                        print name1
                        if name1 != "index.html":
                            shutil.move(name1,new_dir)
                if (dir_name[k] == "event"):
                    dir_name_xrt_event=os.listdir("%s/legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/xrt/event" % (self.uniqKeys[ "direct" ].get(),f[i],c[i][2]))
                    os.chdir(xrt_event)
                    for name2 in dir_name_xrt_event:
                        print name2
                        if name2 != "index.html":
                            shutil.move(name2,new_dir)
            
            os.chdir(auxil)
            dir_name_auxil=os.listdir("%s/legacy.gsfc.nasa.gov/swift/data/obs/%s/%s/auxil" % (self.uniqKeys[ "direct" ].get(),f[i],c[i][2]))
            for name in dir_name_auxil:
                print name
                if name != "index.html":
                    shutil.move(name,new_dir)
        rm_dir="%s/legacy.gsfc.nasa.gov/" % self.uniqKeys[ "direct" ].get()
        shutil.rmtree(rm_dir , ignore_errors=True)
    def lev2_reduction(self,event):
        energy=["30 100","100 1000","30 1000"]
        input_energy=energy[self.var.get()-1]
        print input_energy
        print self.uniqKeys[ "ra" ].get()

        ra_str=self.uniqKeys[ "ra" ].get().split(':')
        dec_str=self.uniqKeys[ "dec" ].get().split(':')

        ra=float(ra_str[0])+float(ra_str[1])/60.0+float(ra_str[2])/3600.0
        dec=float(dec_str[0])+float(dec_str[1])/60.0+float(dec_str[2])/3600.0

        name_file=glob.glob("*.evt")
        reg_make.make_filter(name_file[0],ra,dec)# make lc_filter.reg and bkg_filter.reg

        Xsel.make_param(self.uniqKeys[ "direct" ].get(),input_energy,self.uniqKeys[ "binsize" ].get())

        log_existing=glob.glob('xselect.log')
        try :
            if log_existing[0] == 'xselect.log':
                Xsel.retry_level2(self.uniqKeys[ "direct" ].get())
        except:
            Xsel.level2(self.uniqKeys[ "direct" ].get())
    def unzip(self,name):
        cmd1 = "gunzip %s" % (name)
        proc1 = Popen(cmd1 , shell=True , stdout=PIPE)
        proc1.wait()
        res1=proc1.communicate()
        if proc1.returncode:
            print "Error"
        else:
            print "Success"
            print res1[0]

win=Window()
win.tk.title('LC')
win.tk.mainloop()
