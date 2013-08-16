#coding:utf-8
#!/usr/bin/env python

'''
 ______                              __      __      
/\__  _\                  __        /\ \    /\ \__   
\/_/\ \/     ___     ____/\_\     __\ \ \___\ \ ,_\  
   \ \ \   /' _ `\  /',__\/\ \  /'_ `\ \  _ `\ \ \/  
    \_\ \__/\ \/\ \/\__, `\ \ \/\ \L\ \ \ \ \ \ \ \_ 
    /\_____\ \_\ \_\/\____/\ \_\ \____ \ \_\ \_\ \__\
    \/_____/\/_/\/_/\/___/  \/_/\/___L\ \/_/\/_/\/__/
                                  /\____/            
                                  \_/__/             
 __ Anthr@X        __                
/\ \              /\ \               
\ \ \         __  \ \ \____    ____  
 \ \ \  __  /'__`\ \ \ '__`\  /',__\ 
  \ \ \L\ \/\ \L\.\_\ \ \L\ \/\__, `\
   \ \____/\ \__/.\_\\ \_,__/\/\____/
    \/___/  \/__/\/_/ \/___/  \/___/ 
                                     
'''


import platform
import sys
import socket as sk
import httplib
from subprocess import Popen, PIPE
import re
from optparse import OptionParser
import threading
from threading import Thread
from Queue import Queue

NUM = 50
TIMEOUT=2
PORTS=[21,22,23,25,80,81,110,135,139,389,443,445,873,1433,1434,1521,2433,3306,3307,3389,5800,5900,8080,22222,22022,27017,28017]
URLS=['','phpinfo.php','phpmyadmin/','xmapp/','zabbix/','jmx-console/','.svn/entries','nagios/','index.action','login.action']

PROBES=[
'\r\n\r\n',
'GET / HTTP/1.0\r\n\r\n',
'GET / \r\n\r\n',
'\x01\x00\x00\x00\x01\x00\x00\x00\x08\x08',
'\x80\0\0\x28\x72\xFE\x1D\x13\0\0\0\0\0\0\0\x02\0\x01\x86\xA0\0\x01\x97\x7C\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0',
'\x03\0\0\x0b\x06\xe0\0\0\0\0\0',
'\0\0\0\xa4\xff\x53\x4d\x42\x72\0\0\0\0\x08\x01\x40\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x40\x06\0\0\x01\0\0\x81\0\x02PC NETWORK PROGRAM 1.0\0\x02MICROSOFT NETWORKS 1.03\0\x02MICROSOFT NETWORKS 3.0\0\x02LANMAN1.0\0\x02LM1.2X002\0\x02Samba\0\x02NT LANMAN 1.0\0\x02NT LM 0.12\0',
'< NTP/1.2 >\n',
'< NTP/1.1 >\n',
'< NTP/1.0 >\n',
'\0Z\0\0\x01\0\0\0\x016\x01,\0\0\x08\0\x7F\xFF\x7F\x08\0\0\0\x01\0 \0:\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\04\xE6\0\0\0\x01\0\0\0\0\0\0\0\0(CONNECT_DATA=(COMMAND=version))',
'\x12\x01\x00\x34\x00\x00\x00\x00\x00\x00\x15\x00\x06\x01\x00\x1b\x00\x01\x02\x00\x1c\x00\x0c\x03\x00\x28\x00\x04\xff\x08\x00\x01\x55\x00\x00\x00\x4d\x53\x53\x51\x4c\x53\x65\x72\x76\x65\x72\x00\x48\x0f\x00\x00',
'\0\0\0\0\x44\x42\x32\x44\x41\x53\x20\x20\x20\x20\x20\x20\x01\x04\0\0\0\x10\x39\x7a\0\x01\0\0\0\0\0\0\0\0\0\0\x01\x0c\0\0\0\0\0\0\x0c\0\0\0\x0c\0\0\0\x04',
'\x01\xc2\0\0\0\x04\0\0\xb6\x01\0\0\x53\x51\x4c\x44\x42\x32\x52\x41\0\x01\0\0\x04\x01\x01\0\x05\0\x1d\0\x88\0\0\0\x01\0\0\x80\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x08\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x01\0\0\x40\0\0\0\x40\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x02\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\0\0\0\0\x01\0\0\x40\0\0\0\0\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x04\0\0\0\x03\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x08\0\0\0\x01\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x10\0\0\0\x01\0\0\x80\0\0\0\x01\x10\0\0\0\x01\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x80\0\0\0\x01\x04\0\0\0\x03\0\0\x80\0\0\0\x01\0\0\0\0\0\0\0\0\0\0\0\0\x01\x04\0\0\x01\0\0\x80\0\0\0\x01\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x01\0\0\x40\0\0\0\x01\0\0\0\0\x01\0\0\x40\0\0\0\0\x20\x20\x20\x20\x20\x20\x20\x20\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x01\0\xff\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\xe4\x04\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x7f',
'\x41\0\0\0\x3a\x30\0\0\xff\xff\xff\xff\xd4\x07\0\0\0\0\0\0test.$cmd\0\0\0\0\0\xff\xff\xff\xff\x1b\0\0\0\x01serverStatus\0\0\0\0\0\0\0\xf0\x3f\0'
]

SIGNS=[
'http|^HTTP.*',
'ssh|SSH-2.0-OpenSSH.*',
'ssh|SSH-1.0-OpenSSH.*',
'netbios|^\x79\x08.*BROWSE',
'netbios|^\x79\x08.\x00\x00\x00\x00',
'netbios|^\x05\x00\x0d\x03',
'netbios|^\x83\x00',
'netbios|^\x82\x00\x00\x00',
'netbios|\x83\x00\x00\x01\x8f',
'backdoor-fxsvc|^500 Not Loged in',
'backdoor-shell|GET: command',
'backdoor-shell|sh: GET:',
'bachdoor-shell|[a-z]*sh: .* command not found',
'backdoor-shell|^bash[$#]',
'backdoor-shell|^sh[$#]',
'backdoor-cmdshell|^Microsoft Windows .* Copyright .*>',
'db2|.*SQLDB2RA',
'db2jds|^N\x00',
'dell-openmanage|^\x4e\x00\x0d',
'finger|^\r\n    Line      User',
'finger|Line     User',
'finger|Login name: ',
'finger|Login.*Name.*TTY.*Idle',
'finger|^No one logged on',
'finger|^\r\nWelcome',
'finger|^finger:',
'finger|^must provide username',
'finger|finger: GET: ',
'ftp|^220.*\n331',
'ftp|^220.*\n530',
'ftp|^220.*FTP',
'ftp|^220 .* Microsoft .* FTP',
'ftp|^220 Inactivity timer',
'ftp|^220 .* UserGate',
'http|^HTTP/0.',
'http|^HTTP/1.',
'http|<HEAD>.*<BODY>',
'http|<HTML>.*',
'http|<html>.*',
'http|<!DOCTYPE.*',
'http|^Invalid requested URL ',
'http|.*<?xml',
'http|^HTTP/.*\nServer: Apache/1',
'http|^HTTP/.*\nServer: Apache/2',
'http-iis|.*Microsoft-IIS',
'http-iis|^HTTP/.*\nServer: Microsoft-IIS',
'http-iis|^HTTP/.*Cookie.*ASPSESSIONID',
'http-iis|^<h1>Bad Request .Invalid URL.</h1>',
'http-jserv|^HTTP/.*Cookie.*JServSessionId',
'http-tomcat|^HTTP/.*Cookie.*JSESSIONID',
'http-weblogic|^HTTP/.*Cookie.*WebLogicSession',
'http-vnc|^HTTP/.*VNC desktop',
'http-vnc|^HTTP/.*RealVNC/',
'ldap|^\x30\x0c\x02\x01\x01\x61',
'ldap|^\x30\x32\x02\x01',
'ldap|^\x30\x33\x02\x01',
'ldap|^\x30\x38\x02\x01',
'ldap|^\x30\x84',
'ldap|^\x30\x45',
'smb|^\0\0\0.\xffSMBr\0\0\0\0.*',
'msrdp|^\x03\x00\x00\x0b',
'msrdp|^\x03\x00\x00\x11',
'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\x12.\0$',
'msrdp|^\x03\0\0\x17\x08\x02\0\0Z~\0\x0b\x05\x05@\x06\0\x08\x91J\0\x02X$',
'msrdp|^\x03\0\0\x11\x08\x02..}\x08\x03\0\0\xdf\x14\x01\x01$',
'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\x03.\0$',
'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\0\0\0',
'msrdp|^\x03\0\0\x0e\t\xd0\0\0\0[\x02\xa1]\0\xc0\x01\n$',
'msrdp|^\x03\0\0\x0b\x06\xd0\0\x004\x12\0',
'msrdp-proxy|^nmproxy: Procotol byte is not 8\n$',
'msrpc|^\x05\x00\x0d\x03\x10\x00\x00\x00\x18\x00\x00\x00\x00\x00',
'msrpc|\x05\0\r\x03\x10\0\0\0\x18\0\0\0....\x04\0\x01\x05\0\0\0\0$',
'mssql|^\x04\x01\0C..\0\0\xaa\0\0\0/\x0f\xa2\x01\x0e.*',
'mssql|^\x05\x6e\x00',
'mssql|^\x04\x01\x00\x25\x00\x00\x01\x00\x00\x00\x15.*',
'mssql|^\x04\x01\x00.\x00\x00\x01\x00\x00\x00\x15.*',
'mssql|^\x04\x01\x00\x25\x00\x00\x01\x00\x00\x00\x15.*',
'mssql|^\x04\x01\x00.\x00\x00\x01\x00\x00\x00\x15.*',
'mssql|^\x04\x01\0\x25\0\0\x01\0\0\0\x15\0\x06\x01.*',
'mssql|^\x04\x01\x00\x25\x00\x00\x01.*',
'telnet|^xff\xfb\x01\xff\xfb\x03\xff\xfb\0\xff\xfd.*',
'mssql|;MSSQLSERVER;',
'mysql|^\x19\x00\x00\x00\x0a',
'mysql|^\x2c\x00\x00\x00\x0a',
'mysql|hhost \'',
'mysql|khost \'',
'mysql|mysqladmin',
'mysql|whost \'',
'mysql-blocked|^\(\x00\x00',
'mysql-secured|this MySQL',
'mongodb|^.*version.....([\.\d]+)',
'nagiosd|Sorry, you \(.*are not among the allowed hosts...',
'nessus|< NTP 1.2 >\x0aUser:',
'oracle-tns-listener|\(ERROR_STACK=\(ERROR=\(CODE=',
'oracle-tns-listener|\(ADDRESS=\(PROTOCOL=',
'oracle-dbsnmp|^\x00\x0c\x00\x00\x04\x00\x00\x00\x00',
'oracle-https|^220- ora',
'oracle-rmi|\x00\x00\x00\x76\x49\x6e\x76\x61',
'oracle-rmi|^\x4e\x00\x09',
'postgres|Invalid packet length',
'postgres|^EFATAL',
'rlogin|login: ',
'rlogin|rlogind: ',
'rlogin|^\x01\x50\x65\x72\x6d\x69\x73\x73\x69\x6f\x6e\x20\x64\x65\x6e\x69\x65\x64\x2e\x0a',
'rpc-nfs|^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00',
'rpc|\x01\x86\xa0',
'rpc|\x03\x9b\x65\x42\x00\x00\x00\x01',
'rpc|^\x80\x00\x00',
'rsync|^@RSYNCD:.*',
'smux|^\x41\x01\x02\x00',
'snmp-public|\x70\x75\x62\x6c\x69\x63\xa2',
'snmp|\x41\x01\x02',
'socks|^\x05[\x00-\x08]\x00',
'ssh|^SSH-',
'ssh|^SSH-.*openssh',
'ssl|^\x15\x03',
'ssl|^\x16\x03',
'ssl|^\x82\xad',
'ssl|SSL.*GET_CLIENT_HELLO',
'ssl|-ERR .*tls_start_servertls',
'sybase|^\x04\x01\x00',
'telnet|^\xff\xfd',
'telnet|Telnet is disabled now',
'telnet|^\xff\xfe',
'tftp|^\x00[\x03\x05]\x00',
'http-tomcat|.*Servlet-Engine',
'uucp|^login: password: ',
'vnc|^RFB.*',
'webmin|.*MiniServ',
'webmin|^0\.0\.0\.0:.*:[0-9]',
'websphere-javaw|^\x15\x00\x00\x00\x02\x02\x0a']


# convert an IP address from its dotted-quad format to its
# 32 binary digit representation
def ip2bin(ip):
	b = ""
	inQuads = ip.split(".")
	outQuads = 4
	for q in inQuads:
		if q != "":
			b += dec2bin(int(q),8)
			outQuads -= 1
	while outQuads > 0:
		b += "00000000"
		outQuads -= 1
	return b

# convert a decimal number to binary representation
# if d is specified, left-pad the binary number with 0s to that length
def dec2bin(n,d=None):
	s = ""
	while n>0:
		if n&1:
			s = "1"+s
		else:
			s = "0"+s
		n >>= 1
	if d is not None:
		while len(s)<d:
			s = "0"+s
	if s == "": s = "0"
	return s

# convert a binary string into an IP address
def bin2ip(b):
	ip = ""
	for i in range(0,len(b),8):
		ip += str(int(b[i:i+8],2))+"."
	return ip[:-1]

# print a list of IP addresses based on the CIDR block specified
def listCIDR(c):
	cidrlist=[]
	parts = c.split("/")
	baseIP = ip2bin(parts[0])
	subnet = int(parts[1])
	# Python string-slicing weirdness:
	# "myString"[:-1] -> "myStrin" but "myString"[:0] -> ""
	# if a subnet of 32 was specified simply print the single IP
	if subnet == 32:
		print bin2ip(baseIP)
	# for any other size subnet, print a list of IP addresses by concatenating
	# the prefix with each of the suffixes in the subnet
	else:
		ipPrefix = baseIP[:-(32-subnet)]
		for i in range(2**(32-subnet)):
			cidrlist.append(bin2ip(ipPrefix+dec2bin(i, (32-subnet))))
		return cidrlist	

# input validation routine for the CIDR block specified
def validateCIDRBlock(b):
	# appropriate format for CIDR block ($prefix/$subnet)
	p = re.compile("^([0-9]{1,3}\.){0,3}[0-9]{1,3}(/[0-9]{1,2}){1}$")
	if not p.match(b):
		print "Error: Invalid CIDR format!"
		return False
	# extract prefix and subnet size
	prefix, subnet = b.split("/")
	# each quad has an appropriate value (1-255)
	quads = prefix.split(".")
	for q in quads:
		if (int(q) < 0) or (int(q) > 255):
			print "Error: quad "+str(q)+" wrong size."
			return False
	# subnet is an appropriate value (1-32)
	if (int(subnet) < 1) or (int(subnet) > 32):
		print "Error: subnet "+str(subnet)+" wrong size."
		return False
	# passed all checks -> return True
	return True
	
def pinger():
	global pinglist
	while True:
		ip=q.get()
		if platform.system()=='Linux':
			p=Popen(['ping','-c 2',ip],stdout=PIPE)
			m = re.search('(.*)\srecieved', p.stdout.read())
			if m!=0:
				pinglist.append(ip)
		if platform.system()=='Windows':
			p=Popen('ping -n 2 ' + ip, stdout=PIPE)
			m = re.search('TTL', p.stdout.read())
			if m:
				pinglist.append(ip)
		q.task_done()

def scanipport():
	global lock
	while True:
		host,port=sq.get()
		sd=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
		sd.settimeout(TIMEOUT)
		try:
			sd.connect((host,port))
			if options.genlist==True:
				if port not in ipdict:
					ipdict[port]=[]
					ipdict[port].append(host)
				else:
					ipdict[port].append(host)
			else:
				lock.acquire()
				print "%s:%d OPEN" % (host, port)
				lock.release()
			sd.close()
			if options.downpage==True and port in [80,81,1080,8080]:				
				dlpage(ip,port)
		except:
			pass
		sq.task_done()		
	
def scanservice():
	global signs,lock
	while True:
		host,port=sq.get()
		sd=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
		sd.settimeout(TIMEOUT)
		service='Unknown'
		try:
			sd.connect((host,port))
		except:
			sq.task_done()
			continue
		try:
			result = sd.recv(256)
			service=matchbanner(result,signs)
		except:
			for probe in PROBES:
				try:
					sd.close()
					sd=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
					sd.settimeout(TIMEOUT)
					sd.connect((host,port))
					sd.sendall(probe)
				except:
					continue	
				try:
					result = sd.recv(256)
					service=matchbanner(result,signs)
					if service!='Unknown':
						break
				except:
					continue
		if options.genlist==True:
			if service not in ipdict:
				ipdict[service]=[]
				ipdict[service].append(host+':'+str(port))
			else:
				ipdict[service].append(host+':'+str(port))
		else:
			lock.acquire()
			if service!='Unknown':
				print "%s:%d OPEN %s" % (host, port, service)
			else:
				print "%s:%d OPEN" % (host, port)
			lock.release()	
			sd.close()
			if options.downpage==True and service=='http':				
				dlpage(ip,port)

		sq.task_done()	

def prepsigns():
	signlist=[]
	for 	item in SIGNS:
		#print item
		(label,pattern)=item.split('|',2)
		sign=(label,pattern)
		signlist.append(sign)	
	return signlist	
	
def matchbanner(banner,slist):
	for item in slist:
		p=re.compile(item[1])
		if p.search(banner)!=None:
			return item[0]
	return 'Unknown'
	
def dlpage(ip,port):
	global page,lock
	page+='<h1>'+ip+':'+str(port)+'</h1><br>'
	for url in URLS:
		c=httplib.HTTPConnection(ip+':'+str(port))
		c.request('GET','/'+url)
		r=c.getresponse()
		#print url,r.status
		if r.status in [200,301,302,401]:
			if url=='':
				url='Homepage'
			lock.acquire()
			print ip+':'+str(port),url,'exists.','Code:',r.status
			page+='<h2>'+url+'</h2><br>'+r.read()
			lock.release()
		c.close()

	
	
		
if __name__ == "__main__":
	usage="usage: InsightScan.py <hosts[/24|/CIDR]> [start port] [end port] -t threads\n\nExample: InsightScan.py 192.168.0.0/24 1 1024 -t 20"
	parser = OptionParser(usage=usage)
	parser.add_option("-t", "--threads", dest="NUM",help="Maximum threads, default 50")
	parser.add_option("-T", "--timeout", dest="TIMEOUT",help="Scan timeout, per thread")
	parser.add_option("-p", "--portlist", dest="PORTS",help="Customize port list, separate with ',' example: 21,22,23,25 ...")
	parser.add_option("-N", '--noping', action="store_true", dest="noping",help="Skip ping sweep, port scan whether targets are alive or not")
	parser.add_option("-P", '--pingonly', action="store_true", dest="noscan",help="Ping scan only,disable port scan")
	parser.add_option("-S", '--service', action="store_true", dest="service",help="Service detection, using banner and signature")
	parser.add_option("-d", '--downpage', action="store_true", dest="downpage",help="Detects interesting stuff on HTTP ports(80,80,8080), when used with -S , will try all ports with HTTP service. Grab and save to HTML pages if found anything.")
	parser.add_option("-l", '--genlist', action="store_true", dest="genlist",help="Output a list, ordered by port number(service, with -S option),for THC-Hydra IP list")
	parser.add_option("-L", '--genfile', action="store_true", dest="genfile",help="Put the IP list in separate files named by port number(service, with -S option). Implies -l option.\nExample: IPs with port 445 opened will be put into 445.txt")
	(options, args) = parser.parse_args()
	if options.NUM !=None and options.NUM!=0:
		NUM=int(options.NUM)
		print 'Scanning with',NUM,'threads...'
	if options.TIMEOUT != None and int(options.TIMEOUT)!=0:
		TIMEOUT=int(options.TIMEOUT)
	if len(args)<1:
		parser.print_help()
		sys.exit()
	if options.noping== True and options.noscan == True:
		print 'ERROR: Cannot use -N and -P together'
		sys.exit()
	iplist=[]	
	ipaddr=args[0]
	if len(args)==2:
		print 'Must specify end port'
		sys.exit()
	try:
		sk.inet_aton(ipaddr)
		iplist.append(ipaddr)
	except:		
		if not validateCIDRBlock(ipaddr):
			print 'IP address not valid!'
			sys.exit()
		else:
			iplist=listCIDR(ipaddr)
	if len(args)==3:
		startport=int(args[1])
		endport=int(args[2])
		if startport>endport:
			print 'start port must be smaller or equal to end port'
			sys.exit()
		PORTS=[]
		for i in xrange(startport,endport+1):
			PORTS.append(i)
	if options.PORTS!= None:
		PORTS=[int(pn) for pn in options.PORTS.split(',') ]
	global page		
	page=''
#start ping threads
	if options.noping != True:
		print "Scanning for live machines...\n"
		global pinglist
		q=Queue()
		pinglist=[]
		for i in range(NUM):
			t = Thread(target=pinger)
			t.setDaemon(True)
			t.start()	
		
		for ip in iplist:
			q.put(ip)
		q.join()
	else:
		pinglist=iplist
	#print pinglist
	if options.noscan == True:
		for host in pinglist:
			print host
		sys.exit()
	if len(pinglist)==0:
		print 'No live machines detected. Try again with -N switch'
		sys.exit()
	print "Scanning ports...\n"
	sq=Queue()
	lock = threading.Lock()
	if options.service==True:
		global signs
		signs=prepsigns()
	if options.genfile==True:
		options.genlist=True
	if options.genlist==True:
		global ipdict
		ipdict={}
	for i in range(NUM):
		st = Thread(target=scanipport)
		if options.service==True:
			st = Thread(target=scanservice)
		st.setDaemon(True)
		st.start()	
		
	for scanip in pinglist:
		for port in PORTS:			
			sq.put((scanip,port))
	sq.join()
	
	if options.genlist==True:
		for port,iplist in ipdict.items():
			if options.genfile==True:
				 file=open(str(port)+'.txt', "a")
			else:
				print "\n========",port,'========'
				
			for ip in iplist:
				if options.genfile==True:
					file.write(ip+"\n")
				else:	
					print ip
	
	if options.downpage==True and page!='':
		f = open('page.html', 'a')
		f.write(page)
		f.close()
		print 'page dumped to page.html'
		
