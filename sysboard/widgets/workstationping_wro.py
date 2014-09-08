import threading
import sysboard.settings as cfg
import sysboard.workers as w
import sysboard.common as f
from time import sleep


class workstationping_wro(threading.Thread):
    def run(self):
        while True:
            stations = 0
            for ip in range(10, cfg.station_lastip):
                if w.get_ping('10.93.5.' + str(ip))[0]:
                    stations += 1
            f.push_data('pie_chart', 'EmployeesPie',
                        {'title': '', 'pie_data': [['Online', stations], ['Offline', cfg.station_number-stations]]})
            print('TICK: WorkstationPing - Wro')
            sleep(cfg.refresh_time*120)
