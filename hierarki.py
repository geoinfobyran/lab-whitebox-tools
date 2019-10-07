import os
import sys
import time
from WBT.whitebox_tools import WhiteboxTools
import subprocess

def add_srs_raster(file, epsg=3006):
    subprocess.run(['gdal_edit.py', '-a_srs', f'EPSG:{epsg}', file])

def add_srs_vector(file, epsg=3006):
    split = file.split('.')
    split[0] += f'_{epsg}'
    newfile = '.'.join(split)
    subprocess.run(['ogr2ogr', '-a_srs', f'EPSG:{epsg}', newfile, file])

wbt = WhiteboxTools()

work_dir = os.path.dirname(os.path.abspath(__file__))
wb_dir = work_dir + "/WBT"
data_dir = "/home/johnnie/kod/flodesapp/localdata/geodata"
out_dir = work_dir + "/out/hierarki"

wbt.set_whitebox_dir(wb_dir)

omr = '925'

d8_pntr = f'{data_dir}/D8_Pointer/{omr}.dep'
streams = f'{data_dir}/Streams/{omr}.dep'

subbasins = f'{out_dir}/subbasins.tif'
wbt.subbasins(
    d8_pntr,
    streams,
    subbasins
)
add_srs_raster(subbasins)

topostream = f'{out_dir}/topostream.tif'
wbt.topological_stream_order(
    d8_pntr, 
    streams, 
    topostream
)
add_srs_raster(topostream)

streamswithsubbasinid = f'{out_dir}/streamswithsubbasinid.tif'
wbt.multiply(
    streams,
    subbasins,
    streamswithsubbasinid
)
add_srs_raster(topostream)

topostream_vector = f'{out_dir}/topostream.shp'
wbt.raster_streams_to_vector(
    topostream, 
    d8_pntr, 
    topostream_vector
)
add_srs_vector(topostream_vector)

streamswithsubbasinid_vector = f'{out_dir}/streamswithsubbasinid.shp'
wbt.raster_streams_to_vector(
    streamswithsubbasinid, 
    d8_pntr, 
    streamswithsubbasinid_vector
)
add_srs_vector(streamswithsubbasinid_vector)

subbasins_vector = f'{out_dir}/subbasins.shp'
subprocess.run(['gdal_polygonize.py', subbasins, '-f', 'ESRI Shapefile', subbasins_vector])