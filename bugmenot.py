#!/usr/bin/env python
#coding=utf-8
# vim: set filetype=python ts=4 sw=4 sts=4 noexpandtab :

'''
Get username and password from http://www.bugmenot.com/

File: bugmynot.py
Author: notsobad.me 
Description:
Created: 2009-11-09 15:23:41
Last modified: 2010.11.25

'''

import urllib2, re, pprint
import os,sys,traceback,optparse

class BugMeNot:
	def __init__(self):
		pass

	def _get_account(self, host):
		headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache'      
		}

		try:
			urlOpener = urllib2.build_opener()

			request = urllib2.Request('http://www.bugmenot.com/view/%s?utm_source=extension&utm_medium=firefox' % host , None, headers)

			page = urlOpener.open(request).read(50000) # Log in BugMeNot
		except (urllib2.HTTPError, urllib2.URLError):
			print >> sys.stderr, 'Http Error! Please check the url you input and the network connection'
			sys.exit(2)

		re_loginpwd = re.compile(u'<tr><th>Username </th><td>(.+?)</td></tr>[^<]+?<tr><th>Password </th><td>([^<]*)</td></tr>',re.IGNORECASE|re.DOTALL)

		match =  re_loginpwd.findall(page)
		#return [(i, j) for i, j in match if i and j and len(i) < 30]
		return [{'username':i, 'password':j} for i, j in match if i and j and len(i) < 30]
	
	def get_account(self, host):
		return self._get_account(host)


if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option("-s", "--site", dest = "site",help = "The target site")
	parser.add_option("-t", "--ret_type", dest="ret",default="text", help="The return type(text/json)")

	(options, args) = parser.parse_args()

	if options.site:
		bug = BugMeNot()
		accounts = bug.get_account(options.site)
		if not accounts:
			print "No accounts/password for %s found in www.bugmenot.com" % options.site
			sys.exit(1)

		if options.ret == 'text':
			print "%-30s\t%-20s" % ("Username", "Password")
			print "-" * 50
			for account in accounts:
				print "%(username)-30s\t%(password)-20s" % account
		elif options.ret == 'json':
			import json
			print json.dumps(accounts)
	else:
		parser.print_help()
		sys.exit(1)

	sys.exit(0)

