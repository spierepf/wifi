import network

sta_if = network.WLAN(network.WLAN.IF_STA)

def disconnect_wifi():
    if sta_if.isconnected():
        sta_if.disconnect()
        sta_if.active(False)

def connect_wifi(wifi_credentials, log=print):
    if not sta_if.isconnected():
        log('Scanning for access points.')
        sta_if.active(True)
        access_points = sta_if.scan()
        for access_point in access_points:
            ssid = access_point[0]
            if ssid in wifi_credentials:
                log(f'Attempting to connect to {ssid.decode()}')
                sta_if.connect(wifi_credentials[ssid]['ssid'], wifi_credentials[ssid]['key'])
                status = sta_if.status()
                while status in [network.STAT_CONNECTING, network.STAT_IDLE]:
                    status = sta_if.status()
                if status == network.STAT_GOT_IP:
                    break
                sta_if.active(False)
                for code in [x for x in dir(network) if x.startswith('STAT_')]:
                    if getattr(network, code) == status:
                        log(f"Connection to {ssid.decode()} failed with error: {code}")
                sta_if.active(True)
    log('Network config:', sta_if.ipconfig('addr4'))

