import sysboard.workers as w
import sysboard.common as f


class tunelping_wro_other(f.widget):
    def payload(self):
        tunW1 = w.get_ping('16.193.144.1', '1')
        tunW2 = w.get_ping('10.92.2.1', '1')
        tunOVPN = w.get_ping('10.93.3.1', '1')

        if tunW1[0]:
            tunW1 = {'label': 'UP', 'text': 'Warszawa-1', 'description': ''}
            tunW1Format = {'label_color': 'green', 'center': True}
        else:
            tunW1 = {'label': 'DOWN', 'text': 'Warszawa-1', 'description': ''}
            tunW1Format = {'label_color': 'red', 'center': True}
        if tunW2[0]:
            tunW2 = {'label': 'UP', 'text': 'Warszawa-2', 'description': ''}
            tunW2Format = {'label_color': 'green', 'center': True}
        else:
            tunW2 = {'label': 'DOWN', 'text': 'Warszawa-2', 'description': ''}
            tunW2Format = {'label_color': 'red', 'center': True}
        if tunOVPN[0]:
            tunOVPN = {'label': 'UP', 'text': 'OpenVPN', 'description': ''}
            tunOVPNFormat = {'label_color': 'green', 'center': True}
        else:
            tunOVPN = {'label': 'DOWN', 'text': 'OpenVPN', 'description': ''}
            tunOVPNFormat = {'label_color': 'red', 'center': True}

        f.push_data('fancy_listing_3', 'TunO', [tunW1, tunW2, tunOVPN])
        f.push_settings('TunO', {'vertical_center': False, '1': tunW1Format, '2': tunW2Format, '3': tunOVPNFormat})