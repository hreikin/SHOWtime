from showtime.tabs.hello import HelloTab
#from showtime.tabs.bitcoin import BitcoinPrice, Bitcoind
from showtime.tabs.sysinfo import SystemStats, DiskUsage
from showtime.tabs.uptime import WebsiteUptime

import os

# Add any tabs you want to be visible here
tabs = [
         HelloTab(),

         # Track a running Bitcoin node
         #Bitcoind({"host": "http://127.0.0.1:8332",
         #          "username": "bitcoinrpc",
         #          # Read the password from a file
         #          "password": "password" }),
        
         # A Bitcoin price ticker
         #BitcoinPrice(),
         
         # Displays CPU, RAM usage and uptime
         SystemStats(),
         
         # Displays disk usage
         DiskUsage(),
         
         # Tracks website uptime
         WebsiteUptime({"websites": [ {"name": "Google",
                                       "url": "http://google.com"} ] })
       ]
