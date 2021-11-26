import xml.etree.ElementTree as ET
import argparse
import os
import sys

def parse_services(filename, enable_log):
    #create directory with results
    dir = os.path.splitext(filename)[0]
    if not os.path.exists(dir):
        os.mkdir(dir)

    service_names = dict() #dict for stat

    root = ET.parse(filename).getroot()
    for host in root.findall("host"):
        if host.find("status").attrib["state"] == "up":
            ip = host.find("address").attrib["addr"] + "\n"
            for port in host.find("ports").findall("port"):
                if port.find("state").attrib["state"] == "open":
                    service_name = port.find("service").attrib["name"]

                    #get statistics
                    if service_name in service_names.keys():
                        service_names[service_name] += 1
                    else:
                        service_names.update({service_name : 1})

                    #write ips to file with service name
                    filepath = dir + "/" + service_name + ".txt"
                    with open(filepath, "a+") as f:
                        f.write(ip)
   
    if enable_log:
        checksum = 0
        logfile = os.path.splitext(filename)[0] + '.log'
        with open(logfile, "a+") as f:
            for key in service_names.keys():
                checksum += service_names[key]
                f.write(key + " " + str(service_names[key]) + "\n")
            f.write("Opened ports: " + str(checksum) + '\n')

def get_port_by_service(filename, service_names):
    ports = set()

    root = ET.parse(filename).getroot()
    for host in root.findall("host"):
        if host.find("status").attrib["state"] == "up":
            ip = host.find("address").attrib["addr"] + "\n"
            for port in host.find("ports").findall("port"):
                if port.find("state").attrib["state"] == "open":
                    service_name = port.find("service").attrib["name"]
                    if service_name in service_names:
                        ports.add((port.attrib['portid']))

    for i in ports:
        print(i)

def read_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Parser for nmap .xml results')
    parser.add_argument('-f','--filename', help = 'Name of xml file for pasrsing')
    parser.add_argument('-s', '--services', help = 'Create folder with files, which contains ips with founded service', action='store_true')
    parser.add_argument('-l','--log', help = 'Generate log file', action='store_true')
    parser.add_argument('--ports-by-services', help = 'Get ports with specified services. Service names must be specified')
    opts = parser.parse_args(args)
    return opts

if __name__ == "__main__":
    options = read_options(sys.argv[1:])

    if options.filename == None:
        print('Filename always must be specified')
        exit(0)
    else:
        if options.services:
            parse_services(options.filename, options.log)
        if options.ports_by_services:
            get_port_by_service(options.filename, options.ports_by_services.split(','))


    