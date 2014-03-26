"""
    Module adpil -- Toolbox adpil
    -------------------------------------------------------------------
    This module provides a link between numpy arrays and PIL, Python Imaging
    Library, images. Its functions perform image file I/O (in formats supported
    by PIL) and displaying of images represented as numpy arrays. The layout
    of these numpy arrays follows the rules of the adimage toolbox images.
    -------------------------------------------------------------------
    adimages()    -- List image files located on sys.imagepath, if this variable
                     exists, or, otherwise, on sys.path
    adread()      -- Read an image from a file to a numpy array.
    adshow()      -- Display an image
    adshowclear() -- Close all adshow windows.
    adshowfile()  -- Display an image file
    adshowmode()  -- Set/get the current operational mode.
    adwrite()     -- Write an image from a numpy array to an image file. The
                     format is deduced from the filename extension.
    array2pil()   -- Convert a numpy array to a PIL image
    pil2array()   -- Convert a PIL image to a numpy array

"""
#
__version__ = '1.0 all'

__version_string__ = 'Toolbox adpil V1.0 28Jul2003'

__build_date__ = '04aug2003 11:29'
#

#

#
# =====================================================================
#
#   Global statements for adread
#
# =====================================================================
def findImageFile(filename):
    '''Search image filename in sys.imagepath or sys.path.'''
    import sys, os.path
    if not os.path.isfile(filename) and not os.path.isabs(filename):
        try:
            for a in sys.imagepath:
                if os.path.isfile(os.path.join(a, filename)):
                    filename = os.path.join(a, filename)
                    break
        except:
            for a in sys.path:
                if os.path.isfile(os.path.join(a, filename)):
                    filename = os.path.join(a, filename)
                    break
    return filename
# =====================================================================
#
#   adread
#
# =====================================================================
def adread(imagefile):
    """
        - Purpose
            Read an image from a file to a numpy array.
        - Synopsis
            arr = adread(imagefile)
        - Input
            imagefile: Image file path.
        - Output
            arr: numpy array representing an image.

    """

    import Image
    img = findImageFile(imagefile)
    arr = pil2array(Image.open(img))
    return arr
#
# =====================================================================
#
#   adreadgray
#
# =====================================================================
def adreadgray(imagefile):
    """
        - Purpose
            Read an image from a file to a numpy array as grayscale.
        - Synopsis
            arr = adread(imagefile)
        - Input
            imagefile: Image file path.
        - Output
            arr: numpy array representing an image.

    """

    import Image
    img = findImageFile(imagefile)
    arr = pil2array(Image.open(img).convert('L'))
    return arr
#
# =====================================================================
#
#   adwrite
#
# =====================================================================
def adwrite(imagefile, arr):
    """
        - Purpose
            Write an image from a numpy array to an image file. The format
            is deduced from the filename extension.
        - Synopsis
            adwrite(imagefile, arr)
        - Input
            imagefile: Image file path.
            arr:       The numpy array to save.

    """

    array2pil(arr).save(imagefile)
    return
#
# =====================================================================
#
#   Global statements for adimages
#
# =====================================================================
def listImageFiles(glb='*'):
    '''List image files located on sys.path.'''
    import sys, os.path, glob
    if os.path.splitext(glb)[1] == '':
        imgexts = ['.tif', '.jpg', '.gif', '.png', '.pbm', '.pgm', '.ppm', '.bmp']
    else:
        imgexts = ['']
    images = {}
    try:
        for dir in sys.imagepath:
            for ext in imgexts:
                for ff in glob.glob(os.path.join(dir, glb + ext)):
                    images[os.path.basename(ff)] = ff
    except:
        for dir in sys.path:
            for ext in imgexts:
                for ff in glob.glob(os.path.join(dir, glb + ext)):
                    images[os.path.basename(ff)] = ff
    return images
# =====================================================================
#
#   adimages
#
# =====================================================================
def adimages(glob='*'):
    """
        - Purpose
            List image files located on sys.imagepath, if this variable
            exists, or, otherwise, on sys.path
        - Synopsis
            imglist = adimages(glob='*')
        - Input
            glob: Default: '*'. Glob string for the image filename.
        - Output
            imglist: Image filename list.

    """

    lst = listImageFiles(glob).keys()
    lst.sort()
    return lst
    return imglist
#
# =====================================================================
#
#   Global statements for adshow
#
# =====================================================================
try:
    ################################################################################
    ##
    ##    ImageViewer implementation. Uses Tk idle loop
    ##
    ################################################################################
    import numpy
    import Tkinter
    import Image, ImageTk
    def tkRoot ():
        '''Returns the current Tk root.'''
        if Tkinter._default_root is None:
            root = Tkinter.Tk()
            Tkinter._default_root.withdraw()
        else:
            root = Tkinter._default_root
        return root
    tk_root = None      # posterga a ativacao do Tk ateh que adshow seja chamado
    show_mode = 0       # qdo 1, cria sempre um novo viewer
    #
    class ImageViewer(Tkinter.Toplevel):
        '''The implementation base class for adshow.'''
        viewmap = {}
        geomap = {}
        def __init__(self, arr, id, title=None, slider=None, events=None, status=False):
            self.image = arr
            self.image_label = None
            self.id = id
            self.var = Tkinter.IntVar()
            self.var.set(0)
            ImageViewer.viewmap[id] = self
            Tkinter.Toplevel.__init__(self)
            self.protocol("WM_DELETE_WINDOW", self.done)
            self.bind('<Escape>', self.onQuit)
            self.image_label = self.getTkLabel(arr)
            self.status = None
            self.scale = None
            if slider is not None:
                # p. ex. slider = {'label': 'XXX', 'min': 0, 'max': 100, 'incr': 1, 'cb': None}
                self.cb = slider['cb']
                self.scale = Tkinter.Scale(self, label=slider['label'],
                                                 command=self.onMove,              # catch moves
                                                 variable=self.var,                # reflects position
                                                 from_=slider['min'],
                                                 to=slider['max'],
                                                 resolution=slider['incr'],
                                                 bigincrement=slider['big'],
                                                 highlightcolor='#8080FF',
                                                 highlightthickness=3,
                                                 width=10,
                                                 showvalue=Tkinter.YES, orient='horizontal')
                self.scale.pack(fill='both', expand=1, side=Tkinter.TOP)
            self.image_label.pack(fill='both', expand=1, side=Tkinter.TOP)
            self.image_label.tkraise()
            if status:
                self.status = Tkinter.Label(self, text='Status', bg='gray', bd=1, justify=Tkinter.LEFT, font=('courier',8,'bold'))
                self.status.pack(fill='both', expand=1)
            if events is not None:
                # p. ex. events = {'<B1-Motion>': cb1, ...}
                for ev in events.keys():
                    self.image_label.bind(ev, events[ev])
            self.tkraise()

        def show(self, arr, title=None):
            self.image = arr
            if title is not None:
                self.title(title)
            self.TKimage = self.getTkImage(arr)
            self.image_label.configure(image=self.TKimage)
            self.image_label.tkraise()
            if self.geomap.get(self.id):
                self.geometry(self.geomap[self.id])
            self.tkraise()

        def getTkLabel(self, arr):
            self.TKimage = self.getTkImage(arr)
            return Tkinter.Label(self, image=self.TKimage, bg='gray', bd=0)
        def getTkImage(self, arr):
            self.PILimage = array2pil(arr)
            return ImageTk.PhotoImage(self.PILimage)
        def done(self):
            self.geomap[self.id] = self.geometry()
            del ImageViewer.viewmap[self.id]
            self.destroy()
        def onMove(self, posit):
            if self.cb is not None:
                self.cb(posit)
        def onQuit(self, ev):
            import sys
            sys.exit(0)
    ################################################################################
    HAS_TK = True
except:
    HAS_TK = False
# =====================================================================
#
#   adshow
#
# =====================================================================
def adshow(arr, title='adshow', id=0, slider=None, events=None, status=False):
    """
        - Purpose
            Display an image
        - Synopsis
            adshow(arr, title='adshow', id=0)
        - Input
            arr:   The numpy array to display.
            title: Default: 'adshow'. Title of the view window.
            id:    Default: 0. An identification for the window.

        - Description
            Display an image from a numpy array in a Tk toplevel with
            title given by argument 'title'.

    """
    if HAS_TK:
        import numpy
        global tk_root
        global show_mode
        if tk_root is None:
            # ativa Tk
            tk_root = tkRoot()
        if arr.dtype.char == '?':
            arr = numpy.array(arr*255).astype('B')
        if show_mode:
            vw = ImageViewer(arr, len(ImageViewer.viewmap.keys()), title, slider, events, status)
        elif ImageViewer.viewmap.get(id):
            vw = ImageViewer.viewmap[id]
        else:
            vw = ImageViewer(arr, id, title, slider, events, status)
        vw.show(arr, title)

#
# =====================================================================
#
#   adshowmode
#
# =====================================================================
def adshowmode(newmode=None):
    """
        - Purpose
            Set/get the current operational mode.
        - Synopsis
            mode = adshowmode(newmode=None)
        - Input
            newmode: Default: None. New operational mode. If None, returns
                     the current mode. Mode values are 0: the adshow arg
                     'id' identifies the window where to display the image;
                     1: create a new window for each image.
        - Output
            mode: Current mode.

    """

    global show_mode
    if newmode:
        show_mode = newmode
    return show_mode
    return mode
#
# =====================================================================
#
#   adshowclear
#
# =====================================================================
def adshowclear():
    """
        - Purpose
            Close all adshow windows.
        - Synopsis
            adshowclear()

    """

    for id in ImageViewer.viewmap.keys():
        ImageViewer.viewmap[id].done()

#
# =====================================================================
#
#   adshowfile
#
# =====================================================================
def adshowfile(filepath, id=0):
    """
        - Purpose
            Display an image file
        - Synopsis
            adshowfile(filepath, id=0)
        - Input
            filepath: Image file path.
            id:       Default: 0. An identification for the window.

        - Description
            Display an image file. Uses adshow(). The title is the tail of
            the filename. Argument 'id' is the same as adshow().

    """

    import os.path
    path = findImageFile(filepath)
    img = adread(path)
    adshow(img, os.path.basename(filepath), id)
    return
#
# =====================================================================
#
#   pil2array
#
# =====================================================================
def pil2array(pil):
    """
        - Purpose
            Convert a PIL image to a numpy array
        - Synopsis
            arr = pil2array(pil)
        - Input
            pil: The PIL image to convert.
        - Output
            arr: numpy array representing the PIL image.
        - Description
            Convert a PIL image to a numpy array. The array representing a
            RGB(A) image is formed by images stored sequencially: R-image,
            G-image, B-image and, optionally, Alpha-image.

    """

    import numpy
    w, h = pil.size
    binary = 0
    if pil.mode == '1':
        binary = 1
        pil = pil.convert('L')
    if pil.mode == 'L':
        d = 1 ; shape = (h,w)
    elif pil.mode == 'P':
        if 0:   # len(pil.palette.data) == 2*len(pil.palette.rawmode):
            binary = 1
            pil = pil.convert('L')
            d = 1 ; shape = (h,w)
        else:
            pil = pil.convert('RGB')
            d = 3 ; shape = (h,w,d)
    elif pil.mode in ('RGB','YCbCr'):
        d = 3 ; shape = (h,w,d)
    elif pil.mode in ('RGBA','CMYK'):
        d = 4 ; shape = (h,w,d)
    else:
        raise TypeError, "Invalid or unimplemented PIL image mode '%s'" % pil.mode
    arr = numpy.reshape(numpy.fromstring(pil.tostring(), 'B', w*h*d), shape)
    if d > 1:
        arr = numpy.swapaxes(numpy.swapaxes(arr, 0, 2), 1, 2)
    if binary:
        arr = arr.astype('?')
    # return arr
    return arr
#
# =====================================================================
#
#   array2pil
#
# =====================================================================
def array2pil(arr):
    """
        - Purpose
            Convert a numpy array to a PIL image
        - Synopsis
            pil = array2pil(arr)
        - Input
            arr: numpy array to convert.
        - Output
            pil: The resulting PIL image.
        - Description
            Convert a numpy array to a PIL image. Use the conventions
            explained in the pil2array docstring.

    """
    import Image
    nd = len(arr.shape)
    x = arr.astype('B')
    if nd == 2:
        d, h, w = (1,) + arr.shape
        mode = 'L'
    elif nd == 3:
        if arr.dtype.char == '?':
            raise TypeError, "Binary array cannot be RGB"
        d, h, w = arr.shape
        if   d == 1: mode = 'L'
        elif d == 3: mode = 'RGB'
        elif d == 4: mode = 'RGBA'
        else:
            raise TypeError, "Array first dimension must be 1, 3 or 4 (%d)" % d
    else:
        raise TypeError, "Array must have 2 or 3 dimensions (%d)" % nd
    if d > 1:
        x = numpy.swapaxes(numpy.swapaxes(x, 1, 2), 0, 2)
    pil = Image.fromstring(mode, (w,h), x.tostring())
    if arr.dtype.char == '?':
        pil = pil.point(lambda i: i>0, '1')
    return pil
#
#
# =====================================================================
#
#   addraw(arr, what, *args, **kw)
#
# =====================================================================
class adDraw:
    """
    Proxy of the PIL module ImageDraw.
    """
    FONT_PATH = ['', '/usr/share/fonts/truetype/msttcorefonts/']
    #
    def __init__(self, image, rgb=False):
        """
        Creates a context for drawing in image image.
        """
        import ImageDraw
        self.pil = array2pil(image)
        if rgb: self.pil = self.pil.convert('RGB')
        self.draw = ImageDraw.Draw(self.pil)

    def get_image(self):
        """
        Returns the image with the drawings.
        """
        return pil2array(self.pil)

    def arc(self, xy, start, end, **options):
        """
        Draws an arc (a portion of a circle outline) between the start
        and end angles, inside the given bounding box.

        The 'outline' option gives the colour to use for the arc.
        """
        return self.draw.arc(xy, start, end, **options)

    def bitmap(self, xy, bitmap, **options):
        """
        Draws a bitmap (mask) at the given position, using the current
        fill colour. The bitmap should be a valid transparency mask
        (mode "1") or matte (mode "L" or "RGBA").

        To paste pixel data into an image, use the paste method on the
        image itself.
        """
        return self.draw.bitmap(xy, bitmap, **options)


    def chord(self, xy, start, end, **options):
        """
        Same as arc, but connects the end points with a straight line.

        The 'outline' option gives the colour to use for the chord outline.

        The 'fill' option gives the colour to use for the chord interior.
        """
        return self.draw.chord(xy, start, end, **options)


    def ellipse(self, xy, **options):
        """
        Draws an ellipse inside the given bounding box.

        The 'outline' option gives the colour to use for the ellipse outline.

        The 'fill' option gives the colour to use for the ellipse interior.
        """
        return self.draw.ellipse(xy, **options)


    def line(self, xy, **options):
        """
        Draws a line between the coordinates in the xy list.
        The coordinate list can be any sequence object containing either
        2-tuples [ (x, y), ... ] or numeric values [ x, y, ... ]. It should
        contain at least two coordinates.

        The 'fill' option gives the colour to use for the line.

        The 'width' option gives the line width, in pixels. Note that line
        joins are not handled well, so wide polylines will not look good.
        """
        return self.draw.line(xy, **options)


    def pieslice(self, xy, start, end, **options):
        """
        Same as arc, but also draws straight lines between the end points
        and the center of the bounding box.

        The 'outline' option gives the colour to use for the pieslice outline.

        The 'fill' option gives the colour to use for the pieslice interior.
        """
        return self.draw.pieslice(xy, start, end, **options)


    def point(self, xy, **options):
        """
        Draws points (individual pixels) at the given coordinates.
        The coordinate list can be any sequence object containing either
        2-tuples [ (x, y), ... ] or numeric values [ x, y, ... ].

        The 'fill' option gives the colour to use for the points.
        """
        return self.draw.point(xy, **options)


    def polygon(self, xy, **options):
        """
        Draws a polygon.
        The polygon outline consists of straight lines between the given
        coordinates, plus a straight line between the last and the first
        coordinate.
        The coordinate list can be any sequence object containing either
        2-tuples [ (x, y), ... ] or numeric values [ x, y, ... ]. It should
        contain at least three coordinates.

        The 'outline' option gives the colour to use for the polygon outline.

        The 'fill' option gives the colour to use for the polygon interior.
        """
        return self.draw.polygon(xy, **options)


    def rectangle(self, box, **options):
        """
        Draws a rectangle.
        The box can be any sequence object containing either 2-tuples
        [ (x, y), (x, y) ] or numeric values [ x, y, x, y ]. It should contain
        two coordinates.
        Note that the second coordinate pair defines a point just outside the
        rectangle, also when the rectangle is not filled.

        The 'outline' option gives the colour to use for the rectangle outline.

        The 'fill' option gives the colour to use for the rectangle interior.
        """
        return self.draw.rectangle(box, **options)


    def text(self, position, string, **options):
        """
        Draws the string at the given position. The position gives the upper
        left corner of the text.

        The 'font' option is used to specify which font to use. It should be the
        arguments of the ImageFont.truetype function: (font_file, font_size).
        Useful truetype fonts: arial.ttf, comic.ttf, cour.ttf, trebuc.ttf,
        tahoma.ttf, times.ttf etc (see the windows/fonts directory).

        The 'fill' option gives the colour to use for the text.
        """
        import ImageFont
        if options.has_key('font'):
            ffile = options['font'][0]
            fsize = options['font'][1]
            del options['font']
            for path in self.FONT_PATH:
                try:
                    options['font'] = ImageFont.truetype(path + ffile, fsize)
                    break
                except:
                    pass
        return self.draw.text(position, string, **options)


    def textsize(self, string, **options):
        """
        Return the size of the given string, in pixels.

        The 'font' option is used to specify which font to use.
        See the 'text' method of this class.
        """
        import ImageFont
        if options.has_key('font'):
            ffile = options['font'][0]
            fsize = options['font'][1]
            del options['font']
            for path in self.FONT_PATH:
                try:
                    options['font'] = ImageFont.truetype(path + ffile, fsize)
                    break
                except:
                    pass
        return self.draw.textsize(string, **options)
