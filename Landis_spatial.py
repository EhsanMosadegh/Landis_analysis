# -*- coding: utf-8 -*-
############################################################
# author: Ehsan Mosadegh
# usage: to analyze LANDIS data, spatial analysis
# date: June 07, 2019
# email: ehsan.mosadegh@gmail.com, ehsanm@dri.edu
# notes:
############################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import time

#===========================================================
# get the starting time

start = time.time()

#===========================================================
# controlling options:

# select the domain
my_domain= 'cmaq_domain' # 'zoomed_domain' or 'cmaq_domain' 
# save the plot or not?
save_plot= 'no'  # 'yes' or 'no'
# select scenario number
scenario_no = '5'
# fsize=9  # font-size
month_list = [ 'jul' , 'aug' , 'sep' , 'oct' , 'nov']
# set the resolution of spatial plot
spatial_res= 'l' # 'l' , 'i' , 'f'
plot_format='pdf'  # 'png' 'svg'
# other settinggs
scenario_year = 30

print(f'-> save plot is= {save_plot} ')
print(f'-> plot domain is set to= {my_domain}')
#===========================================================
# define the input file

input_file_name = 'Scenario_'+scenario_no+'_year_30_latlon.csv' 

input_file_path = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/landis_input_files_latlon_converted/' # '/' at the end of the path

input_file_full_path = input_file_path + input_file_name

#===========================================================
# read-in data

print(f'-> reading input file for scenario= {scenario_no}')

input_df = pd.read_csv( input_file_full_path , sep=',' , header=0 )#, names= ColumnList)# ,  index_listcol=0 ) why index_listcol does not work?

#===========================================================
# filter zero jdays

filter_nonZero_days = ( input_df['FireDay-30'] != 0 )

input_df_nonZero_days = input_df[ filter_nonZero_days ]

#===========================================================
# Basemap plot setting to zoom

### center of CMAQ domain
xcent_cmaq =-120.806 # degrees
ycent_cmaq =40.0 # degrees

# center of my desired map== I like to set Lake Tahoe at the center
lon_desired_cent =-120.0323507 # center of the map; degrees
lat_desired_cent =39.02 # center of the map; degrees

# # lower-left corner of desired map, which I set it based on CMAQ LATD, LOND 
# lower_left_lon_list_of_fires=-122.0 # lower-left corner of the map; degrees, -120.1407
# lower_left_lon_list_of_fires=20.0# lower-left corner of the map; degrees, 37.60086 

### domain size  for zoomed map
NROWS = 500*1000 # height of the map; meters
NCOLS = 500*1000 #

### domain size  for zoomed map
NROWS_zoom = 70000 # height of the map; meters
NCOLS_zoom = 65000 # width of the map; meters

# # upper-right corner
# upper_right_lon_list_of_fires=-118.0 # meters
# upper_right_lon_list_of_fires=40 # meters
print(" ")
print('-> making the map now ...')

# draw the map background --> map of whole domain
# my_desired_base_map= Basemap(projection='lcc' ,\
# 	llcrnrx=lower_left_lon_list_of_fires , llcrnry=lower_left_lon_list_of_fires ,\
# 	lon_list_of_fires_0=lon_list_of_fires_desired_cent , lon_list_of_fires_0=lon_list_of_fires_desired_cent ,\
# 	height=NROWS_zoom , width=NCOLS_zoom ,\
# 	 resolution='l' , area_thresh=0.5) # urcrnrx=upper_right_lon_list_of_fires , urcrnry=upper_right_lon_list_of_fires


# first, we plot a desired base-map, and then we plot our data on this map
if (my_domain=='cmaq_domain'):
	print(f'-> domain is= {my_domain}')

	my_desired_base_map= Basemap(projection='lcc' ,\
		lat_0=ycent_cmaq , lon_0=xcent_cmaq ,\
		height=NROWS , width=NCOLS ,\
		resolution=spatial_res , area_thresh=0.5)

# new version of my map --> zoomed map
if(my_domain=='zoomed_domain'):
	print(f'-> domain is= {my_domain}')

	my_desired_base_map= Basemap(projection='lcc' ,\
		lat_0=lat_desired_cent , lon_0=lon_desired_cent ,\
		height=NROWS_zoom , width=NCOLS_zoom ,\
		resolution=spatial_res , area_thresh=0.5) # 	urcrnrlon_list_of_fires=upper_right_lon_list_of_fires , urcrnrlon_list_of_fires=upper_right_lon_list_of_fires,\ , llcrnrlon_list_of_fires=lower_left_lon_list_of_fires , llcrnrlon_list_of_fires=lower_left_lon_list_of_fires ,\

my_desired_base_map.fillcontinents( color='#CCCCCC' , lake_color='lightblue' , zorder=1 ) # , 
my_desired_base_map.bluemarble( zorder=1 )
#my_desired_base_map.etopo( zorder=1 )
#my_desired_base_map.shadedrelief( zorder=1 )

my_desired_base_map.drawmapboundary(color='k' )#, fill_color='#46bcec' ) #, fill_color='aqua')
my_desired_base_map.drawcoastlines(color = '0.15' , zorder=2 )
my_desired_base_map.drawcounties(linewidth=0.5 , color='k' , zorder=3 )
my_desired_base_map.drawstates(zorder=4)


print(" ")
#===========================================================
# define a dictionary for 
month_dict = {

	'jul' : [ 183 , 213 , 'v'] ,
	'aug' : [ 214 , 244 , 'p'] ,
	'sep' : [ 245 , 274 , '^'] ,
	'oct' : [ 275 , 305 , '.'] ,
	'nov' : [ 306 , 335 , 'd'] 

	}

#===========================================================
# loop through months and and filter chunks

for month in month_list :

	print( f'-> processing month= {month}' )

	filter_month = ( input_df_nonZero_days[ 'FireDay-30' ] >= month_dict[month][0] ) & ( input_df_nonZero_days[ 'FireDay-30' ] <= month_dict[month][1] )

	chunck_of_df = input_df_nonZero_days [ filter_month ]  

	lat_list_of_fires = chunck_of_df ['Lat'].values
	print(f'-> no. of burned pixels in {month} in scen ({scenario_no})= {len(lat_list_of_fires)}')
	#print(lon_list_of_fires)

	lon_list_of_fires = chunck_of_df ['Long'].values
	#print(f'-> no. of fires in {month} = {len(lon_list_of_fires)}')

	#x_coord , y_coord = my_desired_base_map( lon_list_of_fires , lon_list_of_fires ) # order: x ,y; degrees to meters

	#my_desired_base_map.scatter( x_coord , y_coord , latlon=True , marker= month_dict[month][2] , s=10 , label=month) # If lon_list_of_fireslon_list_of_fires is False (default), x and y are assumed to be in map projection coordinates. 
#source: https://matplotlib.org/basemap/api/basemap_api.html

	my_desired_base_map.scatter( lon_list_of_fires , lat_list_of_fires , latlon=True , marker= month_dict[month][2] , s=12 , label=month ,  zorder=5 ) # If lon_list_of_fireslon_list_of_fires is False (default), x and y are assumed to be in map projection coordinates. 

#my_desired_base_map.etopo(scale=0.5, alpha=0.5)  # the map backgroud 
#my_desired_base_map.shadedrelief(scale=0.5)
plt.legend( scatterpoints=1 , frameon=True , title= 'number of fires' , loc='center left', bbox_to_anchor=(1, 0.5) ,
          fancybox=True )

plt.title(f'Spatial distribution of fires in LANDIS scenario {scenario_no}' , fontsize=10 )

#===========================================================
# save the plot
if (save_plot=='yes'):

	plot_name = 'spatial_distribution_of_fires_scen'+scenario_no+'.'+plot_format

	plot_dir = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/plots/'

	saved_plot = plot_dir+plot_name
	#extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
	plt.savefig(saved_plot , dpi=1200 , format=plot_format ) #, bbox_inches='tight')

	print(" ")
	print(f'-> plot saved at=')
	print(saved_plot)
	#plt.show()
	#===========================================================
	# calculon_list_of_firese run time

	end = time.time()

	print( f'-> run time= { (( end - start ) / 60 ) :.2f} min' )  # f-string

	#===========================================================
# show the plot
else:
	print(" ")
	print(f'-> save plot is NO! so we only show it here.')
	plt.show() # save the plot and then show it.



