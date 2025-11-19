 Home  
3D

Python

Terrain

3D Terrain Modelling in Python
3D Terrain Modelling in Python
 Home  
3D

Python

Terrain

3D Terrain Modelling in Python
Tuesday, September 3, 2019
AUTHOR
geomatics
Follow @ideageo
3D modelling is a nice way to view an object in order to get a more vivid visualization with more intense feeling as if we can touch it. Also in viewing topographic surface or terrain, 3D modelling gives more detail surface features in every angle of a region compare with 2D visualization. If we have a set of height point from topographic survey, we will need some processing steps to get a contour map and view the result in 3D. It can be done using some proprietary software like Surfer, ArcGIS ArcScene, Autodesk AutoCAD Map or even using Open Source Software like QGIS 3.x. In this post, I won't discuss any of those. Moreover I will show you how to create a 3D terrain model with a set of height point from topographic or field measurement in Python. So at the end of this tutorial we will get a 3D terrain surface like figure 1 below.
Figure 1. 3D Terrain Modelling in Python
3D Terrain Modelling Technical Approach
Before writing this post, I had done some experiments with different technical approaches and results. It took some times till I got a good one and decided to share the result with you. So this post shows the final result. But before discussing how to do it step by step, let me explain briefly the story "behind the scene" until I come to this point.
Choosing Python Graphic Library
Matplotlib is the first graphic library I know when started learning Python. I use it frequently to plot any graph I need. So firstly I used Matplotlib to model a terrain surface in 3D. I found there are some functions to plot 3D model in Matplotlib such as wireframe, surface and trisurf. Figure 2 shows 3D terrain from Matplotlib's surface function.
Figure 2. 3D terrain modelling with Matplotlib surface plot
The first output from Matplotlib made me so happy, now  I can make a terrain 3D model in Python. But later on I found the output with Matplotlib was getting slower as number of point increasing. Previously with a fewer points I can freely rotate it without any delay, but the terrain rendering became slower and needed longer time to compute when the surface is getting more complex with thousand points. It's hard to forget the first love, but really sorry I need to find something else.
Finally after some adventures, I found Plotly library is a good one to model the terrain in 3D. It renders faster, smoother and it can produce a html output with some tools that enabled us to zoom in, zoom out, pan, rotate, export to static image and so forth.
Populate Interpolation Points
Might be you have a question. Why are there more points are required in creating 3D model and even getting thousands? In fact the point from field measurement many fewer that that? Actually when doing topographic measurement, what someone do is taking a number of sampling point appropriately in the surveying area. Then we populate more points that cover the whole region and estimate the height based on the measurement points, so we can model the 3D surface for the area that close to the actual condition.
Let's take an example to make it more concrete and easy to understand. One day, we did a topographic survey of a region with area 100 x 100 m. From the survey, we took 50 measurement points (blue dots). Then we do interpolation every 5 m for both X and Y axis, so we have 20 points for X and 20 points for Y. In total, the number of interpolation points will be 400 points (red dots) as shown in figure 3. What about 1 m interval? how many points will it be? simply 100 x 100=10000 points.
Figure 3. Measurement and interpolation points
Interpolation Method
Next question could be, how we estimate the height of interpolation points? There are many spatial interpolation methods available such as linear interpolation, Inverse Distance Weight (IDW) and Kriging. I chose IDW because we can estimate an unknown point at any location and it's rather more simple to implement than Kriging method. On the other hand, the linear interpolation can only interpolate at any location between two known points along a straight line that connected the two known points. It can be used for creating contour line but not suitable for 3D topographic surface modelling. Please refer to my post about creating contour lines and IDW spatial interpolation for further explanation.
From the explanation above, I'm sure you can grasp the main idea how to model a 3D terrain in Python. But let me write it down for clarity.
The surface function from Plotly library is used to construct a 3D terrain model, .
Defined an interval distance and populate interpolation points that cover the whole area.
Estimate the height of unknown/interpolation points using IDW spatial interpolation method.
3D Terrain Modelling: Python Part
Now let's dive into the code. For this tutorial I used Jupyterlab 1.0 with Python 3.7.4, Plotly 4.1.0 and Numpy 1.16.4. For Ploty installation you can refer to Plotly manual. Firstly let's import the Numpy and Plotly libraries with the following code.
import numpy as np
import plotly.offline as go_offline
import plotly.graph_objects as go
Before proceeding to the next step, please run the code. If there is no error appears, it means the required libraries already installed. If not, install the required library  properly.
Reading Data
For this tutorial I used a height dataset around 100 points. The data is in CSV format that contains x,y and z/elevation columns as seen in figure 4.
Figure 4. Height dataset
The data can be downloaded here or you can use your own data if you have one. But I suggest to use the sample data first. If everything works well until you can get 3D terrain, then you can switch to your own data. But please keep in mind the coordinate of data must be in projected coordinate system with meter unit. That's because we will calculate distance and use it for weight determination.
Next we will read and parsing the data into x, y and z. Therefore we initiated three list to store x and y coordinate and z or elevation value. To confirm if the data are stored correctly, then try to plot it using Scatter function in Plotly. If you can see the scatter plot of height points as shown in figure 5, then everything works fine till this step.
Anyway we don't need the height point scatter plot, so after successful storing data into respected list and seeing the plot, pelase comment or delete the plotting line code.
#READING AND PARSING THE DATA
file=open('F:/3D_Terrain/survey_data.csv','r')
lines=file.readlines()
n_line=len(lines)
x=[]
y=[]
z=[]
for i in range(1,n_line):
split_line=lines[i].split(",")
xyz_t=[]
x.append(float(split_line[0].rstrip()))
y.append(float(split_line[1].rstrip()))
z.append(float(split_line[2].rstrip()))
Figure 5. Height scatter plot
IDW Function
Now it's time to create IDW function which will be used to estimate the height value interpolation point. For this one I used IDW algorithm that estimate an unknown value based on a minimum number of point. Detail explanation about the function can be found in another post that described how to create IDW interpolation in Python.
The IDW function code can be seen in the following code.
#DISTANCE FUNCTION
def distance(x1,y1,x2,y2):
d=np.sqrt((x1-x2)**2+(y1-y2)**2)
return d
#CREATING IDW FUNCTION
def idw_npoint(xz,yz,n_point,p):
r=10 #block radius iteration distance
nf=0
while nf<=n_point: #will stop when np reaching at least n_point
x_block=[]
y_block=[]
z_block=[]
r +=10 # add 10 unit each iteration
xr_min=xz-r
xr_max=xz+r
yr_min=yz-r
yr_max=yz+r
for i in range(len(x)):
# condition to test if a point is within the block
if ((x[i]>=xr_min and x[i]<=xr_max) and (y[i]>=yr_min and y[i]<=yr_max)):
x_block.append(x[i])
y_block.append(y[i])
z_block.append(z[i])
nf=len(x_block) #calculate number of point in the block
#calculate weight based on distance and p value
w_list=[]
for j in range(len(x_block)):
d=distance(xz,yz,x_block[j],y_block[j])
if d>0:
w=1/(d**p)
w_list.append(w)
z0=0
else:
w_list.append(0) #if meet this condition, it means d<=0, weight is set to 0
#check if there is 0 in weight list
w_check=0 in w_list
if w_check==True:
idx=w_list.index(0) # find index for weight=0
z_idw=z_block[idx] # set the value to the current sample value
else:
wt=np.transpose(w_list)
z_idw=np.dot(z_block,wt)/sum(w_list) # idw calculation using dot product
return z_idw
Populate Interpolation Points
At this step we are creating a number of interpolation points that covered the whole area. Based on the number of point specified in variabel n, then x and y interval will be defined by divided the width and the lenght of area with n. Using the interval for x and y axis, then the interpolation point will be populated and stored to x and y interpolation list. The estimation of height will be calculated for each interpolation point and stored in z interpolation list.
# POPULATE INTERPOLATION POINTS
n=100 #number of interpolation point for x and y axis
x_min=min(x)
x_max=max(x)
y_min=min(y)
y_max=max(y)
w=x_max-x_min #width
h=y_max-y_min #length
wn=w/n #x interval
hn=h/n #y interval
#list to store interpolation point and elevation
y_init=y_min
x_init=x_min
x_idw_list=[]
y_idw_list=[]
z_head=[]
for i in range(n):
xz=x_init+wn*i
yz=y_init+hn*i
y_idw_list.append(yz)
x_idw_list.append(xz)
z_idw_list=[]
for j in range(n):
xz=x_init+wn*j
z_idw=idw_npoint(xz,yz,5,1.5) #min. point=5, p=1.5
z_idw_list.append(z_idw)
z_head.append(z_idw_list)
Plot 3D Terrain Model
After creating interpolation points, we are ready to create 3D terrain model of the respected area. Make sure to delete the plotting line code that previously used to create scatter plot above. We will export the terrain model into a html file. When the process is finished it will print the path of the html on the Jupyter output cell.
# CREATING 3D TERRAIN MODEL
fig=go.Figure()
fig.add_trace(go.Surface(z=z_head,x=x_idw_list,y=y_idw_list))
fig.update_layout(scene=dict(aspectratio=dict(x=2, y=2, z=0.5),xaxis = dict(range=[x_min,x_max],),yaxis = dict(range=[y_min,y_max])))
go_offline.plot(fig,filename='F:/3D_Terrain/3d_terrain.html',validate=True, auto_open=False)
After opening the html file, you should see the 3D terrain surface plot with x, y, z axis and a color scale bar on the right. Play with it, use the Plotly tool to zoom in, zoom out, pan, rotate, export to an image, etc.
Congratulation, now you can create a 3D topographic surface or terrain modelling in Python using a set of height point data that could be taken from field measurement or other sources. You can tweak the plot with some Plotly setting options. If you want to learn more, please visit Plotly reference manual.
Thanks for reading this post. Give any comment if you find something interesting to discuss and please share it if you think other people will get benefit from it.
Complete source code.
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
#3D TERRAIN MODELLING
#CREATED BY: IDEAGORA GEOMATICS
#ORIGINAL SOURCE CODE AT WWW.GEODOSE.COM
import numpy as np
import plotly.offline as go_offline
import plotly.graph_objects as go
#READING AND PARSING THE DATA
file=open('F:/3D_Terrain/survey_data.csv','r')
lines=file.readlines()
n_line=len(lines)
x=[]
y=[]
z=[]
for i in range(1,n_line):
split_line=lines[i].split(",")
xyz_t=[]
x.append(float(split_line[0].rstrip()))
y.append(float(split_line[1].rstrip()))
z.append(float(split_line[2].rstrip()))
#DISTANCE FUNCTION
def distance(x1,y1,x2,y2):
d=np.sqrt((x1-x2)**2+(y1-y2)**2)
return d
#CREATING IDW FUNCTION
def idw_npoint(xz,yz,n_point,p):
r=10 #block radius iteration distance
nf=0
while nf<=n_point: #will stop when np reaching at least n_point
x_block=[]
y_block=[]
z_block=[]
r +=10 # add 10 unit each iteration
xr_min=xz-r
xr_max=xz+r
yr_min=yz-r
yr_max=yz+r
for i in range(len(x)):
# condition to test if a point is within the block
if ((x[i]>=xr_min and x[i]<=xr_max) and (y[i]>=yr_min and y[i]<=yr_max)):
x_block.append(x[i])
y_block.append(y[i])
z_block.append(z[i])
nf=len(x_block) #calculate number of point in the block
#calculate weight based on distance and p value
w_list=[]
for j in range(len(x_block)):
d=distance(xz,yz,x_block[j],y_block[j])
if d>0:
w=1/(d**p)
w_list.append(w)
z0=0
else:
w_list.append(0) #if meet this condition, it means d<=0, weight is set to 0
#check if there is 0 in weight list
w_check=0 in w_list
if w_check==True:
idx=w_list.index(0) # find index for weight=0
z_idw=z_block[idx] # set the value to the current sample value
else:
wt=np.transpose(w_list)
z_idw=np.dot(z_block,wt)/sum(w_list) # idw calculation using dot product
return z_idw
# POPULATE INTERPOLATION POINTS
n=100 #number of interpolation point for x and y axis
x_min=min(x)
x_max=max(x)
y_min=min(y)
y_max=max(y)
w=x_max-x_min #width
h=y_max-y_min #length
wn=w/n #x interval
hn=h/n #y interval
#list to store interpolation point and elevation
y_init=y_min
x_init=x_min
x_idw_list=[]
y_idw_list=[]
z_head=[]
for i in range(n):
xz=x_init+wn*i
yz=y_init+hn*i
y_idw_list.append(yz)
x_idw_list.append(xz)
z_idw_list=[]
for j in range(n):
xz=x_init+wn*j
z_idw=idw_npoint(xz,yz,5,1.5) #min. point=5, p=1.5
z_idw_list.append(z_idw)
z_head.append(z_idw_list)
# CREATING 3D TERRAIN
fig=go.Figure()
fig.add_trace(go.Surface(z=z_head,x=x_idw_list,y=y_idw_list))
fig.update_layout(scene=dict(aspectratio=dict(x=2, y=2, z=0.5),xaxis = dict(range=[x_min,x_max],),yaxis = dict(range=[y_min,y_max])))
go_offline.plot(fig,filename='F:/3D_Terrain/3d_terrain.html',validate=True, auto_open=False)

3D
Python
Terrain
Related Posts
Disqus Comments


Home