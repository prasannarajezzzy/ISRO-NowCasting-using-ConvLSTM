
import numpy as np 
import matplotlib.pyplot as plt 
import h5py as h5 
import os
import xarray as xr 
import glob
from scipy import interpolate
mypath="./"
chnl=['IMG_TIR1','IMG_TIR2','IMG_VIS','IMG_WV','IMG_SWIR','IMG_MIR']
cnl_0,cnl_1,cnl_2,cnl_3,cnl_4,cnl_5=[],[],[],[],[],[]
l=['Jul20_061738']
cnl0,cnl1,cnl2,cnl3,cnl4,cnl5=np.zeros((150,404,404)),np.zeros((150,404,404)),np.zeros((150,404,404)),np.zeros((150,404,404)),np.zeros((150,404,404)),np.zeros((150,404,404))


x= np.linspace(0,1618,404)
y= np.linspace(0,1616,404)

files= glob.glob(l[0]+"./*h5")

for i,_ in enumerate(files[:150]):
    h5f=h5.File(_,"r") 
    dummy=[]
    for k in chnl:
            #get channels
            value=h5f[k][0]
            xx=np.arange(0,value.shape[1])
            yy=np.arange(0,value.shape[0])
            f = interpolate.interp2d(xx, yy, value, kind='linear')
            value = f(x, y)
            
            print("-")
            
            dummy.append(value)
    cnl0[i,:,:]=dummy[0]
    cnl1[i,:,:]=dummy[1]
    cnl2[i,:,:]=dummy[2]
    cnl3[i,:,:]=dummy[3]
    cnl4[i,:,:]=dummy[4]
    cnl5[i,:,:]=dummy[5]

print("saving files")



# print(cnl0.shape)
# exit()

d={}
d["time"]=('time',np.arange(0,150))
d["lat"]=('lat',np.arange(404))
d["lon"]=("lon",np.arange(404))

d['IMG_TIR1'] = (['time','lat','lon'],cnl0)
d['IMG_TIR2'] = (['time','lat','lon'],cnl1)
d['IMG_VIS'] = (['time','lat','lon'],cnl2)
d['IMG_WV'] = (['time','lat','lon'],cnl3)
d['IMG_SWIR'] = (['time','lat','lon'],cnl4)
d['IMG_MIR'] = (['time','lat','lon'],cnl5)

print("dataset")
dset = xr.Dataset(d)
print("to netcdf")

dset.to_netcdf("./files_3dr.nc")

