1) Language used- Python 3.6

2) Libraries required- dns-resolver, geolite2, folium, argparse, warnings
Note: Make sure to install the following packages: dnspython, python-geoip, python-geoip-geolite2, maxminddb-geolite2, folium, argparse
Use this example command: pip install dnspython

3)Inputs- This file takes 5 inputs: input_filename, output_filename, timeout_period, hostname, plot_filename
Sample command: python open_dns_resolver.py input.txt output.txt 1 faceboook.com plot
Use -h or --help to view detailed options. 
If no parameters are passed, following default parameters would be taken: 
	- input.txt
	- output.txt
	- 1
	- facebook.com
	- plot

4) Output- a) An output file containing a list of open DNS resolvers and their coordinates and a sentence mentioning their total count
	   b) A plot of all the coordinates found with the script

To run the file, ensure that input.txt and open_dns_resolver.py are in the same directory.
Run the command: python open_dns_resolver.py
The output files are created in the same directory as the above.