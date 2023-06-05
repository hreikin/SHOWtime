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
    def __init__(self, title="Odroid SHOW", header_type="default"):
        self.header_type = header_type
        super(Header, self).__init__(title)

    def render(self, ctx, tab_idx=0, tab_count=1):
        if self.header_type == "default":
            # Print top row (title)
            ctx.home().write_line(self.title)
            
            # Print bottom row (tabs only)
            ctx.write(f"{tab_idx+1}/{tab_count}")
            
            time_str = time.strftime("%H:%M")
            
            columns = ctx.get_columns() - len(f"{tab_idx+1}/{tab_count}") - len(time_str)
            empty_line = ""
            for i in range(0, columns):
                empty_line += " "
                
            # Print the empty space and time
            ctx.write(empty_line + time_str)
        elif self.header_type == "single":
            # Print top row (title)
            ctx.home().write(self.title)
            
            time_str = time.strftime("%H:%M")
            
            columns = ctx.get_columns() - len(f"{self.title}") - len(time_str)
            empty_line = ""
            for i in range(0, columns):
                empty_line += " "
                
            # Print the empty space and time
            ctx.write(empty_line + time_str)
        else:
            raise ValueError("Incorrect keyword argument used for `header_type`, available options are 'default', 'single' or None.")

class Footer(BaseComponent):
    def __init__(self, title=str(), footer_type="default"):
        self.footer_type = footer_type
        super(Footer, self).__init__(title)
    
    def render(self, ctx):
        total_rows = ctx.get_rows()
        if self.footer_type == "default":
            footer_start = total_rows-2
            ctx.set_cursor_loc(footer_start, 0)
            ctx.write_line("Footer line 1")
            ctx.write_line("Footer line 2")
        elif self.footer_type == "single":
            footer_start = total_rows-1
            ctx.set_cursor_loc(footer_start, 0)
            ctx.write_line("Footer line 1")
        else:
            raise ValueError("Incorrect keyword argument used for `footer_type`, available options are 'default', 'single' or None.")