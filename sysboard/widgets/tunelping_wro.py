import sysboard.settings as cfg
import sysboard.workers as w
import sysboard.common as f
from time import strftime


class tunelping_wro(f.widget):
    def payload(self):
        rid = f.clean_get('sysboard:TunPingID')
        tunP = w.get_ping('10.93.1.10', '5')
        tunH = w.get_ping('10.9.15.201', '5')
        values = {'TunPPing': 0, 'TunHPing': 0}

        if tunP[0]:
            f.push_data('just_label', 'TunP', {'just-label': 'UP'})
            f.push_settings('TunP', {'just-label-color': 'green', 'fading_background': 'false'})
            cfg.redis.zadd('sysboard:TunPPing', [strftime('%M:%S'), int(tunP[1])], rid)
            values['TunPPing'] = tunP[1]
        else:
            f.push_data('just_label', 'TunP', {'just-label': 'DOWN'})
            f.push_settings('TunP', {'just-label-color': 'red', 'fading_background': 'false'})
            cfg.redis.zadd('sysboard:TunPPing', [strftime('%M:%S'), 0], rid)
        if tunH[0]:
            f.push_data('just_label', 'TunH', {'just-label': 'UP'})
            f.push_settings('TunH', {'just-label-color': 'green', 'fading_background': 'false'})
            cfg.redis.zadd('sysboard:TunHPing', [strftime('%M:%S'), int(tunH[1])], rid)
            values['TunHPing'] = tunH[1]
        else:
            f.push_data('just_label', 'TunH', {'just-label': 'DOWN'})
            f.push_settings('TunH', {'just-label-color': 'red', 'fading_background': 'false'})
            cfg.redis.zadd('sysboard:TunHPing', [strftime('%M:%S'), 0], rid)

        cfg.redis.incr('sysboard:TunPingID')
        cfg.redis.zremrangebyrank('sysboard:TunPPing', 0, -11)
        cfg.redis.zremrangebyrank('sysboard:TunHPing', 0, -11)

        for graphs in ['TunPPing', 'TunHPing']:
            graphs_data = []
            for records in cfg.redis.zrange('sysboard:' + graphs, 0, -1):
                graphs_data.append(eval(records))
            f.push_data('line_chart', graphs + 'Chart', {'subtitle': '{0:.1f}'.format(values[graphs]) + ' ms',
                                                         'description': '', 'series_list': [graphs_data]})