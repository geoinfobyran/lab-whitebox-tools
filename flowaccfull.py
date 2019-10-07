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
    subprocess.run(['ogr2ogr', '-s', f'EPSG:{epsg}', newfile, file])

wbt = WhiteboxTools()

work_dir = os.path.dirname(os.path.abspath(__file__))
wb_dir = work_dir + "/WBT"
data_dir = "/home/johnnie/kod/flodesapp/localdata/geodata"
out_dir = data_dir + "/out"

wbt.set_whitebox_dir(wb_dir)

def addSrs(file):
    add_srs=f'gdal_edit.py -a_srs EPSG:3006 {file}'
    print(add_srs)  
    os.system(add_srs)

def run():
    out_dem = f'{out_dir}/flowacc_ab/dem.tif'
    out_pntr = f'{out_dir}/flowacc_ab/pntr.tif'
    out_accum = f'{out_dir}/flowacc_ab/accum.tif'

    # wbt.breach_depressions(
    #     f'{data_dir}/DEM_LM/ab_10m_nowater.tif', 
    #     out_dem,
    #     fill_pits=True
    # )

    # wbt.d8_pointer(
    #     out_dem, 
    #     out_pntr
    # )

    # wbt.d8_flow_accumulation(
    #     out_dem, 
    #     out_accum, 
    #     out_type="cells"
    # )


    wbt.flow_accumulation_full_workflow(
        f'{data_dir}/DEM_LM/ab_10m_nowater.tif',
        out_dem,
        out_pntr,
        out_accum,
       out_type="cells"
    )



    add_srs_raster(out_dem)
    add_srs_raster(out_pntr)
    add_srs_raster(out_accum)


start = time.time()
run()
end = time.time()
print(end - start)
