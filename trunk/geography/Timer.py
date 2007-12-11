import time
import threading

class Timer(threading.Thread):
    def __init__(self, seconds, text):
        self._stopevent = threading.Event()
        self.time = seconds
        self.text = text
        threading.Thread.__init__(self)
        
    def run(self):
        while self.time > 0.0 and not self._stopevent.isSet():
            self.text.set("%0.1f" % self.time)
            self.time -= 0.1
            time.sleep(0.1)
        self.text.set("%.1f" % self.time)
        
    def stop(self, timeout=None):
        self._stopevent.set()