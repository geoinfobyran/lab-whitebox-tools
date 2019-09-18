import os
import sys
import time
from WBT.whitebox_tools import WhiteboxTools

wbt = WhiteboxTools()

work_dir = os.path.dirname(os.path.abspath(__file__))
wb_dir = work_dir + "/WBT"
data_dir = work_dir + "/data"
out_dir = work_dir + "/out"

wbt.set_whitebox_dir(wb_dir)

omr = '925'

def addSrs(file):
    add_srs=f'gdal_edit.py -a_srs EPSG:3006 {file}'
    print(add_srs)  
    os.system(add_srs)

def run():
    out_dem = f'{out_dir}/flowacc/dem.tif'
    out_pntr = f'{out_dir}/flowacc/pntr.tif'
    out_accum = f'{out_dir}/flowacc/accum.tif'

    wbt.flow_accumulation_full_workflow(
        f'{data_dir}/DEM_LM/mosaik_grid2+_ab_lan_5m_float.tif',
        out_dem,
        out_pntr,
        out_accum
    )

    addSrs(out_dem)
    addSrs(out_pntr)
    addSrs(out_accum)


start = time.time()
run()
end = time.time()
print(end - start)
