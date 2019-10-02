# import click
from threading import Thread
from sys import argv

from dhcp import dhcp
from tcp import tcp
from tftp import tftp
from utility import power_cycle

path = './config.txt'
path_file = open(path, r)
data_dir = path_file.readline()
tftp_port = path_file.readline()
tcp_port = path_file.readline()
ip = path_file.readline()
subnet_mask = path_file.readline()
mac_ip_file = path_file.readline()

def server(): 
    tftp_thread = Thread(target=tftp.do_tftpd, args=[data_dir, ip, tftp_port], name="tftpd")
    tftp_thread.start()

    dhcp_thread = Thread(target=dhcp.do_dhcp, args=[ip, subnet_mask, mac_ip_file], name="dhcpd")
    dhcp_thread.start()

    tcp_thread = Thread(target=tcp.do_tcp, args=[data_dir, tcp_port, ip], name="tcp")
    tcp_thread.start()

    tftp_thread.join()
    dhcp_thread.join()
    tcp_thread.join()


def restart(ports):
    for port in ports:
        power_cycle.power_cycle(port)


def reinstall(port):
    with open("/tcp/reinstall.txt", "w") as f:
        f.write("172.30.1.{}".format(port))
    
    power_cycle.power_cycle(port)


def exit_piman():
    print("Insufficient amount of arguments")
    exit(1)

if __name__ == "__main__":
    args = "Arguments: "
    for a in argv:
        args += a + " "
    print(args)

    if len(argv) < 2:
        power_cycle.power_cycle(10)
        server()
        exit()

    if argv[1] == "server":
        server()
    elif argv[1] == "restart":
        if len(argv) < 3:
            exit_piman()
        restart(argv[2:])
    elif argv[1] == "reinstall":
        if len(argv) < 3:
            exit_piman()
        reinstall(argv[2:])
    else: 
        power_cycle.power_cycle(10)
        server()
