import threading
import sysboard.settings as cfg
import sysboard.workers as w
import sysboard.common as f
from time import sleep, strftime


class router_wro(threading.Thread):
    def run(self):
        while True:
            output = w.get_snmp()
            if output:
                if output['WAN1Status'] == 1:
                    f.push_data('just_label', 'WANA', {'just-label': 'UP'})
                    f.push_settings('WANA', {'just-label-color': 'green', 'fading_background': 'false'})
                else:
                    f.push_data('just_label', 'WANA', {'just-label': 'DOWN'})
                    f.push_settings('WANA', {'just-label-color': 'red', 'fading_background': 'false'})
                if output['WAN2Status'] == 1:
                    f.push_data('just_label', 'WANB', {'just-label': 'UP'})
                    f.push_settings('WANB', {'just-label-color': 'green', 'fading_background': 'false'})
                elif output['WAN1Status'] == 1:
                    f.push_data('just_label', 'WANB', {'just-label': 'STANDBY'})
                    f.push_settings('WANB', {'just-label-color': 'orange', 'fading_background': 'false'})
                else:
                    f.push_data('just_label', 'WANB', {'just-label': 'DOWN'})
                    f.push_settings('WANB', {'just-label-color': 'red', 'fading_background': 'false'})

                rnum = f.clean_get('sysboard:WANDeltaID')
                output['WAN1InDelta'] = output['WAN1In'] - f.clean_get('sysboard:WAN1InOld')
                cfg.redis.set('sysboard:WAN1InOld', output['WAN1In'])
                output['WAN2InDelta'] = output['WAN2In'] - f.clean_get('sysboard:WAN2InOld')
                cfg.redis.set('sysboard:WAN2InOld', output['WAN2In'])
                output['WAN1OutDelta'] = output['WAN1Out'] - f.clean_get('sysboard:WAN1OutOld')
                cfg.redis.set('sysboard:WAN1OutOld', output['WAN1Out'])
                output['WAN2OutDelta'] = output['WAN2Out'] - f.clean_get('sysboard:WAN2OutOld')
                cfg.redis.set('sysboard:WAN2OutOld', output['WAN2Out'])
                cfg.redis.zadd('sysboard:WAN1InDelta', [strftime('%M:%S'),
                                                        f.clean_transfer(output['WAN1InDelta'])], rnum)
                cfg.redis.zadd('sysboard:WAN1OutDelta', [strftime('%M:%S'),
                                                         f.clean_transfer(output['WAN1OutDelta'])], rnum)
                cfg.redis.zadd('sysboard:WAN2InDelta', [strftime('%M:%S'),
                                                        f.clean_transfer(output['WAN2InDelta'])], rnum)
                cfg.redis.zadd('sysboard:WAN2OutDelta', [strftime('%M:%S'),
                                                         f.clean_transfer(output['WAN2OutDelta'])], rnum)
                cfg.redis.incr('sysboard:WANDeltaID')
                cfg.redis.zremrangebyrank('sysboard:WAN1InDelta', 0, -11)
                cfg.redis.zremrangebyrank('sysboard:WAN1OutDelta', 0, -11)
                cfg.redis.zremrangebyrank('sysboard:WAN2InDelta', 0, -11)
                cfg.redis.zremrangebyrank('sysboard:WAN2OutDelta', 0, -11)

                for graph in ['WAN1In', 'WAN1Out', 'WAN2In', 'WAN2Out']:
                    graph_data = []
                    for record in cfg.redis.zrange('sysboard:' + graph + 'Delta', 0, -1):
                        graph_data.append(eval(record))
                    f.push_data('line_chart', graph + 'Chart',
                                {'subtitle': f.clean_transfer(output[graph + 'Delta'], False), 'description': '',
                                'series_list': [graph_data]})
            print('TICK: Router - Wro')
            sleep(cfg.refresh_time)