from showtime.context import Screen, ScreenContext
import time

class Header:
    
    def render_header(self, ctx, tab, tab_name, tab_count):
        # Print top row (tab name)
        ctx.home().set_bg_colour(Screen.BG_RED).set_fg_colour(Screen.FG_WHITE).write(tab_name)
        
        columns = ctx.get_columns() - len(tab_name)
        empty_line = ""
        for i in range(0, columns):
            empty_line += " "
            
        ctx.write(empty_line)
        
        # Print bottom row (tabs)
        characters_drawn = 0
        
        ctx.write("%d / %d" % (tab+1, tab_count))
        
        time_str = time.strftime("%H:%M")
        
        columns = ctx.get_columns() - len("%d / %d" % (tab+1, tab_count)) - len(time_str)
        empty_line = ""
        for i in range(0, columns):
            empty_line += " "
            
        # Draw the time
        ctx.write(empty_line + time_str)
                
        ctx.set_bg_colour(Screen.BG_BLACK)
