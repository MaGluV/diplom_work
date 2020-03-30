#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from subprocess import Popen,PIPE
import os,shutil,glob,errno,reg_make,Xsel,download,getpass,read_fits,graph,make_spec,dcf,mod

class Window:
    def __init__(self):
        self.tk=Tk()
        self.uniqKeys = {}
        self.list_names = {}
        self.serv=' '#"http://relay.sao.ru:8080"

        self.var=IntVar()
        self.var.set(1)

        self.grd=IntVar()
        self.grd.set(3)

        self.lab("Create light curve:",1,0)

        self.lab("RA",2,0)
        self.mainwindow("0:0:0","ra",2,1)
        
        self.lab("Dec",3,0)
        self.mainwindow("0:0:0","dec",3,1)
        
        self.lab("radius",2,2)
        self.mainwindow("1","radius",2,3)
        
        self.lab("DIRECT",3,2)
        self.main_dir=os.getcwd()
        self.mainwindow(self.main_dir,"direct",3,3)

        self.button("OK",5,1,self.get_id)
        
        self.button("Create *.reg",5,3,self.create)

        self.R1=Radiobutton(text="0.3-1.0 keV",variable=self.var,value=1)
        self.R1.grid(row = 6,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.R2=Radiobutton(text="1.0-10.0 keV",variable=self.var,value=2)
        self.R2.grid(row = 7,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.R3=Radiobutton(text="0.3-10.0 keV",variable=self.var,value=3)
        self.R3.grid(row = 8,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.checkbutton("Time binning","n","bin",6,1)

        self.lab("Set time bin(days):",7,1)

        self.mainwindow("1.0","time_bin",8,1)

        self.button("OK",7,3,self.lev2_reduction)

        self.button("Plot light curve",8,3,self.mk_gr)

        self.lab("Create spectrum:",9,0)

        self.R1=Radiobutton(text="Grade 0",variable=self.grd,value=1)
        self.R1.grid(row = 10,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.R2=Radiobutton(text="Grade 0 to 4",variable=self.grd,value=2)
        self.R2.grid(row = 11,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.R3=Radiobutton(text="Grade 0 to 12",variable=self.grd,value=3)
        self.R3.grid(row = 12,column = 0,rowspan = 1,columnspan = 1,sticky = W+N+S+E)

        self.lab("CALDB",10,1)
        self.cald='/home/'+getpass.getuser()
        self.mainwindow(self.cald,"caldb",10,2)

        self.lab("Group min",11,1)
        self.mainwindow("1","min",11,2)

        self.button("Download",10,3,self.spec)

        self.button("OK",11,3,self.create_spec)

        self.lab("Rebin min",13,0)
        self.mainwindow("20","rebin_min",14,0)

        self.lab("Rebin max",13,1)
        self.mainwindow("15","rebin_max",14,1)

        self.lab("Models",13,2)
        lst=['diskbb+wabs*po','diskbb+wabs*compLS']
        self.lsbox(1,3,SINGLE,14,2,1,1,lst,self.open_window,"model")

        self.button("Get flux",15,0,self.flux_plot)

    def lab(self , lab_name , size_row , size_col):        #metki
        lab_n = Label(text = lab_name)
        lab_n.grid(row = size_row , column = size_col)
    def mainwindow(self,value,uniqKey,size_row,size_col):  #tekstovye polya
        C = StringVar()
        C.set(value)
        self.uniqKeys[ uniqKey ] = Entry(textvariable = C , width = 10 , bg = "white")
        self.uniqKeys[ uniqKey ].grid(row = size_row , column = size_col)
    def button(self , name , size_row , size_col , name_func): #knopki
        but = Button(text = name , pady = 10)
        but.grid(row = size_row , column = size_col , rowspan = 1 , columnspan = 1 , sticky = W+N+S+E)
        b=but.bind("<Button-1>",name_func)
    def checkbutton(self , name , value , uniqKey , size_row , size_col): #tumblery
        self.uniqKeys[ uniqKey ] = StringVar()
        self.uniqKeys[ uniqKey ].set(value)
        check = Checkbutton(variable = self.uniqKeys[ uniqKey ] , onvalue = "y" , offvalue = "n" , text = name)
        check.grid(row=size_row,column=size_col,rowspan=1,columnspan=1,sticky=W+N+S+E)
    def lsbox(self,height,width,selectmode,size_row,size_col,row,col,lst,function,name): #spisok 
        listbox=Listbox(height=height,width=width,selectmode=selectmode)
        scrollbar = Scrollbar(self.tk)
        self.list_names[name]=listbox
        for name in lst:
            listbox.insert(END,name)
        listbox.bind("<<ListboxSelect>>",function)
        listbox.grid(row=size_row,column=size_col,rowspan=row,columnspan=col,sticky=W+N+S+E)
        scrollbar.grid(row=size_row,column=size_col+col,rowspan=row,columnspan=col,sticky=W+N+S)#+E)
        scrollbar.config(command=listbox.yview)
        listbox['yscrollcommand'] = scrollbar.set
    def get_id(self , event):                           #poluchayu spisok id nablyudeniy
        cmd = "export http_proxy=%s;export ftp_proxy=%s;perl browse_extract_wget.pl table=swiftmastr position=\"%s %s\" coordinates=EQUATORIAL radius=\"%s\" format=batch resultmax=\"0\" > %s/id.dat" % (self.serv,self.serv,self.uniqKeys[ "ra" ].get().replace(':',' '),self.uniqKeys[ "dec" ].get().replace(':',' '),self.uniqKeys[ "radius" ].get(),self.uniqKeys[ "direct" ].get())
        proc = Popen(cmd , shell=True , stdout=PIPE)
        proc.wait()
        res = proc.communicate()
        print res[0]
        r=open('id.dat','r').read()
        print r
        self.ls_id()
        return self.tk.destroy
    def ls_id(self):                                    #zagruzhayu *.cl (level 2) faily s servera po id i date nablyudeniya
        rd=open('id.dat','r').read()
        s=rd.split('\n')
        n=len(s)-4
        c=[s[i+2].split('|') for i in range(n)]
        f=[c[i][5][0:7].replace('-','_') for i in range(n)]
        for i in xrange(n):
            print self.serv,' ',f[i],' ',c[i][2]
            download.event(self.serv,f[i],c[i][2])
        archive=glob.glob('*.evt.gz')
        for name_zip in archive:
            cmd1 = "gunzip %s" % (name_zip)
            proc1 = os.system(cmd1)
            print name_zip,' ',proc1
    def lev2_reduction(self,event):                     # cherez XSELECT stroyu spectry i crivie bleska
        energy=["30 100","100 1000","30 1000"]
        input_energy=energy[self.var.get()-1]
        print input_energy
        names=['bkg_*.lc','curve_*.lc','spec_*.pha','sp_bkg_*.pha','n_spec_*.pha','red_curve_*.lc']
        for name in names:
            try:
                file_=glob.glob(name)
                for name_ in file_:
                    print name_
                    os.remove(name_)
            except:
                pass
        try:
            os.remove('xselect.log')
        except:
            pass

        Xsel.make_param(self.uniqKeys[ "direct" ].get(),input_energy)

        log_existing=glob.glob('xselect.log')
        home='/home/%s' % getpass.getuser()
        dat_names=glob.glob('param*.dat')
        for dat_name in dat_names:
            reduc=dat_name.replace('param','reduc')
            try :
                if log_existing[0] == 'xselect.log':
                    os.remove('xselect.log')
                    Xsel.level2(self.uniqKeys[ "direct" ].get(),home,dat_name,reduc)
            except:
                Xsel.level2(self.uniqKeys[ "direct" ].get(),home,dat_name,reduc)
            os.remove(dat_name)
            os.remove(reduc)

    def open_image(self,event):                        # spomoshchyu ds9 otkryvayu fail iz spiska i sozdayu *.reg faily dlya obyecta i fona
        ra_str=self.uniqKeys[ "ra" ].get().split(':')
        dec_str=self.uniqKeys[ "dec" ].get().split(':')
        if float(ra_str[0])>=0:
            ra=float(ra_str[0])+float(ra_str[1])/60.0+float(ra_str[2])/3600.0
        else:
            ra=float(ra_str[0])-float(ra_str[1])/60.0-float(ra_str[2])/3600.0
        if float(dec_str[0])>=0:
            dec=float(dec_str[0])+float(dec_str[1])/60.0+float(dec_str[2])/3600.0
        else:
            dec=float(dec_str[0])-float(dec_str[1])/60.0-float(dec_str[2])/3600.0
        image=self.list_names["image"].get(self.list_names["image"].curselection())
        print image,ra,dec
        reg_make.make_filter2(image,ra,dec)

    def create(self,event):                             #sozdayu spisok s imenami failov
        list_n=glob.glob('*.evt')
        self.lsbox(15,25,SINGLE,1,4,8,8,list_n,self.open_image,"image")
    def mk_gr(self,event):                              # biniruyu krivie bleska (s fiksirovannym shagom ili po GTI) i vivozhu na ekran rezultat v vide grafika
        if self.uniqKeys[ "bin" ].get()=='n':
            read_fits.one_event()
            read_fits.sort('all')
        else:
            read_fits.rebin(float(self.uniqKeys[ "time_bin" ].get()))
            read_fits.sort('bin')
        graph.plot_gr()
    def spec(self,event):                               #zagruzhayu faily dlya sozdaniya *.arf failov i kopiruyu *.rmf iz CALDB
        rd=open('id.dat','r').read()
        s=rd.split('\n')
        n=len(s)-4
        c=[s[i+2].split('|') for i in range(n)]
        f=[c[i][5][0:7].replace('-','_') for i in range(n)]
        for i in range(n):
            dcf.files(self.serv,f[i],c[i][2])
            grade=["0","0to4","0to12"]
            dcf.search_rmf(self.uniqKeys["caldb"].get(),grade[self.grd.get()-1],f[i],c[i][2])
        archive=glob.glob("*.fits.gz")
        for i in archive:
            cmd = "gunzip %s" % i
            proc = os.system(cmd)
            print i,' ',proc
        archive1=glob.glob("*.hk.gz")
        for i in archive1:
            cmd = "gunzip %s" % i
            proc = os.system(cmd)
            print i,' ',proc
    def create_spec(self,event):              #sozdayu arf        
        home_dir='/home/'+getpass.getuser()
        file_names=glob.glob('sw*xpcw*po_cl.evt')
        current=os.getcwd()
        for file_ in file_names:
            name_at=file_[0:13]+'*at.fits'
            print current
            try:
                at=current+'/'+glob.glob(name_at)[0]
                print at
            except:
                pass
            hd=current+'/'+file_[0:13]+'xhd.hk'
            arf=current+'/'+file_[0:13]+'.arf'
            pha=current+'/'+'spec_'+file_[2:13]+'.pha'
            bkg=current+'/'+'sp_bkg_'+file_[2:13]+'.pha'
            img=current+'/'+file_[0:21]+'ex.img'
            img_arc=current+'/'+file_[0:21]+'rawinstr.img.gz'
            min_=self.uniqKeys["min"].get()
            rmf=current+'/'+file_[0:13]+'.rmf'
            #try:
            #    if glob.glob(arf)[0] == arf:
            #        os.remove(arf)
            #        print arf,'removed'
            #except:
            #    pass
            #try:
            #    if glob.glob(img)[0] == img:
            #        os.remove(img)
            #        print img,'removed'
            #except:
            #    pass
            #try:
            #    if glob.glob(img_arc)[0] == img_arc:
            #        os.remove(img_arc)
            #        print img_arc,'removed'
            #except:
            #    pass
            #try:
            #    new='n_'+pha
            #    if glob.glob(new)[0] == new:
            #        os.remove(new)
            #        print new,'removed'
            #except:
            #    pass
            arf_ex=glob.glob('*.arf')
            try:
                i=0
                while arf_one[i]!=arf:
                    i += 1
                print '%s exist' % arf_one[i]
            except:
                try:
                    out=make_spec.exp_map(home_dir,self.uniqKeys["caldb"].get(),file_,at,hd)
                except:
                    print '*at not founded'
                    out=1
                    pass
                if out==0:
                    make_spec.arf_build(home_dir,self.uniqKeys["caldb"].get(),arf,pha,img)
                else:
                    make_spec.arf_without_expomap(home_dir,self.uniqKeys["caldb"].get(),arf,pha)
            make_spec.grppha(current,home_dir,pha,min_,bkg,arf,rmf)
            print "created %s" % file_[0:13]
                    
    def open_window(self,event):    #s pomoshchyu Xspec approximiruyu odnoy iz modeley : diskbb+wabs*po ili diskbb+wabs*compLS
        os.chdir(self.uniqKeys["direct"].get())
        name=self.list_names["model"].get(self.list_names["model"].curselection())
        direct=self.uniqKeys["direct"].get()
        var=self.var.get()
        new_win = Toplevel(self.tk)
        mod.run_window(new_win,name,direct,var,self.uniqKeys["rebin_min"].get(),self.uniqKeys["rebin_max"].get())
    def flux_plot(self,event):      #vychislyayu potoki i vivozhu resultat v vide grafika
        if self.uniqKeys[ "bin" ].get()=='n':
            read_fits.convert()
            graph.plot_flux("curve")
        else:
            read_fits.convert_rebin1(float(self.uniqKeys[ "time_bin" ].get()))
            graph.plot_flux("bin")
        
win=Window()
win.tk.title('LC')
win.tk.mainloop()
