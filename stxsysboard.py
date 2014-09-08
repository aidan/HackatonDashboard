# STXSysBoard
# Abandon hope all ye who enter here

import sysboard.widgets
from sysboard import settings as cfg

if __name__ == '__main__':
    for m in cfg.modules:
        worker = eval('sysboard.widgets.' + m)()
        worker.start()
        print('STARTED: ' + m)