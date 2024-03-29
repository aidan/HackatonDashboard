import subprocess
import shlex
from pysnmp.entity.rfc3413.oneliner import cmdgen
import sysboard.settings as cfg
import sysboard.common as f


def get_ping(hostname, count='1'):
    try:
        out = subprocess.check_output(shlex.split('fping -q -c' + count + ' ' + hostname), stderr=subprocess.STDOUT)
        m = str(out).split(' ')[7].split('/')[1]
        return [True, float(m)]
    except:
        return [False]


def get_snmp(host, community, snmp):
    errorindication, _, _, varbinds = snmp.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((host, 161)), *snmp.field)
    if errorindication:
        return False
    else:
        out = {}
        for name, val in varbinds:
            if val > -1:
                out[snmp.field_index[str(name)]] = int(val.prettyPrint().replace('.', ''))
            else:
                out[snmp.field_index[str(name)]] = 0
        return out


def get_vm(vm_master):
    out = {}
    try:
        processors = float(vm_master.getInfo()[2])
        for machine in vm_master.listDomainsID():
            vm = vm_master.lookupByID(machine)
            infos = vm.info()
            name = vm.name()
            if infos[0] == 1:
                cputime_percentage = int(1.0e-7 * float(infos[4]) / processors)
                vmdelta = f.clean_get('sysboard:vm:' + name)
                out[name] = {'cputimeraw': cputime_percentage, 'cputimedelta': cputime_percentage - vmdelta}
                cfg.redis.set('sysboard:vm:' + name, cputime_percentage)
    except Exception:
        return False
    return out
