import sysboard.settings as cfg
import sysboard.workers as w
import sysboard.common as f


class workstationping_wro(f.widget):
    def payload(self):
        self.refresh = 600
        stations = 0
        for ip in range(10, cfg.station_lastip):
            if w.get_ping('10.93.5.' + str(ip))[0]:
                stations += 1
        f.push_data('pie_chart', 'EmployeesPie',
                    {'title': '', 'pie_data': [['Online', stations], ['Offline', cfg.station_number-stations]]})
