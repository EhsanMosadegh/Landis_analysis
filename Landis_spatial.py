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

# select scenario number
scenario_no = '5'
# fsize=9  # font-size
month_list = [ 'jul' , 'aug' , 'sep' , 'oct' , 'nov']

# other settinggs
scenario_year = 30

#===========================================================
# define the input file

input_file_name = 'Scenario_'+scenario_no+'_year_30_latlon.csv' 

input_file_path = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/' # '/' at the end of the path

input_file_full_path = input_file_path + input_file_name

#===========================================================
# read-in data

print('-> reading input file ...')

input_df = pd.read_csv( input_file_full_path , sep=',' , header=0 )#, names= ColumnList)# ,  index_listcol=0 ) why index_listcol does not work?

#===========================================================
# filter zero jdays

filter_nonZero_days = ( input_df['FireDay-30'] != 0 )

input_df_nonZero_days = input_df[ filter_nonZero_days ]

#===========================================================
# Basemap plot setting to zoom

### center of domain
# xcent =-120.806 # degrees
# ycent =40.0 # degrees

xcent_zoom =-120.02 # degrees
ycent_zoom =39.05 # degrees

### domain size
NROWS_zoom = 100000 # meters
NCOLS_zoom = 100000 # meters
# lower-left corner
llcornerx=-117500 # meters
llcornery=-265500 # meters
# upper-right corner
# urcornerx=132500 # meters
# urcornery=-500 # meters

print('-> making the map ...')
# draw the map background
theMap= Basemap(projection='lcc' , \
	llcrnrx=llcornerx , llcrnry=llcornery ,\
	lat_0=ycent_zoom , lon_0=xcent_zoom , height=NROWS_zoom , width=NCOLS_zoom , resolution='f' , area_thresh=0.5) # urcrnrx=urcornerx , urcrnry=urcornery

theMap.drawmapboundary(color='k' )#, fill_color='#46bcec' ) #, fill_color='aqua')
theMap.drawcoastlines(color = '0.15')
theMap.drawcounties(linewidth=0.5 , color='k')
theMap.drawstates()

#theMap.fillcontinents(color = 'white') #,lake_color='#46bcec')

#theMap.fillcontinents(color='#CCCCCC',lake_color='lightblue')
#theMap.bluemarble()

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

	print( f'-> doing for month= {month}' )

	filter_month = ( input_df_nonZero_days[ 'FireDay-30' ] >= month_dict[month][0] ) & ( input_df_nonZero_days[ 'FireDay-30' ] <= month_dict[month][1] )

	chunck_of_df = input_df_nonZero_days [ filter_month ]  

	lat = chunck_of_df ['Lat'].values

	lon = chunck_of_df ['Long'].values

	x_coord , y_coord = theMap( lon , lat ) # order: x ,y; degrees to meters

	theMap.scatter( x_coord , y_coord , latlon=False , marker= month_dict[month][2] , s=10 , label=month) # If latlon is False (default), x and y are assumed to be map projection coordinates. 
#source: https://matplotlib.org/basemap/api/basemap_api.html

#theMap.etopo(scale=0.5, alpha=0.5)  # the map backgroud 
#theMap.shadedrelief(scale=0.5)
plt.legend( scatterpoints=1 , frameon=True , title= 'number of fires' )

plt.title(f'Spatial distribution of fires - LANDIS scen {scenario_no}')

#===========================================================
# save the plot

plot_name = 'spatial_distribution_of_fires_scen'+scenario_no+'.png'

plot_dir = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/plots/'

saved_plot = plot_dir+plot_name
#extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
plt.savefig(saved_plot , dpi=1200 , format='png' ) #, bbox_inches='tight')

#===========================================================
# calculate run time

end = time.time()

print( f'-> run time= { (( end - start ) / 60 ) :.2f} min' )  # f-string

#===========================================================
# show the plot

plt.show() # save the plot and then show it.



