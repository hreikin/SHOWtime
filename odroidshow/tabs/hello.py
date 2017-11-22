from odroidshow.context import Screen, ScreenContext
from odroidshow.tabs.tab import Tab

import time

class HelloTab(Tab):
    def __init__(self):
        self.title = "Hello World Tab"
        
    def render_tab(self, ctx):

        ctx.bg_color(Screen.BLACK)
        ctx.fg_color(Screen.WHITE)

        ctx.write_line("Hello, World!")
