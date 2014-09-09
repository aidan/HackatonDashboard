import sysboard.settings as cfg
import sysboard.workers as w
import sysboard.common as f


class vmalpha_wro(f.widget):
    def payload(self):
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
        else:
            f.push_data('pie_chart', 'PieVM1', {'title': '', 'pie_data': []})