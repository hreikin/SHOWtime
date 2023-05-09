from showtime.context import Screen, ScreenContext
from showtime.tabs.tab import Tab

import time

class HelloTab(Tab):
    def __init__(self):
        self.title = "Hello World Tab"
        
    def render_tab(self, ctx):

        ctx.set_bg_colour(Screen.BG_BLACK)
        ctx.set_fg_colour(Screen.FG_WHITE)

        ctx.write_line("Hello, World!")
