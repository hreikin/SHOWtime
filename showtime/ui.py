from showtime.context import Screen, ScreenContext
import time

class BaseComponent():
    def __init__(self, config={}):
        self.config = config
    
    def render(self, ctx):
        raise NotImplementedError(f"'render()' not implemented on {self.__class__.__name__} UI component!")

class Tab(BaseComponent):
    def __init__(self, config={}):
        self.config = config
        super(Tab, self).__init__(self.config)
    
    def render(self, ctx):
        return super().render(ctx)

class Header(BaseComponent):
    def __init__(self, config={}):
        self.config = config
        super(Tab, self).__init__(self.config)

    def render(self, ctx, tab_idx, title, tab_count):
        # Print top row (title)
        ctx.home().set_bg_colour(ctx.current_bg_colour).set_fg_colour(ctx.current_fg_colour).write(title)
        
        columns = ctx.get_columns() - len(title)
        empty_line = ""
        for i in range(0, columns):
            empty_line += " "
            
        ctx.write(empty_line)
        
        # Print bottom row (tabs)
        characters_drawn = 0
        
        ctx.write("%d / %d" % (tab_idx+1, tab_count))
        
        time_str = time.strftime("%H:%M")
        
        columns = ctx.get_columns() - len("%d / %d" % (tab_idx+1, tab_count)) - len(time_str)
        empty_line = ""
        for i in range(0, columns):
            empty_line += " "
            
        # Draw the time
        ctx.write(empty_line + time_str)
                
        ctx.set_bg_colour(Screen.BG_BLACK)
