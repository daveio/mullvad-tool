from codecs import encode
from json import loads

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
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


def generate_keypair():
    encoding = serialization.Encoding.Raw
    format = serialization.PrivateFormat.Raw
    private_key = X25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=encoding,
        format=format,
        encryption_algorithm=serialization.NoEncryption(),
    )
    private_text = encode(private_bytes, "base64").decode("utf8").strip()
    public_bytes = private_key.public_key().public_bytes(
        encoding=encoding, format=format
    )
    public_text = encode(public_bytes, "base64").decode("utf8").strip()
    print("Private key: ", private_text)
    print(" Public key: ", public_text)


def create_device(account_id, private_key):
    pass
