# -*- coding: utf-8 -*-
"""
May 2021

@author: coding: Ivan Lokmer, problem: Tom Manzzocchi, Ivan Lokmer

The script finds the optimal location of the 3x3 km copper mine based
on the thickness and concentration data from 598 boreholes
(Copper_mine_exercise.ipynb)

A mining company has drilled 598 boreholes on a regular grid in a 13 km by 46 km
area whilst prospecting for copper. In each borehole, the company have measured:
(i) The thickness of the copper-bearing rock formation (in metres)
(ii) The average copper concentration of this rock formation, 
     in parts per million by volume (ppm).
     
Problem:
1. Calculate the total amount of the copper in the entire area (give your answer
    to the nearest tonne). The density of copper is 8960 kg/m3.
2. The company wants to put a 3 km by 3 km mine in the area. Find the X and Y
   locations of the centre of this mine, for the mine location that will contain
   the most copper. 
3. Plot the distribution of Cu mass in the investigated area to visually inspect 
   your result for the best placement of the mine
   
The data is given in csv file as 'Well X location (km), Well Y location (km),
Thickness (m), Concentration (ppm)'. The file can be found at Gdrive link:
https://drive.google.com/file/d/1SGhQMRjWKc2F57FBeb4rXv16T7xUvMS4/view?usp=sharing

You can download the file and inspect it visually using Notepad, Wordpad or
similar basic text editor.
"""


######### IMPORT ALL THE LIBRARIES USED IN THE SCRIPT #########################
import pandas as pd # import pandas (data analysis and manipulation tool)
import numpy as np  # numerical Python library (required for the work with arrays and matrices)
import matplotlib.pyplot as plt # plotting library




######### READ CSV DATA FILE DIRECTLY FROM GOOGLE DRIVE ######################
# Read the csv file from Google drive share link (variable url) 
# url.split('/')[-2] takes the part of url between the last and second last slash ('/')
# pd.read_csv reads a csv file
# Check Stackoverflow forums, e.g.
# https://stackoverflow.com/questions/56611698/pandas-how-to-read-csv-file-from-google-drive-public
# Alternatively, download the file and then just use pd.read_csv(filename)
# Read more about how to read csv files and DataFrame here: https://www.listendata.com/2019/06/pandas-read-csv.html
#############################################################################



url='https://drive.google.com/file/d/1SGhQMRjWKc2F57FBeb4rXv16T7xUvMS4/view?usp=sharing'

path = 'https://drive.google.com/uc?id='+url.split('/')[-2]
df = pd.read_csv(path) #read csv file
print(df.head(10)) #print the first 10 lines on the screen
                                 
print('The number of (rows, columns) =',df.shape) #inspecting the data - write the numbers of rows and columns

input('Press Enter to continue...') # pause the script until Enter is pressed
                                    # to inspect the file

# Let's assign the columns to the variables reqired for further work
x=df['X(km)'] 
y=df['Y(km)']
h=df['Thickness(m)'] 
conc=df['Concentration(ppm)']/1e6 #Volume fraction of copper 
                                
                                   
                                      

####### PROBLEM 1: TOTAL AMOUNT OF COPPER IN TONNES ##########################
#
# Assume that measurements in 598 wells are representative for the whole 
# investigated area of 598 km2 (13km x 46km), i.e. that the measurements
# in each well are representative for the area of 1km2 (note that this is a very
# crude assumption. The correct way would be to interpolate the thickness and
# concentration values between the wells with one of the methods, such as linear
# interpolation, kriging, spline interpolation etc.)
# 
# Volume of copper-bearing formation per each well (m3) = Thickness (m) x Area (m)
# Volume of copper per well = Volume (m3) x ppm
# Mass of copper per well = Volume of copper x Density of copper
# Total mass of copper = sum of the mass in each well
#
# Here we will use 'for loop' (to repeat the calculation for each well). Find 
#more about for loops at: https://wiki.python.org/moin/ForLoop
##############################################################################

N_wells=len(h) #Number of wells
Area=1000000 #Representative area for each well is 1e6 m2 (1km2)
ro=8960 #Density of copper = 8960kg/m3
Mass=0 #Initialise total mass, we will add incrementally to it the mass of each well

for i in range(N_wells):    
    Mwell=h[i]*Area*ro*conc[i]/1000 #Mass per well in tonnes
    Mass=Mass+Mwell #Total mass in tonnes
    
# Note that for this simple case, you can use Mass=sum(h*Area*ro*conc), where
# the expression inside the brackets contains the result of all the wells. 
# You could also use numpy package and and define "h" and "conc" as arrays and
# perform element-by-element multiplication using dot product. 

print('Total mass of copper is %.3g tonnes' %Mass)
input ("Press Enter to continue...")


##### PROBLEM 2: FIND THE CENTRE OF 3km x 3km MINE THAT WILL CONTAIN ########
#####            THE MOST COPPER                                     ########
#
# The data need to be re-arranged to 2D arrays (x,y) covering the whole area.
# Yuo can think about it as grid (or matrix), where each point on the grid 
# (element of the matrix) has (x,y) coordinates. If x runs in E-W direction,
# and y in N-S direction, then the number of columns of our 2D array will be 13 (x-values)
# and the number of rows 46 (y-values). 
# 'Numpy' is required for working with arrays. This is a numerical Python
# library. Find more about it here: https://www.w3schools.com/python/numpy/default.asp
##############################################################################

Mwell_Cu = h*conc*Area*ro/1000 #Copper mass in tonnes in each well as panda series
Mwell_Cu_arr=np.array(Mwell_Cu) #Convert panda series into numpy array in order to be
                          #able to reshape it into a matrix/grid

Mwell2D_Cu = Mwell_Cu_arr.reshape(46,13) #Converting 1D array to 2D array (matrix/grid)

Mmine_Cu_max= 0 #initialise the mass of the mine with the most copper


# Do the same with x and y in order to check if your grid is correctly created
x_arr=np.array(x)
y_arr=np.array(y)
x2D=x_arr.reshape(46,13)
y2D=y_arr.reshape(46,13)
print("x-coordinates of the grid:")
print(x2D)
input ("Press Enter to continue")

print("y-coordinates of the grid:")
print(y2D)
input("Press Enter to continue...")

# 3km x 3km mine will occupy the are defined by 3x3 wells (remember that we assumed
# that each well data cover the area of 1km2 - note, this is a very crude assumption)
# We will search all such 3x3 rectangles, starting from the first row and column
# of our grid and finishing at the (last-2) row and column of our grid. Note that this
# can be done in many different ways, this is not the only one.
 
for j in range(x2D.shape[1]-2): #run over all the columns
    for i in range(x2D.shape[0]-2): #run over all the rows
        Mmine_Cu = np.sum(Mwell2D_Cu[i:i+2,j:j+2]) #Mass  of the proposed 3km x 3km mine
        X_mean = np.mean(x2D[i:i+2,j:j+2]) #  Central x-coordinate of the mine
        Y_mean = np.mean(y2D[i:i+2,j:j+2]) # Central y-coordinate of the mine
        
     #Check  if the mass of Cu in the current 3km x 3km mine is greater than Mmine_cu_max.
     # If it is, than it becomes Mmine_Cu_max. In this way we will find the mine with the 
     # most copper. More about "if" statement can be found at:
     # https://www.w3schools.com/python/python_conditions.asp
        
        if Mmine_Cu > Mmine_Cu_max: 
           Mmine_Cu_max = Mmine_Cu
           Xmine=X_mean # Remember the central coordinates of the mine with the most Cu
           Ymine=Y_mean
          
#Print the results. Find more about possible output formats here:
# https://www.w3schools.com/python/python_string_formatting.asp
print("The best location for the mine is x = %.2f and y = %.2f" %(Xmine, Ymine))
print("The amount of copper in this mine is %.4g tonnes" %Mmine_Cu_max)




######### PROBLEM 3: MAKE A CONTOUR COLOUR PLOT OF the CU MASS DISTR. ########
#
# 'Matplolib' library is used for plotting. 
# There are many different ways to plot colour 2D plots (contourf, pcolor etc.)
# for some examples check https://jakevdp.github.io/mpl_tutorial/tutorial_pages/tut3.html
# or https://www.python-course.eu/matplotlib_contour_plot.php. 
# Remember, there are many ways of creating and formatting the plot. Pick the simplest
# which satisfies the task. 
##############################################################################


fig, ax = plt.subplots() # Create figure and plot, so you can refer to the plot (ax) later

# See how to plot contourplots at https://matplotlib.org/stable/gallery/images_contours_and_fields/contourf_demo.html
#We will use the colourmap 'jet'. there are many other colourmaps available, such as 
# 'bone', 'jet', 'ocean' etc: https://matplotlib.org/stable/tutorials/colors/colormaps.html
heatmap = ax.contourf(x2D, y2D, Mwell2D_Cu/1e6, cmap='jet',levels=50) # Create the heatmap
cbar = plt.colorbar(heatmap, orientation="vertical",shrink=0.75, pad=0.1) #Add colourbar; "pad" defines the distance from the plot measured asthe fraction of the plot axes. 
cbar.set_label('Mass of Cu [Mt]', rotation=270, labelpad=10 ) #Add the label and rotate it from 270 degrees; labelpad defines the distance from the colourbar
ax.set_title('Mass distribution of Cu (in Megatonnes)') # Image title
ax.set_xlabel('X [km]') #X-axis label
ax.set_ylabel('Y [km]') # Y-axis label
ax.set_aspect('equal') # If you want, plot x and y axes in the same scale 

# And we are done! 
# Now, if you get a new dataset we the same question, you need  just seconds to run the script
# It is a good habit to write the data input and data analysis parts as separate functiones (modules).
# In this way you can, for example, combine the function for reading the data with any other function 
# for data analysis. This gives you flexibility and imporves performance, especially if you often deal
# with the same type of datasets/input files, for which you need to do different data analisys tasks. 
# A great resource for beginner: https://www.w3schools.com/python/

 