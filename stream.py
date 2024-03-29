import os
import sys
import time
from WBT.whitebox_tools import WhiteboxTools

wbt = WhiteboxTools()

work_dir = os.path.dirname(os.path.abspath(__file__))
wb_dir = work_dir + "/WBT/"
data_dir = work_dir + "/data/"
out_dir = work_dir + "/out/"

wbt.set_whitebox_dir(wb_dir)

omr = '925'

def run():
    outfile = f'{out_dir}/streams/{omr}.tif'
    wbt.greater_than(
        f'{data_dir}/D8_Flowacc/{omr}.dep',
        '10000',
        outfile
    )
    add_srs=f'gdal_edit.py -a_srs EPSG:3006 {outfile}'
    print(add_srs)  
    os.system(add_srs)

start = time.time()
run()
end = time.time()
print(end - start)

