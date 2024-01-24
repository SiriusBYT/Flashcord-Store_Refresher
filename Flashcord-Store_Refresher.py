import time
from StoreRefresher import *

while True:
    RefreshStore()
    print("\n Now sleeping for 3600 seconds.")
    time.sleep(3600)