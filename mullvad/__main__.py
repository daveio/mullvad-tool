import click

import mullvad

mullvad_version = "0.1.0"


@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo("mullvad %s" % mullvad_version)


@cli.command()
@click.option(
    "-m",
    "mikrotik_interface",
    help="Generate Mikrotik script to set key on interface TEXT",
)
@click.option(
    "-s",
    "print_script",
    is_flag=True,
    show_default=True,
    default=False,
    help="Print keys for a script, as PRIVATEKEY PUBLICKEY",
)
def keygen(mikrotik_interface, print_script):
    keypair = mullvad.generate_keypair()
    if mikrotik_interface is not None:
        click.echo("Not yet implemented")
        pass
    elif print_script:
        click.echo("%s %s" % (keypair.private, keypair.public))
    else:
        click.echo("Private key: %s" % keypair.private)
        click.echo(" Public key: %s" % keypair.public)


@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("-i", "interface_prefix", help="Prefix created interface names with TEXT")
@click.option("-p", "peer_prefix", help="Prefix created peer names with TEXT")
def wireguard(interface_prefix, peer_prefix):
    click.echo("Not yet implemented")


@cli.command()
@click.argument("userpass_file", type=click.Path(exists=True))
@click.argument("certificate_file", type=click.Path(exists=True))
@click.argument("config_file", type=click.Path(exists=True))
@click.option("-i", "interface_prefix", help="Prefix created interface names with TEXT")
def openvpn(userpass_file, certificate_file, config_file, interface_prefix):
    click.echo("Not yet implemented")


if __name__ == "__main__":
    cli()
