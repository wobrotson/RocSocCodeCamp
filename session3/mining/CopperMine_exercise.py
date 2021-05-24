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
   

Assumption: Assume that measurements in 598 wells are representative for the whole 
 investigated area of 598 km2 (13km x 46km), i.e. that the measurements
 in each well are representative for the area of 1km2 (note that this is a very
 crude assumption, but it will suffice for this exercise (correct way would
 be to interpolate the thickness and concentration values between the wells with 
 one of the methods, such as linear  interpolation, kriging, spline interpolation etc.
 - example of the interpolation is given in the end of this script)


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


######## INPUT INFO (urlname, constants etc) ##################################
# If you want to apply the same script to another dataset of the same type later,
# you just change the information witihin this block. Always try to define all your 
# constants at the start of the proogram, rather than putting the numbers directly in the code

urlname="https://drive.google.com/file/d/1SGhQMRjWKc2F57FBeb4rXv16T7xUvMS4/view?usp=sharing"
Nwells = 598
Nx = 13 # Number of wells in x-direction
Ny = 46 # Number of wells in y-direction
Area=1000000 # Representative are for each well (1km2 = 1000000 m2)
ro = 8960 # Densiti of copper in kg/m3
##############################################################################


######### READ CSV DATA FILE DIRECTLY FROM GOOGLE DRIVE ######################
# Read the csv file from Google drive share link (variable url) 
# url.split('/')[-2] takes the part of url between the last and second last slash ('/')
# pd.read_csv reads a csv file
# Check Stackoverflow forums, e.g.
# https://stackoverflow.com/questions/56611698/pandas-how-to-read-csv-file-from-google-drive-public
# Alternatively, download the file and then just use pd.read_csv(filename)
# Read more about how to read csv files and DataFrame here: https://www.listendata.com/2019/06/pandas-read-csv.html
#############################################################################



url=urlname

path = 'https://drive.google.com/uc?id='+url.split('/')[-2]
df = pd.read_csv(path) #read csv file
print(df.head(5)) #print the first 5 lines on the screen
                                 
print("The number of (rows, columns) =",df.shape) #inspecting the data - write the numbers of rows and columns

input("Press Enter to continue...") # pause the script until Enter is pressed
                                    # to inspect the file
                                    
                                    
                                    
# Let's assign the columns to the variables (this is not necessary, but it can be handy;
# you can change the names of the columns in df instead)
x=df['X(km)'] 
y=df['Y(km)']
h=df['Thickness(m)'] 
conc=df['Concentration(ppm)']/1e6 #Volume fraction of copper (note division by million)

# We can delete the variable df now, not to waste memory
del(df)

                                
                                   
                                      

####### PROBLEM 1: TOTAL AMOUNT OF COPPER IN TONNES ##########################
#
# Use the assumption from the problem description.
# 
# Volume of copper-bearing formation per each well (m3) = Thickness (m) x Area (m)
# Volume of copper per well = Volume (m3) x ppm
# Mass of copper per well = Volume of copper x Density of copper
# Total mass of copper = sum of the mass in each well
#
# Here we will use 'for loop' (to repeat the calculation for each well). Find 
#more about for loops at: https://wiki.python.org/moin/ForLoop
##############################################################################

TotMass=0 #Initialise total mass, we will add incrementally to it the mass of each well
for i in range(Nwells):    
    Mwell=h[i]*Area*ro*conc[i]/1000 #Mass per well in tonnes
    TotMass=TotMass+Mwell #Total mass in tonnes
    
# Note that for this simple case, it would be simpler to use Mass=sum(h*Area*ro*conc), where
# the expression inside the brackets contains the result of all the wells. 
# You could also use numpy package and and define "h" and "conc" as arrays and
# perform element-by-element multiplication using dot product. The for loop is 
# used here only for the reason to get familiar with it!!  

print("Total mass of copper is %.3g tonnes" %TotMass)
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

Mwell_Cu = h*conc*Area*ro/1000 #Copper mass in tonnes in each well (as panda series)
Mwell_Cu_arr=np.array(Mwell_Cu) #Convert panda series into numpy array in order to be
                                 #able to reshape it into a matrix/grid

Mwell2D_Cu = Mwell_Cu_arr.reshape(Ny,Nx) #Converting 1D array to 2D array (matrix/grid)
                                         # Ny - number of rows, Nx - number of columns

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
 
Mmine_Cu_max= 0 #initialise the mass of the mine with the most copper

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
#
# In the end, add a rectangle denoting the proposed mine to the plot.
##############################################################################
    
    
fig, ax = plt.subplots(figsize=(15,10)) # Create figure and plot, so you can refer to the plot (ax) later
    
# See how to plot contourplots at https://matplotlib.org/stable/gallery/images_contours_and_fields/contourf_demo.html
#We will use the colourmap 'jet'. there are many other colourmaps available, such as 
# 'bone', 'jet', 'ocean' etc: https://matplotlib.org/stable/tutorials/colors/colormaps.html
heatmap = ax.contourf(x2D, y2D, Mwell2D_Cu/1e6, cmap='jet',levels=50) # Create the heatmap (you can use 1D arrays for x and y instead of matrices)
cbar = plt.colorbar(heatmap, orientation="vertical",shrink=0.75, pad=0.06) #Add colourbar; "pad" defines the distance from the plot measured asthe fraction of the plot axes. 
cbar.set_label("Mass of Cu [Mt]", rotation=270, labelpad=20 ) #Add the label and rotate it from 270 degrees; labelpad defines the distance from the colourbar
ax.set_title("Mass distribution of Cu (in Megatonnes)", fontsize=14) # Image title
ax.set_xlabel("X [km]") #X-axis label
ax.set_ylabel("Y [km]") # Y-axis label
ax.set_aspect("equal") # If you want, plot x and y axes in the same scale 
    

# Let us add a red rectangle where the mine is supposed to be and make the same scale 
# for x and y axes
# Create a Rectangle patch
rect = plt.Rectangle((Xmine-1.5,Ymine-1.5), 3, 3, linewidth=1, edgecolor='r', facecolor='none') #Lower left corner of the rectangle (x,y) with respect to the centre of the mine. The rectangle is 3 km wide and 3 km high.    
    
# Add the patch to the Axes
ax.add_patch(rect)

#Same scale for both axes
ax.set_aspect('equal')
    
# Change the figure title
plt.title("Proposed location for copper mine",fontsize=14)


#Add the amount of copper in the proposed mine to the figure
ax.text(15, 3,"$Mass_{Cu}$ = %.3g Mt" %Mmine_Cu_max, fontsize=14)   
plt.show()


# And we are done! 
# Now, if you get a new dataset we the same question, you just need to change the input info in the 
# input block at the beginning of the program ans run the program again witihn seconds.
# It is a good habit to write the data input and data analysis parts as separate functiones (modules).
# In this way you can, for example, combine the function for reading the data with any other function 
# for data analysis. This gives you flexibility and imporves performance, especially if you often deal
# with the same type of datasets/input files, for which you need to do different data analisys tasks. 
# A great resource for beginner: https://www.w3schools.com/python/



###### BONUS: How to interpolate 2D dataset/grid/matrix? #####################

# We will interpolate our 1 km x 1 km 2D grid data "Mwell2D_Cu" to the 10 x 10 m grid.
# A functions to perform 2D spline interpolation is called "interp2D" and it can be found
# within "scipy.interpolate" (Scientific Python) library.
# Find more here: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp2d.html

# Import the library
from scipy import interpolate

# Re-create current x and y axis, and create new ones for interpolation
dx = 1 # current spatial interval between wells is 1km
dx_new = 0.01 # desired spatial interval is 10 m (0.01 km)
x = np.linspace(1,13,13)#linspace returns evenly spaced numbers linspace(start, end, number of elemenets)
y = np.linspace(1,46,46)

xnew=np.linspace(1,13,1201) # dx= 10 m (desired grid step); you can check the output by typing `print(xnew)`
ynew=np.linspace(1,46,4601)

# Interpolation
f = interpolate.interp2d(x, y, Mwell2D_Cu, kind='linear') # calculatiing interpolation function
Mwell2D_new=f(xnew,ynew) # interpolation (mass values are interpolated at (xnew, ynew) points and stored to Mwell2D_new)

#plot Mwell2D_Cu and Mwell2D_new using "pcolormesh" to compare them visually
fig1, (ax0,ax1)=plt.subplots(nrows=2,constrained_layout=True)
im0 = ax0.pcolormesh(x,y,Mwell2D_Cu,cmap='jet',shading='auto')
im1 = ax1.pcolormesh(xnew,ynew,Mwell2D_new,cmap='jet',shading='auto')
fig1.colorbar(im0,ax=ax0)
ax0.set_title("dx, dy = 1km")
fig1.colorbar(im1,ax=ax1)
ax1.set_title("dx, dy = 10 m")

###########THE END############################################################



 


 