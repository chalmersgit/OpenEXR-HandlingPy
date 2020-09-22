import OpenEXR, Imath, numpy

# If you have issues loading EXR images (e.g., compression type),
# you try modifying the headers. Examples are here:
# https://excamera.com/articles/26/doc/openexr.html#headers

def loadEXRnp(filename):
    # Open the input file
    file = OpenEXR.InputFile(filename)

    # Compute the size
    dw = file.header()['dataWindow']
    w, h = dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1

    # Read the three color channels as 32-bit float strings
    FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
    R, G, B = [file.channel(Chan, FLOAT) for Chan in ("R", "G", "B")]
    
    # make a numpy array
    def fs(x):
        return numpy.core.multiarray.fromstring(x, dtype = numpy.float32).reshape((h, w))
        
    red = fs(R)
    green = fs(G)
    blue = fs(B)
    
    img = numpy.zeros((h, w, 3), dtype = numpy.float32, order = "C")
    img[:,:,0] = red
    img[:,:,1] = green
    img[:,:,2] = blue
    
    return img

def saveEXRnp(img, filename):
	img = img.astype(numpy.float32) 
	
	w, h, d = img.shape
	assert d == 3 or d == 4

	# get the channels
	red = img[:,:,0].tobytes()
	green = img[:,:,1].tobytes()
	blue = img[:,:,2].tobytes()
	if d == 4: alpha = img[:,:,3].tobytes()

	# Make dictionary
	col_dict = {'R': red, 'G': green, 'B': blue}
	if d == 4: col_dict['A'] = alpha

	## Write the three color channels to the output file
	out = OpenEXR.OutputFile(filename, OpenEXR.Header(h,w))
	out.writePixels(col_dict)
    
    
def loadEXR_grey_np(filename):
    # Open the input file
    file = OpenEXR.InputFile(filename)

    # Compute the size
    dw = file.header()['dataWindow']
    w, h = dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1

    # Read the three color channels as 32-bit float strings
    FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
    R, G, B = [file.channel(Chan, FLOAT) for Chan in ("R", "G", "B")]
    
    # make a numpy array
    def fs(x):
        return numpy.core.multiarray.fromstring(x, dtype = numpy.float32).reshape((h, w))
        
    red = fs(R)
    green = fs(G)
    blue = fs(B)
    
    img = numpy.zeros((h, w), dtype = numpy.float32, order = "C")
    img[:,:] = (red+green+blue)/3
    
    return img

def saveEXR_grey_np(img, filename):
	img = img.astype(numpy.float32) # comment this out if we have problems

	d = len(img.shape)
	if d >= 3:
		w, h, _ = img.shape
	else:
		w, h = img.shape
	assert d == 3 or d == 4 or d == 2
			
	# get the channels
	if d == 2:
		intensity = numpy.array(img[:,:]).data
	else:
		red = numpy.array(img[:,:,0])
		green = numpy.array(img[:,:,1])
		blue = numpy.array(img[:,:,2])
		itentensity_temp = (red+green+blue) / 3
		intensity = itentensity_temp.data
	
	intensity = intensity.tobytes()

	# Write the three color channels to the output file
	out = OpenEXR.OutputFile(filename, OpenEXR.Header(h,w))
	dict = {'R' : intensity, 'G' : intensity, 'B' : intensity}
	out.writePixels(dict)       
