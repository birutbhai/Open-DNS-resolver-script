#This scripts finds the geographical coordinates of open DNS resolvers
#Abhisek Banerjee AXB180050
#Pratidhi Pratyasha PXP170020
#Ref https://github.com/jpverkamp/dnsscan#Ref:https://deparkes.co.uk/2016/06/03/plot-lines-in-folium/
#Ref:https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/MinMaxLimits.ipynb
#Ref https://github.com/jpverkamp/dnsscan
import warnings
warnings.filterwarnings("ignore")
import sys
import os
import dns.resolver
from geolite2 import geolite2
import folium
import argparse

def getIpList(list, input_file):
    with open(input_file, "r") as addresses:
        for address in addresses:
            list.append(address[:-1])

def queryDns(list,coordinates,timeout,host,output_file):
    resolver_count = 0
    address_count = 0
    ip_db = geolite2.reader()
    resolver = dns.resolver.Resolver()
    resolver.lifetime = timeout
    file= open(output_file,"w")
    for ip in list:
        try:
            resolver.nameservers = [ip]
            dns_query_response = resolver.query(host, 'A')
            f_entry = "ip: " +  str(ip)
            resolver_count = resolver_count + 1
            loc = ip_db.get(ip)       
            if loc is not None:
                coordinates.append(tuple([loc['location']['latitude'], loc['location']['longitude']]))
                f_entry = f_entry+("; latitude: ")+ str(loc['location']['latitude'])+ ("; longitude: ") + str(loc['location']['longitude']) + "\n"
                address_count = address_count + 1
            else:
                f_entry = f_entry+("; Could not resolve location\n")
            file.write(f_entry)
        except:
            continue
    geolite2.close()
    file.write("\nTotal number of ips used for verification: " + str(len(list)))
    file.write(("\nTotal number of open DNS resolvers: ")+str(resolver_count)+("\nTotal number of location resolvable open DNS resolvers: ")+str(address_count))
    file.write("\nTotal number of location unresolved open DNS resolvers: "+str(resolver_count-address_count))
    file.write("\nTotal number of ips found not to be open DNS resolvers: " + str(len(list)-resolver_count))
    file.close()

def plot(coordinates,output_plot):
    f = folium.Figure(width=1000, height=500)
    plot =  folium.Map(location=[0,0], zoom_start=2, min_zoom = 2.5)
    for coordinate in coordinates:  
            folium.Marker(coordinate).add_to(plot)
    plot.save(output_plot)

if __name__ == "__main__":
    default_output_file = "output.txt"
    default_input_file = "input.txt"
    default_timeout = 1
    default_host = "facebook.com"
    default_output_plot = "plot"
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="Input file name.", nargs='?',
            default=default_input_file, const=default_input_file)
    parser.add_argument("outfile", type=str, help="Output file name.", nargs='?',
            default=default_output_file, const=default_output_file)
    parser.add_argument("timeout", type=float, help="Time after dns query should timeout.", nargs='?',
            default=default_timeout, const=default_timeout)
    parser.add_argument("host", type=str, help="Target host name to resolve.", nargs='?',
            default=default_host, const=default_host)
    parser.add_argument("outplot", type=str, help="Output plot name(html file will be generated).", nargs='?',
            default=default_output_plot, const=default_output_plot)
    args = parser.parse_args()
    input_file = args.infile
    output_file = args.outfile
    timeout = args.timeout
    host = args.host
    output_plot = args.outplot+".html"
    list = []
    getIpList(list, input_file)
    coordinates=[]
    queryDns(list,coordinates,timeout,host,output_file)
    plot(coordinates,output_plot)
