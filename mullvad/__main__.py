import mullvad


def __main__():
    keypair = mullvad.generate_keypair()
    print("Private key: %s" % keypair["private"])
    print(" Public key: %s" % keypair["public"])


if __name__ == "__main__":
    __main__()
