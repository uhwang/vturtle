'''
    Initial version by ChatGPT & Gemini
    Edited by Uisang Hwang
'''
import math
from pathlib import Path
import libvgl as vgl

# Define color constants that might be missing in libvgl if not already there
# For demonstration, I'll assume vgl.BLACK, vgl.RED, etc. are available.
# If not, you'd define them like:
# class color:
#     BLACK = (0.0, 0.0, 0.0) # RGB
#     RED = (1.0, 0.0, 0.0)
#     BLUE = (0.0, 0.0, 1.0)
#     GREEN = (0.0, 1.0, 0.0)
#     WHITE = (1.0, 1.0, 1.0)
# Assuming you have a 'vgl' module with a 'Color' class like this:
# class Color:
#     def __init__(self, r, g, b):
#         self.r = r
#         self.g = g
#         self.b = b
#
#     def __repr__(self):
#         return fvgl.Color({self.r}, {self.g}, {self.b})
#
# If you don't have this, the output will contain an error unless 'vgl' and 'Color' are defined.
# For the purpose of providing the *string representation* of what you want,
# we'll represent it as strings in the dictionary first, and you can convert to actual objects
# if you implement the vgl.Color class.

turtle_colors = {
    # Basic colors
    "black": vgl.Color(0, 0, 0),
    "white": vgl.Color(255, 255, 255),
    "gray": vgl.Color(128, 128, 128),
    "darkgray": vgl.Color(169, 169, 169),
    "lightgray": vgl.Color(211, 211, 211),
    "silver": vgl.Color(192, 192, 192),
    "dimgray": vgl.Color(105, 105, 105),

    # Reds
    "red": vgl.Color(255, 0, 0),
    "darkred": vgl.Color(139, 0, 0),
    "lightcoral": vgl.Color(240, 128, 128),
    "indianred": vgl.Color(205, 92, 92),
    "crimson": vgl.Color(220, 20, 60),
    "firebrick": vgl.Color(178, 34, 34),
    "maroon": vgl.Color(128, 0, 0),
    "salmon": vgl.Color(250, 128, 114),
    "darksalmon": vgl.Color(233, 150, 122),
    "lightsalmon": vgl.Color(255, 160, 122),
    "orangered": vgl.Color(255, 69, 0),
    "tomato": vgl.Color(255, 99, 71),

    # Pinks
    "pink": vgl.Color(255, 192, 203),
    "deeppink": vgl.Color(255, 20, 147),
    "hotpink": vgl.Color(255, 105, 180),
    "lightpink": vgl.Color(255, 182, 193),
    "palevioletred": vgl.Color(219, 112, 147),
    "mediumvioletred": vgl.Color(199, 21, 133),

    # Oranges
    "orange": vgl.Color(255, 165, 0),
    "darkorange": vgl.Color(255, 140, 0),
    "coral": vgl.Color(255, 127, 80),

    # Yellows
    "yellow": vgl.Color(255, 255, 0),
    "gold": vgl.Color(255, 215, 0),
    "lightyellow": vgl.Color(255, 255, 224),
    "lemonchiffon": vgl.Color(255, 250, 205),
    "palegoldenrod": vgl.Color(238, 232, 170),
    "khaki": vgl.Color(240, 230, 140),
    "darkkhaki": vgl.Color(189, 183, 107),
    "goldenrod": vgl.Color(218, 165, 32),
    "darkgoldenrod": vgl.Color(184, 134, 11),

    # Browns
    "brown": vgl.Color(165, 42, 42),
    "saddlebrown": vgl.Color(139, 69, 19),
    "sienna": vgl.Color(160, 82, 45),
    "chocolate": vgl.Color(210, 105, 30),
    "peru": vgl.Color(205, 133, 63),
    "tan": vgl.Color(210, 180, 140),
    "burlywood": vgl.Color(222, 184, 135),
    "wheat": vgl.Color(245, 222, 179),
    "sandybrown": vgl.Color(244, 164, 96),

    # Greens
    "green": vgl.Color(0, 128, 0),
    "darkgreen": vgl.Color(0, 100, 0),
    "lightgreen": vgl.Color(144, 238, 144),
    "limegreen": vgl.Color(50, 205, 50),
    "forestgreen": vgl.Color(34, 139, 34),
    "seagreen": vgl.Color(46, 139, 87),
    "mediumseagreen": vgl.Color(60, 179, 113),
    "darkseagreen": vgl.Color(143, 188, 143),
    "palegreen": vgl.Color(152, 251, 152),
    "springgreen": vgl.Color(0, 255, 127),
    "lightspringgreen": vgl.Color(0, 250, 154),
    "mediumspringgreen": vgl.Color(0, 250, 154), # Alias
    "chartreuse": vgl.Color(127, 255, 0),
    "lawngreen": vgl.Color(124, 252, 0),
    "olivedrab": vgl.Color(107, 142, 35),
    "darkolivegreen": vgl.Color(85, 107, 47),
    "yellowgreen": vgl.Color(154, 205, 50),
    "honeydew": vgl.Color(240, 255, 240),
    "mintcream": vgl.Color(245, 255, 250),

    # Cyans/Teals
    "cyan": vgl.Color(0, 255, 255),
    "aqua": vgl.Color(0, 255, 255), # Alias for cyan
    "lightcyan": vgl.Color(224, 255, 255),
    "paleturquoise": vgl.Color(175, 238, 238),
    "turquoise": vgl.Color(64, 224, 208),
    "mediumturquoise": vgl.Color(72, 209, 204),
    "darkturquoise": vgl.Color(0, 206, 209),
    "aquamarine": vgl.Color(127, 255, 212),
    "mediumaquamarine": vgl.Color(102, 205, 170),
    "teal": vgl.Color(0, 128, 128),
    "darkslategray": vgl.Color(47, 79, 79),
    "lightslategray": vgl.Color(119, 136, 153),
    "slategray": vgl.Color(112, 128, 144),

    # Blues
    "blue": vgl.Color(0, 0, 255),
    "darkblue": vgl.Color(0, 0, 139),
    "mediumblue": vgl.Color(0, 0, 205),
    "navy": vgl.Color(0, 0, 128),
    "royalblue": vgl.Color(65, 105, 225),
    "cornflowerblue": vgl.Color(100, 149, 237),
    "steelblue": vgl.Color(70, 130, 180),
    "lightsteelblue": vgl.Color(176, 196, 222),
    "dodgerblue": vgl.Color(30, 144, 255),
    "deepskyblue": vgl.Color(0, 191, 255),
    "skyblue": vgl.Color(135, 206, 235),
    "lightskyblue": vgl.Color(135, 206, 250),
    "powderblue": vgl.Color(176, 224, 230),
    "cadetblue": vgl.Color(95, 158, 160),
    "aliceblue": vgl.Color(240, 248, 255),
    "ghostwhite": vgl.Color(248, 248, 255),
    "lavender": vgl.Color(230, 230, 250),
    "midnightblue": vgl.Color(25, 25, 112),

    # Purples
    "purple": vgl.Color(128, 0, 128),
    "darkmagenta": vgl.Color(139, 0, 139),
    "mediumorchid": vgl.Color(186, 85, 211),
    "darkorchid": vgl.Color(153, 50, 204),
    "blueviolet": vgl.Color(138, 43, 226),
    "darkviolet": vgl.Color(148, 0, 211),
    "mediumpurple": vgl.Color(147, 112, 219),
    "rebeccapurple": vgl.Color(102, 51, 153),
    "thistle": vgl.Color(216, 191, 216),
    "plum": vgl.Color(221, 160, 221),
    "violet": vgl.Color(238, 130, 238),
    "orchid": vgl.Color(218, 112, 214),

    # Other common colors (Greys and others)
    "whitesmoke": vgl.Color(245, 245, 245),
    "gainsboro": vgl.Color(220, 220, 220),
    "antiquewhite": vgl.Color(250, 235, 215),
    "bisque": vgl.Color(255, 228, 196),
    "blanchedalmond": vgl.Color(255, 235, 205),
    "floralwhite": vgl.Color(255, 250, 240),
    "oldlace": vgl.Color(253, 245, 230),
    "seashell": vgl.Color(255, 245, 238),
    "snow": vgl.Color(255, 250, 250),
    "azure": vgl.Color(240, 255, 255),
    "mistyrose": vgl.Color(255, 228, 225),
    "lavenderblush": vgl.Color(255, 240, 245),
    "linen": vgl.Color(250, 240, 230),
    "peachpuff": vgl.Color(255, 218, 185),
    "papayawhip": vgl.Color(255, 239, 213),
    "mocassin": vgl.Color(255, 228, 181),
    "navajowhite": vgl.Color(255, 222, 173),
    "cornsilk": vgl.Color(255, 248, 220),
    "ivory": vgl.Color(255, 255, 240),
    "lemonchiffon": vgl.Color(255, 250, 205), # Duplicated in previous list, keep for consistency
    "beige": vgl.Color(245, 245, 220),
    "lightgoldenrodyellow": vgl.Color(250, 250, 210),
    "lightyellow": vgl.Color(255, 255, 224), # Duplicated
    "olivedrab": vgl.Color(107, 142, 35), # Duplicated
    "darkolivegreen": vgl.Color(85, 107, 47), # Duplicated
    "mediumaquamarine": vgl.Color(102, 205, 170), # Duplicated
    "darkseagreen": vgl.Color(143, 188, 143), # Duplicated
    "mediumseagreen": vgl.Color(60, 179, 113), # Duplicated
    "lightseagreen": vgl.Color(32, 178, 170),
    "cadetblue": vgl.Color(95, 158, 160), # Duplicated
    "darkcyan": vgl.Color(0, 139, 139),
    "deepskyblue": vgl.Color(0, 191, 255), # Duplicated
    "dodgerblue": vgl.Color(30, 144, 255), # Duplicated
    "royalblue": vgl.Color(65, 105, 225), # Duplicated
    "mediumslateblue": vgl.Color(123, 104, 238),
    "slateblue": vgl.Color(106, 90, 205),
    "darkslateblue": vgl.Color(72, 61, 139),
    "mediumpurple": vgl.Color(147, 112, 219), # Duplicated
    "darkorchid": vgl.Color(153, 50, 204), # Duplicated
    "darkviolet": vgl.Color(148, 0, 211), # Duplicated
    "darkblue": vgl.Color(0, 0, 139), # Duplicated
    "darkred": vgl.Color(139, 0, 0), # Duplicated
    "darkgreen": vgl.Color(0, 100, 0), # Duplicated
    "darkorange": vgl.Color(255, 140, 0), # Duplicated
    "darkgoldenrod": vgl.Color(184, 134, 11), # Duplicated
    "darkkhaki": vgl.Color(189, 183, 107), # Duplicated
    "darkturquoise": vgl.Color(0, 206, 209), # Duplicated
    "darkslategray": vgl.Color(47, 79, 79), # Duplicated
    "darkgrey": vgl.Color(169, 169, 169), # Alias for darkgray
    "lightgrey": vgl.Color(211, 211, 211) # Alias for lightgray
}

class Turtle:
    """
    A simple Turtle graphics implementation using the libvgl library.
    """
    _device_called = False
    _device_dpi = 300
    _device_pdir = 'p'
    
    def __init__(self, 
            fname="turtle.jpg",
            nrows=1,
            ncols=1,
            sx   = 0,
            sy   = 0,
            wid  = 2,
            hgt  = 2,
            xmin = -200,
            xmax =  200,
            ymin = -200,
            ymax =  200):
        """
        Initializes the Turtle.

        Args:
            device: An instance of a libvgl Device (e.g., vgl.DeviceIMG, vgl.DevicePDF).
            frame: An instance of a libvgl Frame created by FrameManager.
        """
        self._fname = fname
        self._dev = None
        self._fmm = vgl.FrameManager()
        
        self._x = 0.0
        self._y = 0.0
        self._heading = 0.0  # 0 degrees is East (right)
        self._pendown = True
        self._pencolor = vgl.BLACK
        self._pensize = 0.001  # Default line thickness
        self._fillcolor = None
        self._filling = False
        self._fill_coords = [] # Stores coordinates for begin_fill/end_fill

        # Initialize the graphics context (if necessary for libvgl)
        # For libvgl, we generally draw directly to the device.
        self._nrows = nrows
        self._ncols = ncols
        self._sx = sx
        self._sy = sy
        self._wid = wid
        self._hgt = hgt
        
        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax
        
        self._frames = None
        self._frm_horz_padding = 0.01
        self._frm_vert_padding = 0.01
        self._current_index = 0
        
        self._create_grid(nrows, ncols)
        #self.device(fname)
    
    def _create_grid(self, nrows, ncols):
        self._frames = []
            
        for i in range(nrows):
            for j in range(ncols):
                xx = self._sx+j * self._wid + j*self._frm_horz_padding
                yy = self._sy+i * self._hgt + i*self._frm_vert_padding
                frm = self._fmm.create(xx, yy, self._wid, self._hgt,
                                      vgl.Data(self._xmin, self._xmax, self._ymin, self._ymax))
                self._frames.append(frm)
       
    def subplot(self, *args):
        """Accepts either subplot(321) or subplot(3,2,1)"""
        if len(args) == 1:
            code = str(args[0])
            if len(code) != 3:
                raise ValueError("subplot code must be a 3-digit integer (e.g., 321)")
            rows, cols, index = int(code[0]), int(code[1]), int(code[2])
        elif len(args) == 3:
            rows, cols, index = args
        else:
            raise ValueError("subplot requires either 1 integer (321) or 3 arguments (3,2,1)")

        if rows != self._nrows or cols != self._ncols:
            self._create_grid(rows, cols)
            self.device()
            self._nrows = rows
            self._ncols = cols
            index = 1

        if not (1 <= index <= rows * cols):
            raise ValueError(f"Subplot index must be in 1..{rows * cols}")

        self._current_index = index - 1
        self._dev.set_device(self._frames[self._current_index])
        self.reset()
        return self
        
    sp = subplot
    
    def device(self, fname=None, dpi=300, pdir="p"):
   
        # initial call
        pdir_ = pdir.lower()
        #
        if not self._device_called:
            self._device_called = True
            self._device_dpi = dpi
            self._device_pdir = pdir_
        else:
            dpi  = self._device_dpi
            pdir = self._device_pdir
            
        if fname is not None:
            self._fname = fname

        p = Path(self._fname).suffix.lower()
        if self._dev:
            self._dev.close()
       
        if "jpg" in p or "png" in p:
            self._dev = vgl.DeviceIMG(self._fname, self._fmm.get_gbbox(), dpi)
        elif "wmf" in p:
            self._dev = vgl.DeviceWMF(self._fname, self._fmm.get_gbbox())
        elif "emf" in p:
            self._dev = vgl.DeviceEMF(self._fname, self._fmm.get_gbbox())
        elif "svg" in p:
            self._dev = vgl.DeviceSVG(self._fname, self._fmm.get_gbbox(), dpi)
        elif "pdf" in p:
            self._dev = vgl.DevicePDF(self._fname, self._fmm.get_gbbox(), pdir=pdir)
        elif "pptx" in p:
            self._dev = vgl.DevicePPT(self._fname, self._fmm.get_gbbox())
        else:
            print("Error: invalid device")
            return

    def _degrees_to_radians(self, degrees):
        return math.radians(degrees)

    def _move_to(self, new_x, new_y):
        """Internal method to move the turtle and draw if pen is down."""
        if self._pendown:
            self._dev.line(self._x, self._y, new_x, new_y,
                          lcol=self._pencolor, lthk=self._pensize)
        self._x = new_x
        self._y = new_y
        if self._filling:
            self._fill_coords.append((new_x, new_y))

    # symid : string ex: 
    # circle'        : 'o'
    # triangle_left' : '<'
    # triangle_right': '>'
    # triangle_down' : 'v'
    # triangle_up'   : '^'
    # diamond'       : 'D'
    # square'        : 's'
    # pentagon'      : 'p'
    # trigram'       : '*3'
    # quadgram'      : '*4'
    # pentagram'     : '*5'
    # hexgram'       : '*6'
    # plus'          : '+'
    # cross'         : 'x'
    def symbol(self, sid='o', size=0.02, deg=0):
        self._dev.symbol(self._x, self._y, sid, size, deg, 
                         self._pencolor, 
                         self._pensize, 
                         lpat=vgl.linepat._PAT_SOLID, 
                         fcol=self._fillcolor)
    sym = symbol
    
    def forward(self, distance):
        """Move the turtle forward by the specified distance."""
        angle_rad = self._degrees_to_radians(self._heading)
        new_x = self._x + distance * math.cos(angle_rad)
        new_y = self._y + distance * math.sin(angle_rad)
        self._move_to(new_x, new_y)

    fd = forward
    
    def backward(self, distance):
        """Move the turtle backward by the specified distance."""
        self.forward(-distance)
    
    bk = backward
    
    def left(self, angle):
        """Turn turtle left by angle units."""
        self._heading = (self._heading + angle) % 360
    
    lt = left
    
    def right(self, angle):
        """Turn turtle right by angle units."""
        self._heading = (self._heading - angle) % 360
    rt = right
    
    def penup(self):
        """Pull the pen up – no drawing when moving."""
        self._pendown = False
    
    pu = penup # Alias

    def pendown(self):
        """Put the pen down – drawing when moving."""
        self._pendown = True
    
    pd = pendown # Alias

    def pencolor(self, *args):
        """
        Return or set the pen color.
        Usage:
            pencolor() -> current pen color (RGB tuple or None if not set)
            pencolor(color_name_or_rgb_tuple)
        """
        if not args:
            return self._pencolor
        if isinstance(args[0], tuple) and len(args[0]) == 3:
            self._pencolor = vgl.Color(args[0][0],args[0][1],args[0][2])
        elif isinstance(args[0], str):
            # Assuming libvgl.color has predefined colors by name
            # Or you'd map string names to RGB tuples here
            try:
                #self._pencolor = getattr(color, args[0].upper())
                #self._pencolor = vgl.default_color[args[0].lower()]
                self._pencolor = turtle_colors[args[0].lower()]
            except AttributeError:
                print(f"Warning: Color '{args[0]}' not found. Using current color.")
                self._pencolor = vgl.default_color['w']
        elif isinstance(args[0], vgl.Color):
            self._pencolor = args[0]
        else:
            print("Invalid color argument. Please use an RGB tuple or a recognized color name.")
    pen = pencolor # Alias

    def pensize(self, size=None):
        """
        Return or set the pen size (line thickness).
        Usage:
            pensize() -> current pen size
            pensize(size)
        """
        if size is None:
            return self._pensize
        self._pensize = float(size)
        
    def width(self, value=None):
        if value is None:
            return self._pensize
        else:
            self._pensize = float(value)
            
    def pos(self):
        """Return the turtle's current position (x, y)."""
        return self._x, self._y
    position = pos # Alias

    def reset(self):
        """Delete the turtle's drawings and reset its state."""
        self._x = 0.0
        self._y = 0.0
        self._heading = 0.0
        self._pendown = True
        self._pencolor = vgl.BLACK
        self._pensize = 0.001
        self._fillcolor = None
        self._filling = False
        self._fill_coords = []
        # For libvgl, 'reset' would typically mean clearing the frame or starting a new drawing.
        # Since libvgl doesn't have a direct "clear" method for a device's current drawing,
        # 'reset' here will only reset the turtle's state. To clear the drawing, you'd
        # likely need to create a new device or frame.
        # If your device had a `clear()` method, you'd call it here:
        # self._dev.clear()

    def setpos(self, x, y=None):
        """
        Move turtle to an absolute position.
        If the pen is down, draw a line.
        Usage:
            setpos(x, y)
            setpos((x, y))
        """
        if isinstance(x, (tuple, list)):
            target_x, target_y = x[0], x[1]
        else:
            target_x, target_y = x, y
        self._move_to(target_x, target_y)
    goto = setpos # Alias

    def teleport(self, x, y=None):
        """
        Move turtle to an absolute position without drawing.
        Usage:
            teleport(x, y)
            teleport((x, y))
        """
        was_pendown = self._pendown
        self.penup()
        self.setpos(x, y)
        if was_pendown:
            self.pendown()

    def towards(self, x, y=None):
        """
        Return the angle of the line from the turtle's position to (x, y).
        Usage:
            towards(x, y)
            towards((x, y))
        """
        if isinstance(x, (tuple, list)):
            target_x, target_y = x[0], x[1]
        else:
            target_x, target_y = x, y

        dx = target_x - self._x
        dy = target_y - self._y
        angle_rad = math.atan2(dy, dx)
        return math.degrees(angle_rad) % 360

    def setx(self, x):
        """Set the turtle’s first coordinate to x."""
        self.setpos(x, self._y)

    def sety(self, y):
        """Set the turtle’s second coordinate to y."""
        self.setpos(self._x, y)

    def circle(self, radius, extent=360, steps=None):
        """
        Draw a circle with the given radius.
        The center is radius units left of the turtle (if radius > 0)
        or radius units right (if radius < 0).
        """
        # For simplicity, we'll draw a circle using the libvgl.circle method.
        # This means the Turtle's position will be the center for libvgl.
        # This differs from standard Turtle behavior where the circle is drawn
        # relative to the turtle's position and orientation.
        # To strictly adhere to standard Turtle circle:
        # 1. Calculate center based on current position and heading.
        # 2. Move to a starting point on the circle.
        # 3. Draw many small line segments or use a specialized arc function if available.

        # Given libvgl's circle, we'll implement it as:
        # current_x, current_y are turtle's position.
        # The center of the circle will be the turtle's position.
        # For standard Turtle, the circle center is NOT the turtle's current position.
        # It's at (turtle.x, turtle.y - radius) if facing East.
        # Let's try to simulate the standard turtle behavior more closely.

        # Calculate the center of the circle relative to the turtle's current position
        # and heading. If radius > 0, the center is "left" of the turtle.
        # A 0-degree heading means facing right (East).
        # To find the center: rotate -90 degrees from current heading, then move radius distance.
        center_angle_rad = self._degrees_to_radians(self._heading + 90 if radius > 0 else self._heading - 90)
        center_x = self._x + abs(radius) * math.cos(center_angle_rad)
        center_y = self._y + abs(radius) * math.sin(center_angle_rad)

        # libvgl's circle draws a full circle from center and radius.
        # It doesn't support 'extent' or 'steps' directly for drawing segments.
        # To support 'extent', we'd need to draw a polyline of many segments.
        # For now, we'll use libvgl's circle for a full circle, and for extent,
        # we'd need a more complex polyline implementation.

        if extent == 360:
            self._dev.circle(center_x, center_y, abs(radius),
                            lcol=self._pencolor, lthk=self._pensize,
                            fcol=self._fillcolor if self._filling else None)
        else:
            print("Warning: `circle` with `extent` is not fully implemented with libvgl's native circle. Drawing a full circle for now.")
            self._dev.circle(center_x, center_y, abs(radius),
                            lcol=self._pencolor, lthk=self._pensize,
                            fcol=self._fillcolor if self._filling else None)
            # To implement extent:
            # 1. Calculate start and end points on the arc.
            # 2. Generate intermediate points.
            # 3. Use self._dev.polyline() to draw the arc.

    def heading(self):
        """Return the turtle's current heading."""
        return self._heading

    def setheading(self, angle):
        """Set the turtle’s heading to angle."""
        self._heading = angle % 360

    seth = setheading
    
    def fillcolor(self, *args):
        """
        Return or set the fill color.
        Usage:
            fillcolor() -> current fill color (RGB tuple or None)
            fillcolor(color_name_or_rgb_tuple)
        """
        if not args:
            return self._fillcolor
        if isinstance(args[0], tuple) and len(args[0]) == 3:
            self._fillcolor = args[0]
        elif isinstance(args[0], str):
            try:
                #self._fillcolor = getattr(color, args[0].upper())
                self._fillcolor = turtle_colors[args[0].lower()]
            except AttributeError:
                print(f"Warning: Color '{args[0]}' not found. Using current fill color.")
        elif isinstance(args[0], vgl.Color):
            self._fillcolor = args[0]
        else:
            print("Invalid color argument. Please use an RGB tuple or a recognized color name.")

    def begin_fill(self):
        """Call this just before drawing the shape to be filled."""
        self._filling = True
        self._fill_coords = [(self._x, self._y)] # Start with current position

    def end_fill(self):
        """Fill the shape drawn since the last call to begin_fill."""
        if self._filling and self._fill_coords and self._fillcolor:
            # Add the current position to close the shape if it's not already closed
            if self._fill_coords[-1] != (self._x, self._y):
                self._fill_coords.append((self._x, self._y))

            # Ensure the shape is explicitly closed for polygon filling
            if self._fill_coords[0] != self._fill_coords[-1]:
                self._fill_coords.append(self._fill_coords[0])

            x_coords = [p[0] for p in self._fill_coords]
            y_coords = [p[1] for p in self._fill_coords]
            self._dev.polygon(x_coords, y_coords,
                             lcol=self._pencolor, lthk=self._pensize,
                             fcol=self._fillcolor)
        self._filling = False
        self._fill_coords = []

    def screen_size(self, xmin, xmax, ymin, ymax):
        """
        Sets the coordinate system of the drawing area.
        This reconfigures the frame's data range.
        Note: This effectively redefines the 'world' coordinates for the turtle.
        """
        # Create a new Data object for the frame's new plot area
        new_data_range = vgl.Data(xmin, xmax, ymin, ymax)
        # Assuming there's a way to update the frame's data range directly
        # or that creating a new frame is the intended way.
        # Based on the FrameManager setup, it seems the data range is set at creation.
        # If we need to change it, we'd typically need to recreate the frame or modify
        # its internal data range. Let's assume `frm` has a method to update its data range.
        # If not, you might need to recreate the frame and pass it to the turtle.
        self.frm.set_data_range(new_data_range) # This method might need to be added to libvgl's Frame class.
                                               # If not, the most robust way to change screen size
                                               # is to create a new frame and possibly a new device.
    def close(self):
        if self._dev: 
            self._dev.close()


# --- GLOBAL INSTANCE AND EXPOSED FUNCTIONS (NEW PART) ---

# Create a default Turtle instance. This is what 'forward()' etc. will operate on.
# You can customize the default output filename and canvas size here.
# Make sure to set a default filename like "turtle_output.jpg" or "drawing.png"
# and appropriate xmin, xmax, ymin, ymax values.
_default_turtle = Turtle("turtle.jpg")

# Expose the methods of the default turtle instance as global functions.
# This makes it behave like the standard turtle module.
backward    = _default_turtle.backward
bk          = _default_turtle.bk
device      = _default_turtle.device
forward     = _default_turtle.forward
fd          = _default_turtle.fd
goto        = _default_turtle.goto
left        = _default_turtle.left
lt          = _default_turtle.lt
right       = _default_turtle.right
rt          = _default_turtle.rt
penup       = _default_turtle.penup
pu          = _default_turtle.pu
up          = _default_turtle.penup
pendown     = _default_turtle.pendown
pd          = _default_turtle.pd
down        = _default_turtle.pendown
pencolor    = _default_turtle.pencolor
pen         = _default_turtle.pen
pensize     = _default_turtle.pensize
width       = _default_turtle.width
pos         = _default_turtle.pos
position    = _default_turtle.position
reset       = _default_turtle.reset
setpos      = _default_turtle.setpos
symbol      = _default_turtle.symbol
sym         = _default_turtle.sym
teleport    = _default_turtle.teleport
towards     = _default_turtle.towards
setx        = _default_turtle.setx
sety        = _default_turtle.sety
circle      = _default_turtle.circle
heading     = _default_turtle.heading
setheading  = _default_turtle.setheading
seth        = _default_turtle.seth
fillcolor   = _default_turtle.fillcolor
begin_fill  = _default_turtle.begin_fill
end_fill    = _default_turtle.end_fill
screen_size = _default_turtle.screen_size
subplot     = _default_turtle.subplot

# Also expose the close method
close = _default_turtle.close

# Optional: Add setup for onexit to ensure the device is closed if script exits cleanly
import atexit
atexit.register(_default_turtle.close)


'''            
# --- Example Usage ---
if __name__ == "__main__":
    t=Turtle("turtle.jpg")

    t.pencolor('r')
    t.pensize(0.006)
    for i in range(5):
        t.right(144)
        t.forward(100)

    vgl.draw_grid(dev_img)
    vgl.draw_axis(dev_img)
'''    
