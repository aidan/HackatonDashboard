import sysboard.settings as cfg
import sysboard.workers as w
import sysboard.common as f
from time import strftime


class vm_wro(f.widget):
    def payload(self):
        self.refresh = 30
        for server in cfg.servers:
            output = w.get_snmp(server, cfg.server_pass, cfg.snmp_s)
            if output:
                rnum = f.clean_get('sysboard:' + server + 'LoadID')
                cfg.redis.zadd('sysboard:' + server + 'Load1', [strftime('%M:%S'), output['Load1']], rnum)
                cfg.redis.zadd('sysboard:' + server + 'Load5', [strftime('%M:%S'), output['Load5']], rnum)
                cfg.redis.zadd('sysboard:' + server + 'Load15', [strftime('%M:%S'), output['Load15']], rnum)

                cfg.redis.incr('sysboard:' + server + 'LoadID')
                cfg.redis.zremrangebyrank('sysboard:' + server + 'Load1', 0, -11)
                cfg.redis.zremrangebyrank('sysboard:' + server + 'Load5', 0, -11)
                cfg.redis.zremrangebyrank('sysboard:' + server + 'Load15', 0, -11)

                graph_data = [[], [], []]
                load1 = f.clean_load(output['Load1'])
                load5 = f.clean_load(output['Load5'])
                load15 = f.clean_load(output['Load15'])
                for record in cfg.redis.zrange('sysboard:' + server + 'Load1', 0, -1):
                    graph_data[0].append(eval(record))
                for record in cfg.redis.zrange('sysboard:' + server + 'Load5', 0, -1):
                    graph_data[1].append(eval(record))
                for record in cfg.redis.zrange('sysboard:' + server + 'Load15', 0, -1):
                    graph_data[2].append(eval(record))
                f.push_data('line_chart',  server + 'LoadChart',
                            {'subtitle': load1 + ' / ' + load5 + ' / ' + load15, 'description': '',
                            'series_list': graph_data})