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
out_dir = data_dir + "/out/hierarki_riks_50m"

wbt.set_whitebox_dir(wb_dir)

d8_pntr = f'{data_dir}/out/flowacc_riks_50m/pntr.tif'
flowacc = f'{data_dir}/out/flowacc_riks_50m/accum.tif'

streams = f'{out_dir}/streams.tif'
wbt.greater_than(
    flowacc,
    10000,
    streams
)
add_srs_raster(streams)

streams_detailed = f'{out_dir}/streams_detailed.tif'
wbt.greater_than(
    flowacc,
    100,
    streams_detailed
)
add_srs_raster(streams_detailed)

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

strahlerstreams = f'{out_dir}/strahlerstreams.tif'
wbt.strahler_stream_order(
    d8_pntr,
    streams_detailed,
    strahlerstreams
)
add_srs_raster(strahlerstreams)

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

strahlerstreams_vector = f'{out_dir}/strahlerstreams.shp'
wbt.raster_streams_to_vector(
    strahlerstreams, 
    d8_pntr, 
    strahlerstreams_vector
)
add_srs_vector(strahlerstreams_vector)

subbasins_vector = f'{out_dir}/subbasins.shp'
subprocess.run(['gdal_polygonize.py', subbasins, '-f', 'ESRI Shapefile', '-8', subbasins_vector])

"""
SQL:

-- noda upp
select pgr_nodenetwork('riks_50m.streamswithsubbasinid_3006', 1, 'strm_val', 'geom');
select pgr_createtopology( 	'riks_50m.streamswithsubbasinid_3006_noded', 	1, 	'geom', 	'id', 	'source', 	'target' );

-- basins med topo stream order
select
	basins.basin_id,
	streams.topo_val,
		basins.geom
from
	(
		select topo.fid, sub.strm_val as basin_id, topo.strm_val as topo_val from riks_50m.topostream_3006 as topo
		left join riks_50m.streamswithsubbasinid_3006 as sub
		on topo.fid = sub.fid
	) as streams
left join
	(
		select dn as basin_id, geom from riks_50m.subbasins as bas
	) as basins
on basins.basin_id = streams.basin_id;


-- länka segment med drivingdistance
select * from pgr_drivingDistance(
	'select id, source, target, 0 as cost from riks_50m.streamswithsubbasinid_3006_noded',
	4862,
	1
)
left join
riks_50m.streamswithsubbasinid_3006_noded
on edge = id;


-- länka uppströms segment med drivingdistance

select  from
(
	select * from pgr_drivingDistance(
		'select id, target as source, source as target, 0 as cost from riks_50m.streamswithsubbasinid_3006_noded',
		4549,
		1
	)
	left join
	riks_50m.streamswithsubbasinid_3006_noded
	on edge = id
	left join
	(
		select geom as basingeom, dn from
		riks_50m.subbasins
	) as basins
	on old_id = basins.dn
) as t
"""