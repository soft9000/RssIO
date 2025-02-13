
# Capture test case scripts & responses.

from abc import *

from io import StringIO
import subprocess
import sys    
    
class SubTee(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def print(self, msg:str)->bool:
        '''Return False to stop the capture.'''
        print(msg, end='')
        return False
    
    def capture(self, cmd):
        '''Fork + capture the output to the command. 
        Will capture until your .print() returns False.
        Process exit / return code + string is returned.
        '''
        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              bufsize=1, text=True) as p, StringIO() as buf:
            while True:
                if p.stdout:
                    for line in p.stdout:
                        buf.write(line)
                        if self.print(line) == False:
                            break

        return p.returncode, buf.getvalue()


class TeeQuit(SubTee):

    def print(self, msg):
        print(msg, end='')
        if msg == '5':
            return False
        return True


if __name__ == '__main__':
    capture = TeeQuit()
    data = capture.capture(' '.join([sys.executable,'./nexus9000/rss9000.py']))
    print(data)