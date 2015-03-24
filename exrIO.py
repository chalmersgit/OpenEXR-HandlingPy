import OpenEXR, Imath, numpy

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
    #img = img.astype(numpy.float32)
    
    w, h, d = img.shape
    assert d == 3 or d == 4

    # get the channels
    red = numpy.array(img[:,:,0]).data
    green = numpy.array(img[:,:,1]).data
    blue = numpy.array(img[:,:,2]).data
    if d == 4: alpha = numpy.array(img[:,:,3]).data
    
    # Write the three color channels to the output file
    out = OpenEXR.OutputFile(filename, OpenEXR.Header(h,w))
    dict = {'R' : str(red), 'G' : str(green), 'B' : str(blue)}
    if d == 4: dict['A'] = alpha
    out.writePixels(dict)
    
    
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
    d = len(img.shape)
    if d >= 3:
        w, h,_ = img.shape
    else:
        w, h = img.shape
    assert d == 3 or d == 4 or d == 2

    if d == 2:
        if type(img[0]) != numpy.float32:
            img = img.astype(numpy.float32)
    elif d == 3:
        if type(img[0,0,0]) != numpy.float32:
            img = img.astype(numpy.float32)
    if d == 4:
        if type(img[0,0,0,0]) != numpy.float32:
            img = img.astype(numpy.float32)   
            
    # get the channels
    if d == 2:
        intensity = numpy.array(img[:,:]).data
    else:
        red = numpy.array(img[:,:,0])
        green = numpy.array(img[:,:,1])
        blue = numpy.array(img[:,:,2])
        itentensity_temp = (red+green+blue) / 3
        intensity = itentensity_temp.data
    
    # Write the three color channels to the output file
    out = OpenEXR.OutputFile(filename, OpenEXR.Header(h,w))
    dict = {'R' : str(intensity), 'G' : str(intensity), 'B' : str(intensity)}
    out.writePixels(dict)       