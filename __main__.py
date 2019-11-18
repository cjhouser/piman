import click
import piman

@click.group()
def cli():
    pass

@cli.command()
def server():    
    piman.server()

@cli.command()
@click.argument('host_ips', nargs=-1, type=click.STRING)
def restart(host_ips):
    piman.restart(host_ips)

@cli.command()
@click.argument('host_ip', nargs=1, type=click.STRING)
def reinstall(host_ip):
    piman.reinstall(host_ip)

@cli.command()
@click.argument('switch_port', nargs=1, type=click.INT)
def powercycle(switch_port):
    piman.powercycle(switch_port)

if __name__ == "__main__":
    cli()
