import math
import random
import numpy as np
import matplotlib.pyplot as plt

xdim = 1024  # x dimension of image
ydim = 1024  # y dimension of image


# smooths the noise using interpolation
def fade(t):
    return 3*(t**2) -2*(t**3)

# finds closes edge to a pixel
def findEdge(x, y, size_box):
    if x % size_box == 0 and y % size_box == 0:
        return (math.ceil(x/size_box)+1,math.ceil(y/size_box)+1)
    elif x % size_box == 0 :
        return (math.ceil(x/size_box)+1,math.ceil(y/size_box))
    elif y % size_box == 0 :
        return (math.ceil(x/size_box),math.ceil(y/size_box)+1)
    else:
        return math.ceil(x/size_box), math.ceil(y/size_box) # returns outer 2 edges contain x and y
        
# creates the creates the perlin noise array
def makeNoise(num_boxes):
    global xdim, ydim
    pixels = np.zeros((xdim,ydim))
    size_box = int(xdim/num_boxes)
    boxes =[]
    
    # array of sqaures in the grid 
    for j in range(0, xdim+size_box, size_box):
            for k in range(0, ydim+size_box, size_box):
                boxes.append([k,j])

    boxes = np.asarray(boxes)
    corners = np.reshape(boxes, (num_boxes+1,num_boxes+1,2))   # squares converted to corners
    
    
    # generates a vector for each corner in the grid using the unit circle
    vectors =[]
    for i in range(len(boxes)):
        radians = (2*math.pi) * random.uniform(0, 1)
        vectors.append([round(math.cos(radians),3), round(math.sin(radians),3)])

    vectors = np.asarray(vectors)
    vectors = np.reshape(vectors,(num_boxes+1,num_boxes+1,2))
    
    
    # creates noise using perlin noise algorithim
    for x in range(xdim):
        for y in range(ydim):
            edge4 = findEdge(x, y, size_box) 

            # finds nearest edges to the specified pixel
            edge1 = (edge4[0]-1,edge4[1]-1) #[0,0]
            edge2 = (edge4[0]-1,edge4[1]) #[0,1]
            edge3 = (edge4[0],edge4[1]-1) #[1,0]
            edge4 = edge4 #[1,1]

            # finds the nearest corners based on the calculated edges
            corner1 = corners[edge1[::-1]]
            corner2 = corners[edge2[::-1]]
            corner3 = corners[edge3[::-1]]
            corner4 = corners[edge4[::-1]]

            # calculates the distance between each corner and a pixel and normalizes them based on the size of each box
            dist1 = np.array([x-corner1[0], y-corner1[1]])/size_box 
            dist2 = np.array([x-corner2[0], y-corner2[1]])/size_box
            dist3 = np.array([x-corner3[0], y-corner3[1]])/size_box
            dist4 = np.array([x-corner4[0], y-corner4[1]])/size_box 

            # stores the vector for the specifed corners using the calculated edges
            vect1 = vectors[edge1]
            vect2 = vectors[edge2]
            vect3 = vectors[edge3]
            vect4 = vectors[edge4]

            # calculates the dot product between all 4 vectors and uses the fading function to smooth it
            dp1 = (vect1@dist1)*fade(1-dist1[0])*fade(1-dist1[1])
            dp2 = (vect2@dist2)*fade(1-dist1[0])*fade(dist1[1])
            dp3 = (vect3@dist3)*fade(dist1[0])*fade(1-dist1[1])
            dp4 = (vect4@dist4)*fade(dist1[0])*fade(dist1[1])
            
            sums = dp1+dp2+dp3+dp4 # sums all the dot products
            pixels[x][y] = sums # sets the pixel to the sum of all dot products
            
    return pixels


def add_contrast(img,amt): #change
    im2 = amt*(img-128)/128
    return 256 / (1 + np.exp(-1*im2))

def make_map():
    # map 1
    raw = makeNoise(4)  # makes an array with noise using 4 boxes 

    raw -= np.amin(raw)  # finds the minimum value in the array and ensures non negative pixels
    raw /= np.amax(raw)  # finds the maximum value in the array and normalizes the pixels
    final1 = 256*raw     # creates the rgb value for each pixel

    # map 2
    raw2 = makeNoise(16)
    
    raw2 -= np.amin(raw2)
    raw2 /= np.amax(raw2)
    final2 = 256*raw2

    # map 3
    raw3 = makeNoise(64)
    
    raw3 -= np.amin(raw3)
    raw3 /= np.amax(raw3)
    final3 = 256*raw3
    
    completeMap = (0.4*final1)+ (0.4*(final2))+ (0.2*(final3))    # adds all 3 maps on top of each other to create 1 map
    added = add_contrast(completeMap,4)
    added -= np.amin(added)
    added /= np.amax(added)
    added = 256*added
    
    return completeMap


# plots the generated noise
completeMap = make_map()

fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(completeMap, cmap='gray', vmin=0, vmax=256, interpolation='nearest')





# uses the generated noise to make a map
def generate_map(noise, xdim, ydim):
    new_pixels = np.zeros((512,512,3))
    for x in range(xdim):
        for y in range(ydim):
            if noise[x,y] < 105: # change the values to created different patterns
                new_pixels[x,y] = [165,186,58] #green (change the rgb values to whatever colors you want)
            elif noise[x,y] < 120:
                new_pixels[x,y] = [245,219,136] #yellow (change the rgb values to whatever colors you want)
            else:
                new_pixels[x,y] = [0,70,170] #blue (change the rgb values to whatever colors you want)
    return new_pixels

# plots the generated map
gm = generate_map(completeMap, 512, 512)

fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(gm/256, vmin=0, vmax=256, interpolation='nearest')
