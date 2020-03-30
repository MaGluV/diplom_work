import os,glob,shutil,math,getpass,xspec_flux
from Tkinter import *
from astropy.io import fits

class New_window():
    def __init__(self,new_win,model,direct,var,min_,max_):
        self.model = model
        self.direct = direct
        self.var = var
        self.libr = {}
        self.rebin_min=min_
        self.rebin_max=max_
        if self.model=='diskbb+wabs*po':
            self.tk_po = new_win
            self.open_po(self.tk_po)
        else:
            self.tk_comp = new_win
            self.open_comp(self.tk_comp)

    def lab(self , tk_name , lab_name , size_row , size_col):
        lab_n = Label(tk_name,text = lab_name)
        lab_n.grid(row = size_row , column = size_col)
        
    def mainwindow(self,tk_name,value,word,size_row,size_col):
        C = StringVar()
        C.set(value)
        self.libr[ word ] = Entry(tk_name,textvariable = C , width = 10 , bg = "white")
        self.libr[ word ].grid(row = size_row , column = size_col)

    def button(self , tk_name , name , size_row , size_col , name_func):
        but = Button(tk_name,text = name , pady = 10)
        but.grid(row = size_row , column = size_col , rowspan = 1 , columnspan = 1 , sticky = W+N+S+E)
        b=but.bind("<Button-1>",name_func)

    def count_to_flux(self,event):
        gcwd=os.getcwd()
        print gcwd
        name=self.model
        print name
        if name=='diskbb+wabs*po':
            model=[name,self.libr["tin"].get(),self.libr["norm"].get(),self.libr["nh"].get(),self.libr["pho"].get(),self.libr["norm_mo"].get()]
        if name=='diskbb+wabs*compLS':
            model=[name,self.libr["tin"].get(),self.libr["norm"].get(),self.libr["nh"].get(),self.libr["kt"].get(),self.libr["tau"].get(),self.libr["norm_mo"].get()]
        home_dir='/home/'+getpass.getuser()
        names=glob.glob("n_spec_*.pha")
        event_=''
        for file_ in names:
            fits_=fits.open(file_)
            fits_date=fits_["SPECTRUM"].header["TSTOP"]
            xspec_flux.Xspec(self.direct,home_dir,file_,model,self.var-1,self.rebin_min,self.rebin_max)
            dat=gcwd+'/'+file_[0:13]+'.dat'
            print dat
            print glob.glob(dat)[0]
            rd=open(dat,'r').read()
            text=[[col for col in line.split(' ') if col!=''] for line in rd.split('\n')]
            for i in xrange(len(text)):
                for j in xrange(len(text[i])):

                    if text[i][j]=='Flux':
                        event_ += str(fits_date)+' '+text[i][j+3].replace('(','')+' '+text[i][j+1]+'\n'
            os.remove(dat)
            print event_
        wt=open('count_to_flux.dat','w')
        wt.write(event_)
        wt.close()

    def count_to_flux1(self,event):
        name=self.model
        print name
        if name=='diskbb+wabs*po':
            model=[name,self.libr["tin"].get(),self.libr["norm"].get(),self.libr["nh"].get(),self.libr["pho"].get(),self.libr["norm_mo"].get()]
            w=self.tk_po
        if name=='diskbb+wabs*compLS':
            w=self.tk_comp
            model=[name,self.libr["tin"].get(),self.libr["norm"].get(),self.libr["nh"].get(),self.libr["kt"].get(),self.libr["tau"].get(),self.libr["norm_mo"].get()]
        energy=["30 100","100 1000","30 1000"]
        input_energy=energy[self.var-1]
        print model,input_energy,self.rebin_min,self.rebin_max
        return w.destroy()
                    
    def open_po(self,tk_name):
        os.chdir(self.direct)
        print self.model,self.direct,self.var
        self.lab(tk_name,"Tin,keV",15,0)
        self.mainwindow(tk_name,"1.0","tin",16,0)
                
        self.lab(tk_name,"Norm",15,1)
        self.mainwindow(tk_name,"1.0","norm",16,1)
    
        self.lab(tk_name,"nH*10^22",15,2)
        self.mainwindow(tk_name,"1e0","nh",16,2)
            
        self.lab(tk_name,"PhoIndex",17,0)
        self.mainwindow(tk_name,"1.0","pho",18,0)

        self.lab(tk_name,"Norm_second",17,1)
        self.mainwindow(tk_name,"1.0","norm_mo",18,1)

        self.button(tk_name,"OK",17,2,self.count_to_flux)

    def open_comp(self,tk_name):
        os.chdir(self.direct)
        print self.model,self.direct,self.var
        self.lab(tk_name,"Tin,keV",15,0)
        self.mainwindow(tk_name,"1.0","tin",16,0)
                
        self.lab(tk_name,"Norm",15,1)
        self.mainwindow(tk_name,"1.0","norm",16,1)
    
        self.lab(tk_name,"nH*10^22",15,2)
        self.mainwindow(tk_name,"1e0","nh",16,2)
        
        self.lab(tk_name,"kT,keV",17,0)
        self.mainwindow(tk_name,"1.0","kt",18,0)
            
        self.lab(tk_name,"Tau",17,1)
        self.mainwindow(tk_name,"1.0","tau",18,1)

        self.lab(tk_name,"Norm_second",17,2)
        self.mainwindow(tk_name,"1.0","norm_mo",18,2)

        self.button(tk_name,"OK",17,3,self.count_to_flux)

def run_window(new_win,model,direct,var,min_,max_):
    win1=New_window(new_win,model,direct,var,min_,max_)
    if model == 'diskbb+wabs*po':
        win1.tk_po.title(model)
        win1.tk_po.mainloop()
    else:
        win1.tk_comp.title(model)
        win1.tk_comp.mainloop()

if __name__=='__main__':
    model=['diskbb+wabs*po','diskbb+wabs*compLS']
    m=input('Choose your destiny[1/2]:')
    direct=os.getcwd()
    min_="20"
    max_="15"
    var=3
    new_win=Tk()
    run_window(new_win,model[m-1],direct,var,min_,max_)
