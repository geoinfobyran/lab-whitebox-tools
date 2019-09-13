import os
import sys
import time
from WBT.whitebox_tools import WhiteboxTools

wbt = WhiteboxTools()

work_dir = os.path.dirname(os.path.abspath(__file__))

wbt.set_whitebox_dir(os.path.dirname(
    os.path.abspath(__file__)) + "/WBT/")

def run(wbt_work_dir):
    wbt.work_dir = wbt_work_dir

    wbt.watershed(
        '824.dep',
        'pour.shp',
        'watershed.tif'
    )

start = time.time()
run(os.path.join(work_dir, 'data', 'D8_Pointer'))
end = time.time()
print(end - start)

