## this is the code that assigns the era5 grids to Indian district shape files 
## and then makes the daily temperature data for the Indian districts

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 10:31:14 2024

@author: SME
"""

import numpy as np
import pickle
import xarray as xr
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


path='G://SME/paper_2/IndiaDrought/'
##getting the districts shape file from the spei maps already provided

districts_shp=gpd.read_file(path+"speidata/india_admin_shapes/DISTRICT_BOUNDARY.shp",crs=4326).to_crs(epsg=4326)
districts_shp=districts_shp[['ID','geometry']]
districts=list(districts_shp['ID'])
districts_shp=districts_shp.set_index('ID')

districts_shp['area']=districts_shp['geometry'].apply(lambda x: x.area)
districts_df=pd.read_csv(path+"speidata/id_India_Districts_SPEI.csv")
era5_ncdf=xr.open_dataset(path+"era5temp/year_2019.nc")
lat_list,long_list=np.arange(0,era5_ncdf.latitude.shape[0],1),np.arange(0,era5_ncdf.longitude.shape[0],1) ##latitudes are the y-coordinates and longitudes are the x-coordinates
coords_list=[[long,lat] for long in long_list for lat in lat_list]
#north south are latitudes so y-axis, and east-west are longitudes so x-axis
'''
Access the yearly ncdf for each district and then get the daily min, max, median and mean temperatures
at the different time stamps. Then convert it to the daily corresponding measures and then save the 
district file with daily temperatures for each year from 2010 to 2020.
So we take the geometry of each district, and then select the ERA5 sub-grids belonging to
that district and then do the aggregation.
'''
ncdf_coords=[]
for coords in coords_list:
    long,lat=coords[0],coords[1]
    #make_point=(era5_ncdf.longitude.values[long],era5_ncdf.latitude.values[lat])
    ncdf_coords.append([era5_ncdf.longitude.values[long],era5_ncdf.latitude.values[lat],long,lat])
    
district_coords={}
no_coords={}
for district in districts:
    geometry=districts_shp.loc[district,'geometry']
    found={'coords':[],'xy-axis':[]}
    for coords in coords_list:
        long,lat=coords[0],coords[1]
        make_point=(era5_ncdf.longitude.values[long],era5_ncdf.latitude.values[lat])
        if geometry.contains(Point(make_point)) or geometry.touches(Point(make_point)):
            found['coords']=found['coords']+[make_point]
            found['xy-axis']=found['xy-axis']+[[long,lat]]
    if len(found['coords'])>0:
        district_coords[district]=found
    else:
        no_coords[district]=found
    print(district)
with open(path+"era5temp/mapped_districts.pickle", 'wb') as f:
    pickle.dump(district_coords, f) 

with open(path+"era5temp/not_mapped_districts.pickle",'rb') as f:
    not_coords = pickle.load(f)
with open(path+"era5temp/mapped_districts.pickle",'rb') as f:
    district_coords = pickle.load(f)


missed_districts=districts_df[districts_df['ID'].isin(list(district_coords.keys()))]            
missed_districts = missed_districts[~missed_districts['District'].str.contains('DISPUTED')]
ncdf_coordsdf = pd.DataFrame(ncdf_coords, columns=['longitude', 'latitude','x-axis','y-axis'])
ncdf_coordsdf['longitude']=ncdf_coordsdf['longitude'].astype(float)
ncdf_coordsdf['latitude']=ncdf_coordsdf['latitude'].astype(float)
no_coords=districts_shp[districts_shp['ID'].isin(list(missed_districts['ID']))]
no_coords_list=list(no_coords['ID'])
no_coords=no_coords.set_index('ID')
district_coords1={}
check=pd.DataFrame()
no_coords_list=[104, 128, 171, 238, 325, 351, 383, 422, 429, 496, 539, 595, 601]
for ix in no_coords_list:
    district=no_coords.loc[ix,'geometry']
    print(ix,': ',district.bounds)
    long_min,long_max=min(district[0],district[2]),max(district[0],district[2])
    lat_min,lat_max=min(district[1],district[3]),max(district[1],district[3])
    select=ncdf_coordsdf[(ncdf_coordsdf['longitude']>=long_min) & (ncdf_coordsdf['longitude']<=long_max)]
    select=select[(select['latitude']>=lat_min) & (select['latitude']<=lat_max)]
    select['id']=ix
    select['district_long_min']=long_min
    select['district_long_max']=long_max
    select['district_lat_min']=lat_min
    select['district_lat_max']=lat_max
    try:
        select['point']= select.apply(lambda row: (row['longitude'], row['latitude']), axis=1)
        select['xy-axis']= select.apply(lambda row: (row['x-axis'], row['x-axis']), axis=1)
    except:
        select['point']='not_found'
        select['xy-axis']='not_found'
    temp={}
    temp['coords'],temp['xy-axis']=list(select['point']),list(select['xy-axis'])
    district_coords1[ix]=temp
    check=pd.concat([check,select],axis=0)

with open(path+"era5temp/mappedv2_districts.pickle", 'wb') as f:
    pickle.dump(district_coords1, f) 
district_coords.update(district_coords1)    
with open(path+"era5temp/mapped_districts.pickle", 'wb') as f:
    pickle.dump(district_coords, f) 
##left=districts_df[districts_df['ID'].isin(list(district_coords.keys()))==False]
##only disputed districts are remaining
with open(path+"era5temp/mapped_districts.pickle", 'rb') as handle:
    district_coords=pickle.load(handle)
district_size={}
for item in district_coords:
    district_size[item]=len(district_coords[item]['xy-axis'])
    
savepath=path+"era5temp/district_era5/"
years=[2010+i for i in range(11)]

def catch_era5(district,ncdf):
        district_ix=district_coords[district]['coords']
        latitude_array = np.array([coord[1] for coord in district_ix])
        longitude_array = np.array([coord[0] for coord in district_ix])
        district_ncdf=ncdf.sel(latitude=latitude_array, longitude=longitude_array, method='nearest')
        district_df=district_ncdf.to_dataframe().reset_index()
        district_df=district_df[['time','t2m']].groupby(by='time').mean().reset_index()
        district_df['date']=district_df['time'].astype(str).apply(lambda x: x.split(' ')[0])
        district_df['date']=district_df['date'].apply(lambda x: int(x.replace('-','')))
        return district_df

for district in district_size:
    if (district_size[district]>0) and (district_size[district]<=5):
        outdf=pd.DataFrame()
        for year in years:
            ncdf=xr.open_dataset(path+'era5temp/year_'+str(year)+'.nc')
            df_part=catch_era5(district,ncdf)
            outdf=pd.concat([outdf,df_part])
        outdf['district']=district
        outdf.to_csv(savepath+str(district)+'_t2m.csv',index=False)
for district in district_size:
    if (district_size[district]>0) and (district_size[district]<=5):
        indf=pd.read_csv(savepath+str(district)+'_t2m.csv')
        indf['district']=district
        indf.to_csv(savepath+str(district)+'_t2m.csv',index=False)
## console 2
for district in district_size:
    if (district_size[district]>5) and (district_size[district]<=15):
        outdf=pd.DataFrame()
        for year in years:
            ncdf=xr.open_dataset(path+'era5temp/year_'+str(year)+'.nc')
            df_part=catch_era5(district,ncdf)
            outdf=pd.concat([outdf,df_part])
        outdf['district']=district
        outdf.to_csv(savepath+str(district)+'_t2m.csv',index=False) 

## console 3
for district in district_size:
    if (district_size[district]>15) and (district_size[district]<=25):
        outdf=pd.DataFrame()
        for year in years:
            ncdf=xr.open_dataset(path+'era5temp/year_'+str(year)+'.nc')
            df_part=catch_era5(district,ncdf)
            outdf=pd.concat([outdf,df_part])
        outdf['district']=district
        outdf.to_csv(savepath+str(district)+'_t2m.csv',index=False) 
 
## console 4
for district in district_size:
    if (district_size[district]>25):
        outdf=pd.DataFrame()
        for year in years:
            ncdf=xr.open_dataset(path+'era5temp/year_'+str(year)+'.nc')
            df_part=catch_era5(district,ncdf)
            outdf=pd.concat([outdf,df_part])
        outdf['district']=district
        outdf.to_csv(savepath+str(district)+'_t2m.csv',index=False)         
'''
  ### NOTE ON THE TEMPERATURE IN THE ERA5 NetCDF ###
  
  This parameter is the temperature of air at 2m above the surface of land, 
  sea or inland waters. 2m temperature is calculated by interpolating between 
  the lowest model level and the Earth's surface, taking account of the 
  atmospheric conditions. This parameter has units of kelvin (K). Temperature 
  measured in kelvin can be converted to degrees Celsius (°C) by subtracting 
  273.15.
  '''          
   
