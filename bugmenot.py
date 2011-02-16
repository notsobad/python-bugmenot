#!/usr/bin/env python
#coding=utf-8
# vim: set filetype=python ts=4 sw=4 sts=4 expandtab autoindent :

'''
Get username and password from http://www.bugmenot.com/

File: bugmynot.py
Author: notsobad.me
Description:
Created: 2009-11-09 15:23:41
Last modified: 2010.11.25
'''

import optparse
import sys
import urllib2
import re


class BugMeNot:
    def __init__(self):
        self.regex = u'<tr><th>Username </th><td>([^<]*)</td></tr>'
        self.regex += u'[^<]+?<tr><th>Password </th><td>([^<]*)</td></tr>'
        self.regex += u'[^<]+?<tr><th>Other</th><td>([^<]*)</td></tr>'
        self.regex += u'[^<]+?<tr><th>Stats</th><td class="stats"><em class="[^"]*">([0-9]*%)[^<]*</em>[^<]*</td></tr>'

    def _get_account(self, host):
        headers = dict()
        headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
        headers['Pragma'] = 'no-cache'
        headers['Cache-Control'] = 'no-cache'

        try:
            urlOpener = urllib2.build_opener()

            request = urllib2.Request('http://www.bugmenot.com/view/%s?utm_source=extension&utm_medium=firefox' % host, None, headers)

            page = urlOpener.open(request).read(50000)  # Log in BugMeNot
        except (urllib2.HTTPError, urllib2.URLError):
            print >> sys.stderr, 'Http Error! Please check the url you input and the network connection'
            sys.exit(2)

        re_loginpwd = re.compile(self.regex, re.IGNORECASE | re.DOTALL)

        match = re_loginpwd.findall(page)
        #return [(i, j) for i, j in match if i and j and len(i) < 30]
        return [{'username':i, 'password':j, 'other':o, 'stats':s} for i, j, o, s in match if i and j and len(i) < 30]

    def get_account(self, host):
        return self._get_account(host)


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option("-e", "--extended_info", dest="extended_info",
            action="store_true", default=False, help="Show extended info in the text mode")
    parser.add_option("-s", "--site", dest="site", help="The target site")
    parser.add_option("-t", "--ret_type", dest="ret", default="text", help="The return type(text/json)")

    (options, args) = parser.parse_args()

    if options.site:
        bug = BugMeNot()
        accounts = bug.get_account(options.site)
        if not accounts:
            print "No accounts/password for %s found in www.bugmenot.com" % options.site
            sys.exit(1)

        if options.ret == 'text':
            print "%-30s\t%-20s" % ("Username", "Password"),
            line_len = 30 + 20
            if options.extended_info:
                print "\t%-25s\t%-5s" % ("Other", "Stats"),
                line_len += 25 + 20

            print "\n", "-" * line_len
            for account in accounts:
                print "%(username)-30s\t%(password)-20s" % account,
                if options.extended_info:
                    print "\t%(other)-25s\t%(stats)-5s" % account,
                print
        elif options.ret == 'json':
            import json
            print json.dumps(accounts)
    else:
        parser.print_help()
        sys.exit(1)

    sys.exit(0)
