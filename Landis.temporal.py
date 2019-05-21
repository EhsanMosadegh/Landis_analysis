# -*- coding: utf-8 -*-
############################################################
# author: Ehsan Mosadegh
# usage: to analyze LANDIS data, temporal analysis
# date: May 10, 2019
# email: ehsan.mosadegh@gmail.com, ehsanm@dri.edu
# notes:
############################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#==========
# controlling options:

# select scenario number
scenario_no = '5'
fsize=9  # font-size

# select type of fire
fire_type_index = 1 # 0-1
fire_type = ['Flaming' ,  'Smoldering']
fire = fire_type[fire_type_index]

# select pollutant and units
pollutant_index = 0 # 0-n
pollutant_name_list = ['PM2.5' , 'PM10' , 'NOX' , 'NH3' , 'CO' , 'CO2']
pollutant_unit_list = ['kg/day' , 'kg/day' , 'kg/day' , 'kg/day' , 'kg/day' , 'kg/day']
pollutant = pollutant_name_list[pollutant_index] # index should be integer
pollutant_unit = pollutant_unit_list[pollutant_index]


# other settinggs
scenario_year = 30
time_scale = 'FireDay-30'
var_1 = pollutant+'-'+fire+'-'+str(scenario_year) # all string

print('-> variable 1 = %s'  %(time_scale) )
print('-> variable 2 = %s'  %(var_1) )

#==========
# define the input file

input_file_name = '/Scenario_'+scenario_no+'_year_30_latlon.csv' # \ at the bigining

input_file_path = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs'

input_file_full_path = input_file_path + input_file_name

#==========
# read-in data

input_df = pd.read_csv( input_file_full_path , sep=',' , header=0 )#, names= ColumnList)# ,  index_listcol=0 ) why index_listcol does not work?

#==========
# group the dataset

grouped_data_by_julian_day = input_df.groupby(time_scale) # group the dataset by jday

# group_keys = grouped_data_by_julian_day.groups.keys # does not get the keys!

group_keys = list(grouped_data_by_julian_day.groups)  # use list() function to geth the keys of each group

total_no_of_fires_list = []

total_emission_annual_list = []

key_list = []

# for each group we extract no. of fires per each day, keys are days with fires
for keys in group_keys:

    single_group = grouped_data_by_julian_day.get_group(keys)  # get any group by its 'key'

    no_of_fire = single_group['pointid'].count() # count the number fo fires per each group/day. 'pointid' no. is unique for each fire.

    total_emission_per_day = single_group[var_1].sum() # sum total emission of a pollutant per day

    total_no_of_fires_list.append(no_of_fire)

    total_emission_annual_list.append(total_emission_per_day)

    key_list.append(keys)

#==========
# prepare lists for plotting

# annual list of values
# note: skipped the first index: jday=0
#x_list = key_list #[1:]
#y_list = total_no_of_fires_list #[1:]
y_list_emission = total_emission_annual_list #[1:]

# create a Df for 366 days with zero values, then fill each day/cell with appropriate value
# first create zero lists for each plot axis
jday_list = [jdays for jdays in range(0,367,1)]             # list of jdays from: 0-366

no_of_fire_list = [fires_no*0 for fires_no in range(367)]   # list of zeros for all year

emission_list = [emis*0 for emis in range(367)]

# create a dict from the zero lists
yr_dict = { 'jday': jday_list,
           'no_of_fires': no_of_fire_list,
           'daily_emission': emission_list}

# create a DF from dict
yr_df = pd.DataFrame(yr_dict)

#yr_df = pd.DataFrame( { 'jday':np.zeros(367),
#                     'no_of_fires':np.zeros(367)} )  # example to create DF from np.zero method

# fill / update zero cells in DF with daily values that are available
for key_list_index in range(0,len(key_list),1): # keys = jdays with fire

    #print('-> list"s cell index= %s' %(key_list_index) )
    #print('-> list"s cell value= %s' %(key_list[key_list_index]) )

    key_list_value = key_list[key_list_index]

    jday_ = key_list_value
    # extract each day value from list
    daily_total_fires = total_no_of_fires_list[key_list_index]      # keys = jdays with fire

    daily_total_emit = total_emission_annual_list[key_list_index]
    # update DF
    yr_df['no_of_fires'][jday_] = daily_total_fires  # update each DF"s column cell at each jday_ with available data, before it was zero

    yr_df['daily_emission'][jday_] = daily_total_emit



# skip the first day with 0-index in the lists
xx_ = list(yr_df['jday'])            #[1:]

yy_ = list(yr_df['no_of_fires'])     #[1:]

yy2_ = list(yr_df['daily_emission'])

x_ = xx_[1:]

y_ = yy_[1:]

y2_ = yy2_[1:]

#---
# with plt method

#plt.xticks(range(0,367,10) , rotation=90)
#plt.margins(0.2)
#
#plt.xlabel('julian days')
#
#plt.ylabel('number of fires')
#
##plt.legend('ehsan')
#plt.title('frequency of fires in LANDIS scenario %s, 2016' %scenario_no)
#width = 0.5
#plt.bar( x_list , y_list , width , color = 'r' , align='center')
#
#plt.show()

#==========
# plotting

#--- first plot= no. of fires

# 1st x-axis
ax1 = plt.subplot(211) # define ax1
#ax1.grid(True)
ax1.bar(x_ , y_ , width = 1 , color='r' , align='center')

ax1.set_xlim(xmin=0, xmax=366)  # to start the plot from zero-zero
ax1.set_ylim(ymin=0, ymax=500)
ax1.set_xlabel('julian days' , fontsize=fsize)
ax1.set_ylabel('number of fires' , fontsize=fsize)
# rotate numnbers???

# 2nd x-axis
ax11 = ax1.twiny()
ax11_xtick_labels = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
ax11_xtick_position_list = [0,31,60,91,121,152,182,213,244,274,305,335,366]
ax11.set_xticks(ax11_xtick_position_list)      # position of x-ticks
ax11.set_xticklabels(ax11_xtick_labels , fontsize=fsize)   # lable of x-ticks ; rotation='vertical'
ax11.xaxis.set_ticks_position('bottom') # set the position of x-ticks of second x-axis to bottom
ax11.xaxis.set_label_position('bottom') # set the position of label of second x-axis to bottom
ax11.set_xlabel('month' , fontsize=fsize)
ax11.spines['bottom'].set_position(('outward', 40))  # plot 2nd x-axis below the 1st axis
#ax2.set_xlim(right=0.5)
plt.title('frequency of fires in LANDIS scenario %s, 2016' %scenario_no , fontsize=fsize)

#--- second plot= emission totals

# 1st x-axis
ax2 = plt.subplot(212) # define ax1 in .subplot() class
#ax1.grid(True)
ax2.bar(x_ , y2_ , width = 1 , color='r' , align='center')

ax2.set_xlim(xmin=0, xmax=366)  # to start the plot from zero-zero
ax2.set_ylim(ymin=0, ymax=500)
ax2.set_xlabel('julian days' , fontsize=fsize)
ax2.set_ylabel('total emissions (%s)' %pollutant_unit, fontsize=fsize)
# rotate numnbers???

# 2nd x-axis
ax22 = ax2.twiny()
ax22_xtick_labels = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
ax22_xtick_position_list = [0,31,60,91,121,152,182,213,244,274,305,335,366]
ax22.set_xticks(ax22_xtick_position_list)      # position of x-ticks
ax22.set_xticklabels(ax22_xtick_labels , fontsize=fsize)   # lable of x-ticks ; rotation='vertical'
ax22.xaxis.set_ticks_position('bottom') # set the position of x-ticks of second x-axis to bottom
ax22.xaxis.set_label_position('bottom') # set the position of label of second x-axis to bottom
ax22.set_xlabel('month' , fontsize=fsize)
ax22.spines['bottom'].set_position(('outward', 40))  # plot 2nd x-axis below the 1st axis
#ax2.set_xlim(right=0.5)
plt.title('total daily emissions of %s from fires in LANDIS scenario %s, 2016' %(var_1,scenario_no) , fontsize=fsize)
#plt.subplots_adjust(hspace=.2)
plt.tight_layout()
plt.show()

#---
# some other method

#x_listloc = lambda month_count: 15+(30*month_count)  # define formula for x_listloc
#def x_listloc(month_count):
#    center_ = 15+30*month_count
#    return center_;

#ax2_xtick_position_list = []
#for month_count in range(len(ax2_xtick_labels)):
#    ax2_xtick_position_list.append(x_listloc(month_count))


#ax2_xtick_position_list = [ x_listloc(month_count) for month_count in range(len(ax2_xtick_labels)) ] # another way to write for loop+function==3 lines to 1 line
#---

#==========
# save the plot

plot_name = 'no_of_fires_scen'+scenario_no+'.png'

plot_dir = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/plots/'

saved_plot = plot_dir+plot_name
#extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
plt.savefig(saved_plot, bbox_inches='tight')





