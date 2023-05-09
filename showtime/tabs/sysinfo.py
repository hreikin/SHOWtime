from showtime.context import Screen, ScreenContext
from showtime.tabs.tab import Tab
from showtime.utils import format_timespan, get_progress_bar

import psutil
import time
import humanfriendly

class SystemStats(Tab):
    def __init__(self):
        self.title = "System stats"
        
        self.cpu_usages = [0.0] * len(psutil.cpu_percent(percpu=True))
        
        self.used_ram = 12505903
        self.total_ram = 20189390
        
        self.YELLOW_THRESHOLD = 0.33
        self.RED_THRESHOLD = 0.66
        
        self.uptime = 0
        
    def render_tab(self, ctx):
        # Update system info
        self.update_sysinfo()

        # Print CPU usage
        for i in range(0, len(self.cpu_usages)):
            cpu_usage = self.cpu_usages[i]
            
            ctx.set_fg_colour(Screen.FG_WHITE)
            
            ctx.write("CPU %d:" % i).set_fg_colour(Screen.FG_YELLOW).write_line(" %.2f %%" % (cpu_usage*100)).set_fg_colour(Screen.FG_WHITE).write("[")
            
            if cpu_usage < self.YELLOW_THRESHOLD:
                ctx.set_fg_colour(Screen.FG_GREEN)
            elif cpu_usage >= self.YELLOW_THRESHOLD and cpu_usage <= self.RED_THRESHOLD:
                ctx.set_fg_colour(Screen.FG_YELLOW)
            else:
                ctx.set_fg_colour(Screen.FG_RED)
                
            ctx.write(get_progress_bar(ctx.get_columns()-2, cpu_usage)).set_fg_colour(Screen.FG_WHITE).write("]")
            
        # Print RAM
        used = humanfriendly.format_size(self.used_ram)
        total = humanfriendly.format_size(self.total_ram)
        ctx.linebreak().write_line("RAM").set_fg_colour(Screen.FG_YELLOW).write_line("%s / %s" % (used, total)).set_fg_colour(Screen.FG_WHITE)
        
        ram_usage = float(self.used_ram) / float(self.total_ram)
            
        ctx.write("[")
        
        if ram_usage < 0.33:
            ctx.set_fg_colour(Screen.FG_GREEN)
        elif ram_usage >= 0.33 and ram_usage <= 0.66:
            ctx.set_fg_colour(Screen.FG_YELLOW)
        else:
            ctx.set_fg_colour(Screen.FG_RED)
            
        ctx.write(get_progress_bar(ctx.get_columns()-2, ram_usage)).set_fg_colour(Screen.FG_WHITE).write("]")
        
        # Print uptime
        ctx.linebreak().write_line("Uptime:").set_fg_colour(Screen.FG_YELLOW).write_line("%s" % format_timespan(self.uptime)).set_fg_colour(Screen.FG_WHITE)
    
    def update_sysinfo(self):
        cpu_times = psutil.cpu_percent(percpu=True)
        
        for i, cpu_time in enumerate(cpu_times):
            self.cpu_usages[i] = float(cpu_time / 100)
            
        self.total_ram = psutil.virtual_memory().total
        self.used_ram = psutil.virtual_memory().total - psutil.virtual_memory().available
        
        self.uptime = time.time() - psutil.boot_time()
        
class DiskUsage(Tab):
    def __init__(self):
        self.title = "Disk usage"
        
        self.disk_usage = {}
        
        self.YELLOW_THRESHOLD = 0.33
        self.RED_THRESHOLD = 0.66
        
    def render_tab(self, ctx):
        self.update_disk_usage()
        
        for device_name, usage in self.disk_usage.items():
            ctx.write_line("%s" % device_name)
            
            ctx.set_fg_colour(Screen.FG_YELLOW).write_line("%s / %s" % (humanfriendly.format_size(usage["used"]),
                                                                humanfriendly.format_size(usage["total"])))
            
            ctx.set_fg_colour(Screen.FG_WHITE).write("[")
            
            usage_percent = float(usage["used"]) / float(usage["total"])
            
            if usage_percent < self.YELLOW_THRESHOLD:
                ctx.set_fg_colour(Screen.FG_GREEN)
            elif usage_percent >= self.YELLOW_THRESHOLD and usage_percent <= self.RED_THRESHOLD:
                ctx.set_fg_colour(Screen.FG_YELLOW)
            else:
                ctx.set_fg_colour(Screen.FG_RED)
                
            ctx.write(get_progress_bar(ctx.get_columns()-2, usage_percent)).set_fg_colour(Screen.FG_WHITE).write("]").linebreak()
        
    def update_disk_usage(self):
        disk_partitions = psutil.disk_partitions()
        
        for disk_partition in disk_partitions:
            if disk_partition.mountpoint:
                disk_usage = psutil.disk_usage(disk_partition.mountpoint)
                
                self.disk_usage[disk_partition.mountpoint] = {"total": disk_usage.total,
                                                              "used": disk_usage.used}
                
                
