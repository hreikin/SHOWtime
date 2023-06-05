import time
import subprocess
import tempfile
import atexit
import os
import sys
import serial

from PIL import Image

from showtime.ui import Header, Footer
from showtime.utils import split_string_into_chunks

class Screen(object):
    PORTRAIT = 0
    PORTRAIT_FLIPPED = 2
    LANDSCAPE = 1
    LANDSCAPE_FLIPPED = 3
    
    WIDTH = 320
    HEIGHT = 240

    # ANSI Escape Commands
    ESCAPE_CHAR = "\x1b"
    CARRIAGE_RETURN = "\x0d"
    LINEFEED = "\x0a"

    # Foreground Colours
    FG_BLACK = f"{ESCAPE_CHAR}[30m"
    FG_RED = f"{ESCAPE_CHAR}[31m"
    FG_GREEN = f"{ESCAPE_CHAR}[32m"
    FG_YELLOW = f"{ESCAPE_CHAR}[33m"
    FG_BLUE = f"{ESCAPE_CHAR}[34m"
    FG_MAGENTA = f"{ESCAPE_CHAR}[35m"
    FG_CYAN = f"{ESCAPE_CHAR}[36m"
    FG_WHITE = f"{ESCAPE_CHAR}[37m"
    FG_DEFAULT = f"{ESCAPE_CHAR}[39m"   # Default is black.
 
    # Background Colours
    BG_BLACK = f"{ESCAPE_CHAR}[40m"
    BG_RED = f"{ESCAPE_CHAR}[41m"
    BG_GREEN = f"{ESCAPE_CHAR}[42m"
    BG_YELLOW = f"{ESCAPE_CHAR}[43m"
    BG_BLUE = f"{ESCAPE_CHAR}[44m"
    BG_MAGENTA = f"{ESCAPE_CHAR}[45m"
    BG_CYAN = f"{ESCAPE_CHAR}[46m"
    BG_WHITE = f"{ESCAPE_CHAR}[47m"
    BG_DEFAULT = f"{ESCAPE_CHAR}[49m"   # Default is black.

    RESET_STYLING = f"{ESCAPE_CHAR}[0m"
    CLOSE_PORT = f"{ESCAPE_CHAR}c{ESCAPE_CHAR}[2s{ESCAPE_CHAR}[1r\r"

    # VT100 Escape Commands
    ERASE = f"{ESCAPE_CHAR}[2J"
    HOME = f"{ESCAPE_CHAR}[H"

class ScreenContext:
    def __init__(self, port_name="/dev/ttyUSB0", text_size=2, orientation=Screen.LANDSCAPE, fg_colour=Screen.FG_YELLOW, bg_colour=Screen.BG_BLACK, header_type="default", footer_type="default"):
        self.port_name = port_name
        self.characters_on_line = 0
        self.text_size = text_size
        self.orientation = orientation
        self.header_type = header_type
        self.footer_type = footer_type
        # Save colour values the context is created with so things can be reset easily.
        self.fg_colour = fg_colour
        self.bg_colour = bg_colour
        self.current_fg_colour = fg_colour
        self.current_bg_colour = bg_colour
        self.buffer = ""
        self.init_screen()
    
    def init_screen(self):
        self.open_port()
        # Wait 6 seconds for the screen to boot up before we start uploading anything
        self.sleep(6)
        # Reset the LCD styling and set the rotation
        self.reset_lcd_styling()
        self.set_rotation(self.orientation)
        # Set the foreground and background colours
        self.set_fg_colour(self.fg_colour)
        self.set_bg_colour(self.bg_colour)
        self.set_text_size(self.text_size)
        self.fill_with_colour()
        atexit.register(self.cleanup)
        if self.header_type:
            self.header = Header(header_type=self.header_type)
        if self.footer_type:
            self.footer = Footer(footer_type=self.footer_type)
    
    def run(self):
        if self.header_type:
            self.header.render(self)
        if self.footer_type:
            self.footer.render(self)

    def reset_screen(self):
        """
        Reset screen so that it is ready for drawing
        """
        self.reset_lcd_styling().erase_screen().home()
        
        return self
    
    def erase_rows(self, start=0, rows=10):
        """
        Erase specified amount of rows starting from a specified row
        """
        self.home()
        
        for i in range(0, start):
            self.linebreak()
            
        for i in range(0, rows):
            columns = self.get_columns()
            empty_line = ""
            for j in range(0, columns):
                empty_line += " "
                
            self.write(empty_line)
    
    def open_port(self):
        """
        Opens the serial port for writing
        """
        self.port = serial.Serial(self.port_name, baudrate=500000)
    
    def cleanup(self):
        """
        Closes the serial port
        """
        self.buffer = Screen.CLOSE_PORT
        self.sleep(0.1)
        self.port.close()
        
    def push_to_serial(self):
        """
        Uploads the current content of the buffer into the screen
        """
        self.port.write(bytes(self.buffer, encoding="ascii"))
        self.port.flush()
        self.buffer = ""
        
        return self
    
    def get_columns(self):
        """
        Returns the amount of columns, depending on the current text size
        """
        if self.orientation == Screen.LANDSCAPE or self.orientation == Screen.LANDSCAPE_FLIPPED:
            return Screen.WIDTH // (self.text_size * 6)
        else:
            return Screen.HEIGHT // (self.text_size * 6)
    
    def get_rows(self):
        """
        Returns the amount of rows, depending on the current text size
        """
        if self.orientation == Screen.LANDSCAPE or self.orientation == Screen.LANDSCAPE_FLIPPED:
            return Screen.HEIGHT // (self.text_size * 8)
        else:
            return Screen.WIDTH // (self.text_size * 8)
    
    def set_fg_colour(self, colour):
        """
        Set foreground/text color to one of seven colors defined in Screen, eg. Screen.FG_CYAN
        """
        self.buffer += f"{colour}"
        self.sleep()
        self.current_fg_colour = colour
        
        return self
    
    def set_bg_colour(self, colour):
        """
        Set background color to one of seven colors defined in Screen, eg. Screen.BG_CYAN
        """
        self.buffer += f"{colour}"
        self.sleep()
        self.current_bg_colour = colour
        
        return self
    
    def reset_colours(self):
        """
        Reset foreground and background colours to the values used when the ScreenContext was created.
        """
        self.set_bg_colour(self.bg_colour)
        self.set_fg_colour(self.fg_colour)

        return self

    def fill_with_colour(self, mode="default", start=0, rows=10):
        """
        Fill either the entire screen or a selected area with the current background colour.
        """
        self.home()
        if mode == "default":
            total_rows = self.get_rows()
            for i in range(0, total_rows):
                self.write_line("")
            self.home()
        if mode == "selection":
            for i in range(0, start):
                self.linebreak()
            for i in range(0, rows):
                self.write_line("")

        return self
    
    def linebreak(self):
        """
        Moves cursor to the beginning of the next line
        """
        self.buffer += f"{Screen.LINEFEED}{Screen.CARRIAGE_RETURN}"
        
        self.characters_on_line = 0
        
        self.sleep()
        
        return self
    
    def write(self, text, split=True):
        """
        Prints provided text to screen
        """

        self.characters_on_line += len(text)
        if (self.characters_on_line >= self.get_columns()):
            self.characters_on_line = self.characters_on_line % self.get_columns()

        # If the text sends more characters at once than the device can handle,
        # artifacts appear. So, split the string into chunks to prevent this.
        if split:
            text_chunks = split_string_into_chunks(text, 10)
            
            for chunk in text_chunks:
                self.buffer += chunk
                self.sleep(len(chunk) * 0.006)
        else:
            self.sleep(len(chunk) * 0.006)
            
        return self
    
    def write_line(self, text):
        """
        Prints provided text to screen and fills the 
        rest of the line with empty space to prevent
        overlapping text
        """ 
        buffer_text = text
        
        empty_line_count = self.get_columns() - ((len(text) + self.characters_on_line) % self.get_columns())
        
        empty_line = ""
        for i in range(0, empty_line_count):
            empty_line += " "
            
        buffer_text += empty_line
        
        self.write(buffer_text)
        
        return self

    def reset_lcd_styling(self):
        """
        Reset the styling applied to the LCD screen
        """
        self.buffer += Screen.RESET_STYLING
        self.sleep()
        
        return self
    
    def home(self):
        """
        Move cursor to home, eg. 0x0
        """
        self.buffer += Screen.HOME
        self.sleep(0.1)
        self.characters_on_line = 0
        
        # Colors have to be set again after going home otherwise glitches occur
        self.set_bg_colour(self.current_bg_colour).set_fg_colour(self.current_fg_colour)
        return self
    
    def erase_screen(self):
        """
        Erase everything drawn on the screen
        """
        self.buffer += Screen.ERASE
        self.sleep()
        
        return self
    
    def set_text_size(self, size):
        """
        Set text size. Font width is set to 6*size and font height to 8*size
        """
        self.buffer += f"{Screen.ESCAPE_CHAR}[{size}s"
        self.text_size = size
        self.sleep()
        
        return self
    
    def set_rotation(self, rotation):
        """
        Set screen rotation. 
        Accepts values between 0-3, where 1 stands for clockwise 90 degree rotation,
        2 for 180 degree rotation, etc.
        """
        self.orientation = rotation
        self.buffer += f"{Screen.ESCAPE_CHAR}[{self.orientation}r"
        self.sleep()
        
        return self
    
    def set_cursor_pos(self, x, y):
        """
        Set cursor position (in pixels)
        """
        self.buffer += f"{Screen.ESCAPE_CHAR}[{x};{y}H"
        
        self.sleep()
        
        return self

    def set_cursor_loc(self, row, column):
        """
        Set cursor position (in text character coordinates)
        """
        self.buffer += f"{Screen.ESCAPE_CHAR}[{column * self.text_size * 6};{row * self.text_size * 8}H"
        
        self.sleep()
        
        return self

    def draw_image(self, img_path, x, y):
        """
        Draw image at the specified position
        THIS METHOD ISN'T RELIABLE
        """

        _, raw_path = tempfile.mkstemp()

        # Convert the image
        subprocess.call([ "ffmpeg", "-y", "-loglevel", "8","-i", img_path, "-vcodec",
                          "rawvideo", "-f", "rawvideo", "-pix_fmt", "rgb565", raw_path ])
        
        image = Image.open(img_path)
        
        width = image.size[0]
        height = image.size[1]
        
        self.write(f"{Screen.ESCAPE_CHAR}[{x};{y},{width+x};{height+y}i")
        
        self.sleep(0.05)
        # Call a script to cat the image data to the serial port,
        # perhaps we could handle this in Python somehow?
        raw_file = open(raw_path, "rb")
        raw_data = raw_file.read()
        self.port.write(raw_data)
        self.port.flush()
        self.sleep(0.05)
        
        # Add a linebreak to prevent glitches when printing text again
        self.linebreak()
        
        return self
    
    def sleep(self, period=0.001, push_to_serial=True):
        """
        Sleeps for a defined period of time. If push_to_serial is True (default), commands
        and text in the buffer will be pushed to the screen
        """
        if push_to_serial:
            self.push_to_serial()
        
        time.sleep(period)
        
        return self
