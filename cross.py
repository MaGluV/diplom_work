from astropy.io import fits
import glob,os

def get_image():    
    names_curve=sorted(glob.glob("*.evt"))
    for name_curve in names_curve:
        fits_source=fits.open(name_curve)
        x_cent=fits_source["EVENTS"].header["TCRPX2"]
        y_cent=fits_source["EVENTS"].header["TCRPX3"]
        x_cent_deg=fits_source["EVENTS"].header["TCRVL2"]
        y_cent_deg=fits_source["EVENTS"].header["TCRVL3"]
        x_sc=fits_source["EVENTS"].header["TCDLT2"]
        y_sc=fits_source["EVENTS"].header["TCDLT3"]
        x=fits_source["EVENTS"].data.field("X")
        y=fits_source["EVENTS"].data.field("Y")
        x_dec=[x_cent_deg+x_sc*(xi-x_cent) for xi in x]
        y_dec=[y_cent_deg+y_sc*(yi-y_cent) for yi in y]
        x_y=[(x_dec[i],y_dec[i]) for i in xrange(len(x_dec))]
        print x_y
        fits_source.close()

if __name__=='__main__':
    get_image()
