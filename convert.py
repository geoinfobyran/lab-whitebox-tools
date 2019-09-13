import os
import sys
from WBT.whitebox_tools import WhiteboxTools

wbt = WhiteboxTools()

work_dir = os.path.dirname(os.path.abspath(__file__))

wbt.set_whitebox_dir(os.path.dirname(
    os.path.abspath(__file__)) + "/WBT/")

def convert(wbt_work_dir):
    wbt.work_dir = wbt_work_dir

    wbt.convert_raster_format(
        '824.dep',
        '824.tif'
    )

convert(os.path.join(work_dir, 'data', 'Breached_DEMs'))
convert(os.path.join(work_dir, 'data', 'D8_Flowacc'))
convert(os.path.join(work_dir, 'data', 'D8_Pointer'))
