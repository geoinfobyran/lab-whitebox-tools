import os
import sys
import time
from WBT.whitebox_tools import WhiteboxTools

wbt = WhiteboxTools()

work_dir = os.path.dirname(os.path.abspath(__file__))
wb_dir = work_dir + "/WBT"
# data_dir = work_dir + "/data"
data_dir = "/home/johnnie/kod/flodesapp/localdata/geodata"
out_dir = work_dir + "/out"

wbt.set_whitebox_dir(wb_dir)

omr = '925'

def run():
    outfile = f'{out_dir}/vectorstreams/{omr}.shp'
    # wbt.subbasins(
    #     f'{data_dir}/D8_Pointer/{omr}.dep',
    #     f'{data_dir}/Streams/{omr}.dep',
    #     outfile
    # )
    streams = f'{data_dir}/Streams/{omr}.dep'
    d8_pntr = f'{data_dir}/D8_Pointer/{omr}.dep'
    wbt.raster_streams_to_vector(
        streams, 
        d8_pntr, 
        outfile, 
    )
    # add_srs=f'gdal_edit.py -a_srs EPSG:3006 {outfile}'
    # print(add_srs)  
    # os.system(add_srs)

start = time.time()
run()
end = time.time()
print(end - start)

