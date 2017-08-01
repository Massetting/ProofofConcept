# -*- coding: utf-8 -*-
"""
Created on Mon May 09 14:10:31 2016
@author: andrea.massetti@monash.edu
"""
import gdal,ogr
import numpy as np
band=r"fullpath_of_tif_file\filename.tif"
shp=r'fullpath_of_shp_file\filename.shp'
def array_from_points(shp=shp,band=band,data_type=np.float64):
    """Function that writes the values of the points of a shapefile that overlay a pixel of a tiff raster. 
    Please provide points at the same resolution of the raster, centred on the pixel. 
    array_from_points(shp=shp,band=band,data_type=np.float64)
    INPUT
        shp:fullpath_of_tif_file\filename.tif
        band:fullpath_of_shp_file\filename.shp
        data_type: data type of the numpy array in output.
            Important: change data_type to smallest datatype that contains full range of values. 
            ie for pixel value range 0 to 10000 without decimal , use: type=np.uint16
            in memory 10000000 values
            float64=8Mb
            uint16 or int16=2Mb
            (bit depth matters)
            more numpy data types here: https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html
            

    OUTPUT    
    
        Returns a numpy array. The index corresponds to id of feature in the shapefile
    usage examples:
    a=array_from_points()
    a=array_from_points(shp=r"D:\myvectorcollection\mypoints.shp",band=r"D:\myrastercollection\myraster.tif")
    a=array_from_points(shp=r"D:\myvectorcollection\mypoints.shp",band=r"D:\myrastercollection\myraster.tif",data_type=np.int16)
    
    """
    src_ds=gdal.Open(band) 
    gt=src_ds.GetGeoTransform()
    rb=src_ds.GetRasterBand(1)
    ds=ogr.Open(shp)
    lyr=ds.GetLayer()
    arr=np.empty((0),dtype=data_type)
    for feat in lyr:
        geom = feat.GetGeometryRef()
        mx,my=geom.GetX(), geom.GetY() 
        px = int((mx - gt[0]) / gt[1]) 
        py = int((my - gt[3]) / gt[5]) 
        intval=rb.ReadAsArray(px,py,1,1)
        arr=np.append(arr,intval[0])
    return arr   
a=array_from_points()


        

