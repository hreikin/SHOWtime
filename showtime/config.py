from showtime.tabs import HelloTab, SystemStats, DiskUsage, WebsiteUptime

# Add any tabs you want to be visible here
tabs = [
         HelloTab(),
         
         # Displays CPU, RAM usage and uptime
         SystemStats(),
         
         # Displays disk usage
         DiskUsage(),
         
         # Tracks website uptime
         WebsiteUptime({"websites": [ {"name": "Google",
                                       "url": "http://google.com"} ] })
       ]
