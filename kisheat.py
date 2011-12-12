#!/usr/bin/python
import pprint
import collections
import heatmap
import xml.etree.ElementTree
import re
from xml.etree.ElementTree import ElementTree
from optparse import OptionParser
from os.path import basename


def splitup(stringthing):
	parts = stringthing.partition('=')
	return (parts[0], parts[2].strip('"'))

def default_factory(): return 0

pp = pprint.PrettyPrinter(indent=4)

usage = "usage: [options] [path/to/]SAMPLE_NAME [ESSID PATTERN]"
parser = OptionParser(usage=usage)
parser.add_option('-l', '--list',help='Just list xSSIDs and exit',dest='listOnly',default=False,action='store_true')
parser.add_option('-a', '--alldata',help='Include all samples taken while not moving (can exagerate signal strength)',dest='allData',default=False,action='store_true')
parser.add_option('-m','--mergedata',help='Merge all datasets into one overlay whose name you must specify.  If you use a regex filter the merged data will be restricted to accesspoints that matched it. Useful for mapping whole-network coverage mapping.',dest='mergeTo',default=None,action='store',type='string')

(options, args) = parser.parse_args()

if len(args) == 0:
	print usage
	exit()

matchEssid = '.*'

if len(args) == 2:
	matchEssid = args[1]


essidRE = re.compile(matchEssid)

tree = ElementTree()
accesspoints = {}
networks = {}
datasetName = basename(args[0])
tree.parse(args[0]+'.netxml')

for network in tree.getroot().findall('wireless-network'):
	bssid = network.find('BSSID').text
	essid = network.find('SSID/essid')
	if essid is not None:
		if essid.text is not None:
			networks[bssid] = essid.text
		else:
			networks[bssid] = 'none(%s)'%bssid
	else:
		networks[bssid] = 'cloaked(%s)'%bssid

if options.mergeTo is not None:
	accesspoints[options.mergeTo] = list()

if options.listOnly:
	for bssid,essid in networks.items():
		if essidRE.search(essid):
			print bssid," ",essid
else:
	f = open(args[0]+'.gpsxml', 'r')

	locations = {}

	for line in f:
		if line.find('gps-point'):
			dict = collections.defaultdict(default_factory,map(splitup,line.split()))
			if dict['bssid'] != 0 and dict['bssid'] in networks:
				if essidRE.search(networks[dict['bssid']]):
					if (dict['bssid'] not in accesspoints) and (options.mergeTo is None):
						accesspoints[dict['bssid']] = list()
					# The heat map rendering logic will treat repetitive mentions of the same location
					# as an indication that the value for that location is higher.  In practical terms this means
					# that if you happened to have stopped at a stop sign for a bit and you include all data
					# gathered there, the position at that stop sign will look like it's getting quite a lot
					# more signal that it really is.  So this logic just ensures that we have no more than
					# one sample for any given lat/lon position for a particular bssid.  This does *not* totally
					# eliminate the exaggeration effect as gps values have jitter, but it does substantially reduce it.
					if not options.allData:
						location = '%(bssid)s,%(lon)f,%(lat)f' % {"bssid": dict['bssid'], "lon": float(dict['lon']), "lat": float(dict['lat'])}
						if location in locations:
							locations[location]+=1
						else:
							locations[location]=1
					if (locations[location] == 1) or options.allData:
						if options.mergeTo is None:
							accesspoints[dict['bssid']].append((float(dict['lon']),float(dict['lat']),100+float(dict['signal_dbm'])))
						else:
							accesspoints[options.mergeTo].append((float(dict['lon']),float(dict['lat']),100+float(dict['signal_dbm'])))

	for key in accesspoints:
		if options.mergeTo is None:
			print networks[key]
		else:
			print options.mergeTo
		hm = heatmap.Heatmap()
		try:
			hm.heatmap(accesspoints[key],'%s.png'%key)
		except ZeroDivisionError:
			print "Error generating map overlay - data sample too small"
		except IndexError:
			print "Error generating map overlay - data sample too small"
		if options.mergeTo is None:
			hm.saveKML('%(dataset)s-%(network)s.kml'% {'dataset' : datasetName, 'network': networks[key]})
		else:
			hm.saveKML('%(dataset)s-%(network)s.kml'% {'dataset' : datasetName, 'network': options.mergeTo})
