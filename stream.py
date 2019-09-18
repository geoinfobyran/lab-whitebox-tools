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

def run():
    wbt.greater_than(
        f'{data_dir}/D8_Flowacc/824.dep',
        '10000',
        f'{out_dir}/streams/824.dep'
    )

start = time.time()
run()
end = time.time()
print(end - start)

