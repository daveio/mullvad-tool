from json import loads

from requests import get


def get_servers(url="https://api.mullvad.net/app/v1/relays"):
    resp = get(url, timeout=30).content
    return loads(resp)


def parse_servers():
    # json = get_servers()
    # data = json.get("wireguard")
    # relays = [relay for relays in data["relays"]]
    interface_template = """  /interface/wireguard/add \\
        add listen-port=[[LPORT]] \\
        mtu=1420 \\
        name=[[IIFNAME]]
    """
    peer_template = """ /interface/wireguard/peer/add \\
        allowed-address=0.0.0.0/0,::/0 \\
        client-address=[[CLIENTV4]],[[CLIENTV6]] \\
        client-dns=[[CLIENTDNS]] \\
        endpoint-address=[[ENDPOINT]] \\
        endpoint-port=[[EPORT]] \\
        interface=[[PIFNAME]] \\
        name=[[PEERNAME]] \\
        public-key="[[PUBKEY]]=" \\
        disabled=yes
    """
    print(interface_template)
    print(peer_template)
