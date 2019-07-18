# -*- coding: utf-8 -*-
############################################################
# author: Ehsan Mosadegh
# usage: to analyze LANDIS dataset, temporal analysis
# date: May 10, 2019
# email: ehsan.mosadegh@gmail.com, ehsanm@dri.edu
# notes: to plot temporal profile of Landis species and fires plus pull some stats from dataset
############################################################

import pandas as pd
import matplotlib.pyplot as plt

#===========================================================
# controlling options:

# select scenario number
scenario_no = '5'
plot_format = 'joined'   # 'joined' OR 'seperate'
make_plot = 'no'    # 'yes' or 'no'
stats= 'yes'    # 'yes' or 'no'

### select output plot format
dpi_size= 300
fig_format= '.png'

# select type of fire
fire_type_index = 0 # range= (0,1)
fire_type = ['Flaming' ,  'Smoldering']
fire = fire_type[fire_type_index]

# select pollutant and units
pollutant_index = 0 # range= (0,n)
pollutant_name_list = ['PM2.5' ,    'PM10' ,        'NOX' ,     'NH3' ,     'CO' ,      'CO2']
pollutant_unit_list = ['tons/day' , 'tons/day' , 'tons/day' , 'tons/day' , 'tons/day' , 'tons/day']
pollutant = pollutant_name_list[pollutant_index] # index should be integer
pollutant_unit = pollutant_unit_list[pollutant_index]


# other settinggs
fsize= 7  # font-size
scenario_year = 30
grouping_param = 'FireDay-30'
pol_col = pollutant+'-'+fire+'-'+str(scenario_year) # all string

print(f'-> Landis scenario is= {scenario_no} ')
print(f'-> pollutant= {pollutant}')
print(f'-> grouping parameter is= {grouping_param}')
print(f'-> type of fire is= {fire}')
print(f'-> processing/plotting for pol_col= {pol_col} ')
print(f'-> make plot is= {make_plot}')

#===========================================================
# define the input file

input_file_name = 'Scenario_'+scenario_no+'_year_30_latlon.csv'

input_file_path = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/landis_input_files_latlon_converted/' # '/' at the end of the path

input_file_full_path = input_file_path + input_file_name

#===========================================================
# read-in data

input_df = pd.read_csv( input_file_full_path , sep=',' , header=0 )#, names= ColumnList)# ,  index_listcol=0 ) why index_listcol does not work?

#===========================================================
# group the dataset

#========== method one

list_of_all_jdays = [ *input_df[ grouping_param ] ]
list_of_all_jdays = list(set( list_of_all_jdays ))
list_of_all_jdays = sorted( list_of_all_jdays )
#print( f'-> list of jdays= { list_of_all_jdays } ')

total_no_of_burning_pixels_perDay_list = []
total_pol_emissions_per_day_list = []
list_of_burning_days = []

for jday_iter in list_of_all_jdays :

    #print( f'-> for {jday_iter} ')

    filtered_index_for_jdays = ( input_df[ grouping_param ] == jday_iter )

    filtered_chunk = input_df[ filtered_index_for_jdays ]

    no_of_burning_pixels_perDay = filtered_chunk['pointid'].count()
    total_no_of_burning_pixels_perDay_list.append( no_of_burning_pixels_perDay )

    sum_of_emissions_perDay = filtered_chunk[pol_col].sum()
    total_pol_emissions_per_day_list.append( sum_of_emissions_perDay )

    list_of_burning_days.append( jday_iter)

#print(f'-> list of Julian days with fire --> len= {len(list_of_burning_days)}; and the list= {list_of_burning_days} ')
#print(f'-> list of pol emissions in fire days --> len={len(total_pol_emissions_per_day_list)}; and the list= {total_pol_emissions_per_day_list}')

#========== method two

# grouped_data = input_df.groupby(grouping_param) # group the dataset by jday

# # jdays_with_fires_list = grouped_data.groups.keys # does not get the keys!

# jdays_with_fires_list = list(grouped_data.groups)  # use list() function to geth the keys of each group
# print(f'-> Julian days with fires --> len= {len(jdays_with_fires_list)}; and the list= {jdays_with_fires_list}  ')

# total_no_of_burning_pixels_perDay_list = []

# total_pol_emissions_per_day_list = []

# list_of_burning_days = []

# # for each group we extract no. of fires per each day, keys are days with fires
# for iter_jday_with_fire in jdays_with_fires_list :

#     #print( f'-> loop for jday= {iter_jday_with_fire} ')
#     # if ( iter_jday_with_fire == 0 ) :
#     #     print( '-> we exclude iter_jday_with_fire= ' , iter_jday_with_fire )
#     #     continue

#     #print( f'-> processing jday= {iter_jday_with_fire} ')

#     grouped_chunk_of_data = grouped_data.get_group(iter_jday_with_fire)  # filter dataset for each day with fire, by its key and get a group by its 'key'
#     #print(type(grouped_chunk_of_data))


#     no_of_burning_pixels_perDay = grouped_chunk_of_data['pointid'].count() # count the number of fires per each group/day. 'pointid' no. is unique for each fire.
#     total_no_of_burning_pixels_perDay_list.append(no_of_burning_pixels_perDay)
#     #print(f'-> noumber of burned pixels for jday {iter_jday_with_fire} are= {no_of_burning_pixels_perDay}')


#     sum_of_emissions_perDay = grouped_chunk_of_data[pol_col].sum() # sum total emission of a pollutant per jday of fire for all burning pixels for that day
#     total_pol_emissions_per_day_list.append(sum_of_emissions_perDay)
#     #print(f'-> total emission of {pollutant} per day is= {sum_of_emissions_perDay} tons!')


#     list_of_burning_days.append(iter_jday_with_fire)

# print(f'-> list of Julian days with fire --> len= {len(list_of_burning_days)}; and the list= {list_of_burning_days} ')
# print(f'-> list of pol emissions in fire days is= {total_pol_emissions_per_day_list}')

#===========================================================
# prepare lists for plotting

# annual list of values
# note: skipped the first index: jday=0
#x_list = list_of_burning_days #[1:]
#y_list = total_no_of_burning_pixels_perDay_list #[1:]
#y_list = total_pol_emissions_per_day_list #[1:]

# create a DataFrame for 366 days with zero values, then fill each day/cell with appropriate value
# first create zero lists for each plot axis
jday_list = [jdays for jdays in range(0,367,1)]             # list of jdays from: 0-366

no_of_burning_pixels_perDay_list = [fires_no*0 for fires_no in range(367)]   # list of zeros for all year

emission_list = [emis*0 for emis in range(367)]

# create a dict from the zero lists above
df_col_dict = { 'jday':                     jday_list ,
                'no_of_burning_pixels_perDays':  no_of_burning_pixels_perDay_list ,
                'daily_emission':           emission_list }

# create a DF from dict
year_df = pd.DataFrame(df_col_dict)

#year_df = pd.DataFrame( { 'jday':np.zeros(367),
#                     'no_of_burning_pixels_perDays':np.zeros(367)} )  # example to create DF from np.zero method

# fill / update / set zero cells in DF with daily values that are available
for list_iter in range(0,len(list_of_burning_days),1) : # keys = jdays with fire

    selected_jday_with_fire = list_of_burning_days[ list_iter ]

    #print('-> cell index of the list= %s' %( list_iter ) )
    #print('-> selected jday tat has fire is= %s' %( selected_jday_with_fire ) )

    # select each daily value from list based on its list index
    daily_total_burning_pixels = total_no_of_burning_pixels_perDay_list[ list_iter ]      # iter_jday_with_fire = jdays with fire
    year_df.loc[ selected_jday_with_fire , 'no_of_burning_pixels_perDays' ] = daily_total_burning_pixels  # update each cell in DF for each jday_ with available data; before it was zero

    daily_total_emission = total_pol_emissions_per_day_list[ list_iter ]
    year_df.loc[ selected_jday_with_fire , 'daily_emission' ] = daily_total_emission # set each cell value by .loc method --> df.loc[row# , 'col_label']
    #print(f'-> daily total emission is= {daily_total_emission}')

# skip the first day with 0-index in the lists
xx_ = list(year_df['jday'])            #[1:]

yy_ = list(year_df['no_of_burning_pixels_perDays'])     #[1:]

yy2_ = list(year_df['daily_emission'])

x_ = xx_[1:]

y_ = yy_[1:]

y2_ = yy2_[1:]

# prepare lists for plotting
#===========================================================
# getting stats of Landis scenarios

#print(f'-> dataframe is= {year_df}')

if (stats == 'yes') :

    month_dict = {  'jan': [1,31],
                    'feb': [32,60],
                    'mar': [61,91],
                    'apr': [92,121],
                    'may': [122,152],
                    'jun': [153,182],
                    'jul': [183,213],
                    'aug': [214,244],
                    'sep': [245,274],
                    'oct': [275,305],
                    'nov': [305,335],
                    'dec': [336,366]    }

    month_list = [ *month_dict.keys() ]  # * makes a list of ...; or we can do: list( month_dict.keys() )
    print(" ")
    print(f'-> scenario is= {scenario_no}')
    #print(f'-> month is= {month} ')
    print(" ")

    total_annual_list = []

    for month in month_list :

        lower_band = month_dict[month][0] 
        upper_band = month_dict[month][1]
        
        #print('lower limit and upper limit for the range is= %s --> %s' %(lower_band , upper_band))

        filtered_indexes= ( lower_band <= year_df['jday'] ) &  ( year_df['jday'] <= upper_band )

        #print(f'-> filter is= {filtered_indexes}')

        total_monthly_emnission= year_df['daily_emission'][ filtered_indexes ].sum()

        print(f'-> total monthly emission of "{pollutant}" in "{month}" is= {total_monthly_emnission} tons!')
        total_annual_list.append( total_monthly_emnission )

    print(" ")
    print(f'-> sum of annual emissions for ({pollutant}) from ({fire}) is= {sum(total_annual_list)} tons! ')

# getting stats of Landis scenarios
#===========================================================

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

#===========================================================
# plotting

if ( plot_format == 'seperate' ) :
    #--- first plot= no. of fires

    # 1st x-axis
    ax1 = plt.subplot(211) # define ax1
    #ax1.grid(True)
    ax1.bar(x_ , y_ , width = 1 , color='r' , align='center')

    ax1.set_xlim(xmin=0, xmax=366)  # to start the plot from zero-zero
    ax1.set_ylim(ymin=0, ymax=500)
    ax1.set_xlabel('julian days' , fontsize=fsize)
    ax1.set_ylabel('area (pixel) burned (10^4 m2)' , fontsize=fsize)
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
    plt.title('total daily emissions of %s from fires in LANDIS scenario %s, 2016' %(pol_col,scenario_no) , fontsize=fsize)
    #plt.subplots_adjust(hspace=.2)
    plt.tight_layout()
    #plt.show()

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

if ( plot_format == 'joined') :

    fig = plt.Figure()
    ax1 = plt.subplot(2,1,2) # burning pixels, the bottom plot, (row,col,index) draw 1st axis at bottom
    ax2 = plt.subplot(2,1,1 , sharex=ax1 ) # total daily emissions, the top one, the next axis on top of 1st, share ax1 properties

    #ax1.get_shared_x_axes().join(ax1, ax2) # when each axis is created seperately, and then we want to join them afterwards

    ax1_xtick_labels = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    ax1_xtick_position_list = [0,31,60,91,121,152,182,213,244,274,305,335,366]

    ax1.set_xticks( ax1_xtick_position_list )      # position of x-ticks
    ax1.set_xticklabels( ax1_xtick_labels ) #, fontsize=8 )

    # set limits for both axes
    ax1.set_xlim( xmin=0, xmax=366 )  # to start the plot from zero-zero , bottom plot, pixels
    ax1.set_ylim( ymin=0, ymax=500 )
   # ax2.set_xlim( xmin=0, xmax=366 )
    ax2.set_ylim( ymin=0, ymax=550 )   # top plot, emissions

   # plt.setp( ax2.get_xticklabels(), visible=False) turns off ax2 x-labels

    # make grids for both axes
    ax1.grid( ax1_xtick_position_list )
    ax2.grid(True)

    #ax1.spines['bottom'].set_position(('outward', 40))  # plot 2nd x-axis below the 1st axis

    # plot the values
    ax1.bar( x_, y_ , width = 1 , color='r' , align='center' , label="1 row" )
    ax2.bar( x_ , y2_ , width = 1 , color='r' , align='center' , label="1 row" )

    ax1.set_xlabel('month' , fontsize=fsize)

    plt.title('frequency of fires in LANDIS scenario %s, 2016' %scenario_no , fontsize=fsize)
    ax1.set_ylabel('area (pixel) burned (10^4 m2)' , fontsize=fsize)
    ax2.set_ylabel(f'{pollutant} total emissions ({pollutant_unit})' , fontsize=fsize)



#===========================================================
# save the plot

if (make_plot == 'yes') :

    plot_name = 'Landis_temporal_daily_burnedPixels_and_totalEmissions_'+pollutant+'_scen'+scenario_no+fig_format

    plot_dir = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/plots/'

    saved_plot = plot_dir+plot_name
    #extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(saved_plot, dpi=dpi_size , format=fig_format )#, bbox_inches='tight')

    print( f'-> plot saved at=')
    print(saved_plot)
