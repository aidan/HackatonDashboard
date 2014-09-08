import threading
import sysboard.settings as cfg
import sysboard.workers as w
import sysboard.common as f
from time import sleep


class vmalpha_wro(threading.Thread):
    def run(self):
        while True:
            output = w.get_vm(cfg.vm_mothers['Alpha'])
            if output:
                zonza = 0
                zadar = 0
                other = 0
                for vms in output:
                    if 'zonza' in vms:
                        zonza += output[vms]['cputimedelta']
                    elif 'zadar' in vms:
                        zadar += output[vms]['cputimedelta']
                    else:
                        other += output[vms]['cputimedelta']
                f.push_data('pie_chart', 'PieVM1', {'title': '', 'pie_data': [['Zonza', zonza],
                                                                              ['Zadar', zadar],
                                                                              ['Other', other]]})
            print('TICK: VMAlpha - Wro')
            sleep(cfg.refresh_time)