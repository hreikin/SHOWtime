from showtime.context import Screen, ScreenContext
import time

class BaseComponent():
    def __init__(self, title=str()):
        self.title = title
    
    def render(self, ctx):
        raise NotImplementedError(f"'render()' not implemented on {self.__class__.__name__} UI component!")

class Tab(BaseComponent):
    def __init__(self, config=dict(), title=str()):
        self.config = config
        super(Tab, self).__init__(title)
    
    def render(self, ctx):
        return super().render(ctx)

class Header(BaseComponent):
    def __init__(self, title=str()):
        super(Header, self).__init__(title)

    def render(self, ctx, tab_idx=0, title="Odroid SHOW", tab_count=1):
        # Print top row (title)
        ctx.home().write_line(title)
        
        # Print bottom row (tabs only)
        ctx.write(f"{tab_idx+1}/{tab_count}")
        
        time_str = time.strftime("%H:%M")
        
        columns = ctx.get_columns() - len(f"{tab_idx+1}/{tab_count}") - len(time_str)
        empty_line = ""
        for i in range(0, columns):
            empty_line += " "
            
        # Print the empty space and time
        ctx.write(empty_line + time_str)

class Footer(BaseComponent):
    def __init__(self, title=str()):
        super(Footer, self).__init__(title)
    
    def render(self, ctx):
        total_rows = ctx.get_rows() 
        footer_start = total_rows-2
        ctx.set_cursor_loc(footer_start, 0)
        ctx.write_line("Footer line 1")
        ctx.write_line("Footer line 2")