import os
import re
import secrets
from codecs import encode
from json import dump, load, loads

import chevron
import click
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from requests import get
from wireguard_tools import WireguardConfig


class Keypair:
    def __init__(self, private, public):
        self.private = private
        self.public = public

    def __repr__(self):
        return f"Keypair(private={self.private}, public={self.public})"


def ensure_dir(path):
    """Creates the specified directory if it doesn't already exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def compose_keypair(mikrotik_interface, print_script):
    keypair = generate_keypair()
    if mikrotik_interface is not None:
        return "Not yet implemented"
    elif print_script:
        return "%s %s" % (keypair.private, keypair.public)
    else:
        retval = "Private key: %s" % keypair.private
        retval = retval + "\n"
        retval = retval + "Public key: %s" % keypair.public
        retval = retval + "\n"
        return retval


def compose_wireguard(config_file, interface_prefix, peer_prefix, listen_port):
    interface, peer = generate_wireguard(
        config_file, interface_prefix, peer_prefix, listen_port
    )
    if interface is None or peer is None:
        return "Failed to generate WireGuard configuration"
    else:
        retval = interface
        retval = retval + "\n"
        retval = retval + peer
        retval = retval + "\n"
        return retval


def compose_openvpn(userpass_file, certificate_file, config_file, interface_prefix):
    return "Not yet implemented"


def get_servers(url="https://api.mullvad.net/app/v1/relays"):
    resp = get(url, timeout=30).content
    return loads(resp)


def generate_wireguard(config_file, interface_prefix, peer_prefix, listen_port):
    config = parse_wireguard_config(config_file)
    if config is None:
        return None, None
    else:
        match = re.search(r"([^/]+)\.conf$", config_file)
        if match:
            interface_name = match.group(1)
        else:
            interface_name = secrets.token_hex(4)
        interface_text = generate_wireguard_interface(
            interface_name, interface_prefix, config["private_key"], listen_port
        )
        peer_text = generate_wireguard_peer(
            interface_name, peer_prefix, interface_name, config
        )
        return interface_text, peer_text


def generate_wireguard_interface(interface_name, interface_prefix, private_key, port):
    if interface_prefix is not None:
        interface_name = interface_prefix + interface_name
    template = """  /interface/wireguard/add \\
        add listen-port={{ listen_port }} \\
        mtu=1420 \\
        name={{ interface_name }} \\
        private-key={{ private_key }} \\
        disabled=yes
    """
    return chevron.render(
        template,
        {
            "interface_name": interface_name,
            "private_key": private_key,
            "listen_port": port,
        },
    )


def generate_wireguard_peer(peer_name, peer_prefix, interface_name, config):
    peer_config = config["peers"][0]
    if peer_prefix is not None:
        peer_name = peer_prefix + peer_name + "-" + str(peer_config["endpoint_port"])
    template = """ /interface/wireguard/peer/add \\
        allowed-address=0.0.0.0/0,::/0 \\
        client-address={{ clientv4 }},{{ clientv6 }} \\
        client-dns={{ clientdns }} \\
        endpoint-address={{ endpoint }} \\
        endpoint-port={{ eport }} \\
        interface={{ pifname }} \\
        name={{ peername }} \\
        public-key="{{ pubkey }}=" \\
        disabled=yes
    """
    return chevron.render(
        template,
        {
            "clientv4": config["addresses"][0],
            "clientv6": config["addresses"][1],
            "clientdns": config["dns_servers"][0],
            "endpoint": peer_config["endpoint_host"],
            "eport": peer_config["endpoint_port"],
            "pifname": interface_name,
            "peername": peer_name,
            "pubkey": peer_config["public_key"],
        },
    )


def generate_keypair():
    encoding = serialization.Encoding.Raw
    priv_format = serialization.PrivateFormat.Raw
    pub_format = serialization.PublicFormat.Raw
    private_key = X25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=encoding,
        format=priv_format,
        encryption_algorithm=serialization.NoEncryption(),
    )
    private_text = encode(private_bytes, "base64").decode("utf8").strip()
    public_bytes = private_key.public_key().public_bytes(
        encoding=encoding, format=pub_format
    )
    public_text = encode(public_bytes, "base64").decode("utf8").strip()
    return Keypair(private_text, public_text)


def create_device(account_id, private_key):
    pass


def parse_wireguard_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = WireguardConfig.from_wgconfig(f).asdict()
            return config
    except FileNotFoundError:
        return None


def init_portgen(starting_port, run_name, state_file):
    ensure_dir(click.get_app_dir("mullvad"))
    with open(state_file, "w") as f:
        dump({run_name: starting_port}, f)
    return "Ready to generate ports with portgen run"


def portgen(run_name, state_file):
    with open(state_file, "r") as f:
        data = load(f)
    port = data[run_name]
    next_port = port + 1
    with open(state_file, "w") as f:
        dump({run_name: next_port}, f)
    return port
