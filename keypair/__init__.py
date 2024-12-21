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
    if print_script:
        return f"{keypair.private} {keypair.public}"
    return """
        Private key : {private}
        Public key  : {public}
        """.format(
        private=keypair.private, public=keypair.public
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
