#!/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl

def plot_gr():
    (r,b)=(0,0)
    data=np.loadtxt('sorted_events.dat')
    data1=sorted(data, key=lambda x:x[4])
    for color in data[:,4]:
        if color==1:
            r += 1
        else:
            b += 1
    xn=[data1[i][0]/86400.0 for i in xrange(r)]
    yn=[data1[i][1] for i in xrange(r)]
    y_ern=[data1[i][2] for i in xrange(r)]
    xp=[data1[r+i][0]/86400.0 for i in xrange(b)]
    yp=[data1[r+i][1] for i in xrange(b)]
    y_erp=[data1[i][2] for i in xrange(b)]

    pointsr=pl.errorbar(xn, yn, label="Obj_name" , yerr=y_ern, fmt='o', color='r')
    pointsb=pl.errorbar(xp, yp, label="Obj_piled_up" , yerr=y_erp, fmt='o', color='b')
    
    pl.title('Light_curve')
    pl.xlabel('T-T0,days')
    pl.ylabel('RATE,counts/sec')
    xmin=(min(data[:,0])-min(data[:,0])/100)/86400
    xmax=(max(data[:,0])+max(data[:,0])/100)/86400
    ymin=min(data[:,1])-min(data[:,1])/100
    ymax=max(data[:,1])+max(data[:,1])/100
    pl.xlim(xmin,xmax)
    pl.ylim(ymin,ymax)
    pl.legend(handles=[pointsr], loc=1, bbox_to_anchor=(1.0, 1.0))
    if b!=0:
        pl.legend(handles=[pointsb], loc=4, bbox_to_anchor=(1.0, 1.0))
    pl.show()

def plot_flux(bin_name):
    (r,b)=(0,0)
    name='fluxed_'+bin_name+'.dat'
    data=np.loadtxt(name)
    data1=sorted(data, key=lambda x:x[3])
    for color in data[:,3]:
        if color==1:
            r += 1
        else:
            b += 1
    xn=[data1[i][0]/86400.0 for i in xrange(r)]
    yn=[data1[i][1] for i in xrange(r)]
    y_ern=[data1[i][2] for i in xrange(r)]
    xp=[data1[r+i][0]/86400.0 for i in xrange(b)]
    yp=[data1[r+i][1] for i in xrange(b)]
    y_erp=[data1[i][2] for i in xrange(b)]

    pointsr=pl.errorbar(xn, yn, label="Obj_name" , yerr=y_ern, fmt='o', color='r')
    pointsb=pl.errorbar(xp, yp, label="Obj_piled_up" , yerr=y_erp, fmt='o', color='b')
    
    pl.title('Light_curve')
    pl.xlabel('T-T0,days')
    pl.ylabel('FLUX,erg/sec/cm^2')
    xmin=(min(data[:,0])-min(data[:,0])/100)/86400
    xmax=(max(data[:,0])+max(data[:,0])/100)/86400
    ymin=min(data[:,1])-min(data[:,1])/100
    ymax=max(data[:,1])+max(data[:,1])/100
    pl.xlim(xmin,xmax)
    pl.ylim(ymin,ymax)
    pl.legend(handles=[pointsr], loc=1, bbox_to_anchor=(1.0, 1.0))
    if b!=0:
        pl.legend(handles=[pointsb], loc=4, bbox_to_anchor=(1.0, 1.0))
    pl.show()

if __name__=='__main__':
    #plot_gr()
    plot_flux('bin')
