from codecs import encode

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


class Keypair:
    def __init__(self, private, public):
        self.private = private
        self.public = public

    def __repr__(self):
        return f"Keypair(private={self.private}, public={self.public})"


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
