'''
    Initial version by ChatGPT & Gemini
    Edited by Uisang Hwang
'''
import re
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

_default_dpi = 300
_default_pdir = "p"

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
        #self._fillcolor = vgl.WHITE
        self._fillcolor = None
        self._filling = False
        self._fill_coords = [] # Stores coordinates for begin_fill/end_fill
        self._poly = False
        self._poly_coords = []

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
    
    def devptr(self):
        return self._dev if self._dev else None
    
    def device(self, fname=None, dpi=None, pdir=None):
   
        # initial call
        #pdir_ = pdir.lower()
        #
        #if not self._device_called:
        #    self._device_called = True
        #    self._device_dpi = dpi
        #    self._device_pdir = pdir_
        #else:
        #    dpi  = self._device_dpi
        #    pdir = self._device_pdir
        dpi_ = _default_dpi if dpi is None else dpi
        pdir_ = _default_pdir if pdir is None else pdir
        
        if fname is not None:
            self._fname = fname

        p = Path(self._fname).suffix.lower()
        if self._dev:
            self._dev.close()
       
        if "jpg" in p or "png" in p:
            self._dev = vgl.DeviceIMG(self._fname, self._fmm.get_gbbox(), dpi_)
        elif "wmf" in p:
            self._dev = vgl.DeviceWMF(self._fname, self._fmm.get_gbbox())
        elif "emf" in p:
            self._dev = vgl.DeviceEMF(self._fname, self._fmm.get_gbbox())
        elif "svg" in p:
            self._dev = vgl.DeviceSVG(self._fname, self._fmm.get_gbbox(), dpi_)
        elif "pdf" in p:
            self._dev = vgl.DevicePDF(self._fname, self._fmm.get_gbbox(), pdir=pdir_)
        elif "pptx" in p:
            self._dev = vgl.DevicePPT(self._fname, self._fmm.get_gbbox())
        else:
            print("Error: invalid device")
            return
            
        self._dev.set_device(self._frames[0])
        return self._dev

    def _degrees_to_radians(self, degrees):
        return math.radians(degrees)

    def _move_to(self, new_x, new_y):
        """Internal method to move the turtle and draw if pen is down."""
        if self._pendown and not self._filling and not self._poly:
            self._dev.line(self._x, self._y, new_x, new_y,
                          lcol=self._pencolor, lthk=self._pensize)
        self._x = new_x
        self._y = new_y
        
        if self._filling:
            self._fill_coords.append((new_x, new_y))

        if self._poly:
            self._poly_coords.append((new_x, new_y))

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
    def get_color(self, c):
        if isinstance(c, str):
            _c = turtle_colors.get(c, None)
            if _c is not None:
                return _c
            else:
                _c = vgl.default_color.get(c.lower(), None)
                if _c is not None:
                    return _c
                elif re.match(r'^[\?]', c):
                    return None
                else:
                    print("Error: invalid color. Back color returns")
                    return vgl.BLACK
        elif isinstance(c, vgl.Color):
            return c
        elif isinstance(c, tuple):
            return vgl.Color(int(c[0]),int(c[1]),int(c[2]))
        else:
            print("Error: invalid color. Back color returns")
            return vgl.BLACK
            
    def symbol(self, sid='o', size=0.02, deg=0, lcol=None, lthk=None, fcol=None):
        _p_col = self._pencolor
        _p_thk = self._pensize
        _f_col = self._fillcolor
        _l_pat = vgl.linepat._PAT_SOLID
        
        if lcol is not None:
            #_p_col = self.get_color(lcol)
            _p_col = lcol
            
        if fcol is not None:
            #_f_col = self.get_color(fcol)
            _f_col = fcol
            
        if lthk is not None:
            _p_thk = float(lthk)
        
        self._dev.symbol(self._x, self._y, sid, size, deg, 
                         _p_col, 
                         _p_thk, 
                         _l_pat, 
                         _f_col)
    sym = symbol
    
    def _new_pos(self, distance):
        """Move the turtle forward by the specified distance."""
        angle_rad = self._degrees_to_radians(self._heading)
        new_x = self._x + distance * math.cos(angle_rad)
        new_y = self._y + distance * math.sin(angle_rad)

        return new_x, new_y
        
    def forward(self, distance):
        new_x, new_y = self._new_pos(distance)
        self._move_to(new_x, new_y)

    fd = forward
    
    def _arrow(self, distance, style, size=0.02, lcol=None, lthk=None, fcol=None, move=False):
        cur_x, cur_y = self._x, self._y
        new_x, new_y = self._new_pos(distance)
        
        a_lcol = self._pencolor
        a_lthk = self._pensize
        a_fcol = self._fillcolor
        a_lpat = vgl.linepat._PAT_SOLID
        
        if lcol is not None:
            a_lcol = lcol
            
        if lthk is not None:
            a_lthk = lthk
            
        if fcol is not None:
            a_fcol = fcol
            
        vgl.drawarrow.draw_arrow(self._dev, 
                       cur_x, cur_y, new_x, new_y, 
                       style, size, a_lcol, a_lthk, a_lpat, a_fcol, 
                       color_table=None)
                
        if move:
            self._x = new_x
            self._y = new_y
                        
    def arrow(self, distance, style, size=0.02, lcol=None, lthk=None, fcol=None):
        self._arrow(distance, style, size, lcol, lthk, fcol, False)
        
    def arrowf(self, distance, style, size=0.02, lcol=None, lthk=None, fcol=None):
        self._arrow(distance, style, size, lcol, lthk, fcol, True)
        
    ar = arrow
    arf= arrowf
    
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
                self._pencolor = vgl.colordict.turtle_colors[args[0].lower()]
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

    def circle(self, radius, cx=None, cy=None, extent=360, steps=None):
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
        if cx is not None and cy is not None:
            center_x, center_y = cx, cy
        else:
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
                self._fillcolor = vgl.colordict.turtle_colors[args[0].lower()]
            except AttributeError:
                print(f"Warning: Color '{args[0]}' not found. Using current fill color.")
        elif isinstance(args[0], vgl.Color):
            self._fillcolor = args[0]
        else:
            print("Invalid color argument. Please use an RGB tuple or a recognized color name.")

    def begin_poly(self):
        self._poly = True
        self._poly_coords = [(self._x, self._y)] # Start with current position
        
    def end_poly(self):
        """Fill the shape drawn since the last call to begin_fill."""
        if self._poly and self._poly_coords:
            # Add the current position to close the shape if it's not already closed
            if self._poly_coords[-1] != (self._x, self._y):
                self._poly_coords.append((self._x, self._y))

            # Ensure the shape is explicitly closed for polygon filling
            if self._poly_coords[0] != self._poly_coords[-1]:
                self._poly_coords.append(self._poly_coords[0])

            x_coords = [p[0] for p in self._poly_coords]
            y_coords = [p[1] for p in self._poly_coords]
            self._dev.polyline(x_coords, y_coords,
                             lcol=self._pencolor, lthk=self._pensize)
        self._poly = False
        self._poly_coords = []
        
    def begin_fill(self):
        """Call this just before drawing the shape to be filled."""
        self._filling = True
        self._fill_coords = [(self._x, self._y)] # Start with current position

    def end_fill(self):
        """Fill the shape drawn since the last call to begin_fill."""
        #if (self._filling and self._fill_coords) or self._fillcolor:
        if self._filling and self._fill_coords:
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
        
    # https://github.com/python/cpython/blob/3.13/Lib/turtle.py 
    def color(self, *args):
        """Return or set the pencolor and fillcolor.

        Arguments:
        Several input formats are allowed.
        They use 0, 1, 2, or 3 arguments as follows:

        color()
            Return the current pencolor and the current fillcolor
            as a pair of color specification strings as are returned
            by pencolor and fillcolor.
        color(colorstring), color((r,g,b)), color(r,g,b)
            inputs as in pencolor, set both, fillcolor and pencolor,
            to the given value.
        color(colorstring1, colorstring2),
        color((r1,g1,b1), (r2,g2,b2))
            equivalent to pencolor(colorstring1) and fillcolor(colorstring2)
            and analogously, if the other input format is used.

        If turtleshape is a polygon, outline and interior of that polygon
        is drawn with the newly set colors.
        For more info see: pencolor, fillcolor

        Example (for a Turtle instance named turtle):
        >>> turtle.color('red', 'green')
        >>> turtle.color()
        ('red', 'green')
        >>> colormode(255)
        >>> color((40, 80, 120), (160, 200, 240))
        >>> color()
        ('#285078', '#a0c8f0')
        """
        if args:
            l = len(args)
            if l == 1:
                pcolor = fcolor = self.get_color(args[0])
            elif l == 2:
                pcolor = self.get_color(args[0])
                fcolor = self.get_color(args[1])
            elif l > 2:
                #pcolor = fcolor = args
                print("Error: invalid color")
                return
            self._pencolor = pcolor
            self._fillcolor = fcolor
        else:
            return str(self._pencolor), str(self._fillcolor)
            
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
color       = _default_turtle.color
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
begin_poly  = _default_turtle.begin_poly
end_poly    = _default_turtle.end_poly
screen_size = _default_turtle.screen_size
subplot     = _default_turtle.subplot
arrow       = _default_turtle.arrow
arrowf      = _default_turtle.arrowf
ar          = _default_turtle.ar
arf         = _default_turtle.arf
devptr      = _default_turtle.devptr

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
