# STXSysBoard
# Abandon hope all ye who enter here

import sysboard.widgets
from sysboard import settings as cfg
from time import sleep

if __name__ == '__main__':
    workers = []
    for m in cfg.modules:
        worker = eval('sysboard.widgets.' + m)()
        worker.start()
        workers.append(worker)
        print('STARTED: ' + m)
    try:
        while True:
            sleep(600)
    except KeyboardInterrupt:
        print('SHUTDOWN STARTED')
        for worker in workers:
            worker.shutdown()