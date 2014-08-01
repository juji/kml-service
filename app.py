#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
import urlparse
import re
import urllib
import cgi


def application(environ, start_response):
    query = urlparse.parse_qs(environ['QUERY_STRING'])
    status = '200 OK'

    default = {'ll':'0,0'}

    response_headers = [('Content-type','text/plain')]
#    start_response(status, response_headers)
#    return [pprint.pformat(environ,indent=10)+'\n']
#'''
    if 'll' not in query:
    	status = '400 Bad Request'
    	start_response(status, response_headers)
    	return ['Latitude and Longitude is empty\n']

    default['ll'] = urllib.unquote(query['ll'][0])
    default['ll'] = re.sub('^([^,]+),(.*?)$',r'\2,\1',default['ll'])

    default['name'] = urllib.unquote(query['n'][0]) if 'n' in query else ''
    default['name'] = cgi.escape(urllib.unquote(default['name']), quote=True)
    default['description'] = urllib.unquote(query['d'][0]) if 'd' in query else ''
    default['icon'] = urllib.unquote(query['i'][0]) if 'i' in query else 'https://goo.gl/59ScNx'

	#breaks
    default['description'] = re.sub('(\r\n|\n|\r)','<br />',default['description'])
	#url
    default['description'] = re.sub('(\s|^|>)(([a-z,A-Z,0-9]+\.)+[a-z,A-Z,0-9]+)(\s|<|$)',r'\1<a href="http://\2">\2</a>\4',default['description'])
    default['description'] = re.sub('(\s|^|>)(http\:\/\/[^\s<]+)(\s|<|$)',r'\1<a href="\2">\2</a>\3',default['description'])
    default['description'] = re.sub('(\s|^|>)(https\:\/\/[^\s<]+)(\s|<|$)',r'\1<a href="\2">\2</a>\3',default['description'])
    default['description'] = re.sub('(\s|^|>)([^\/>\@\s]+\@([^\.\s\<]+\.)+\w+)(\s|<|$)',r'\1<a href="mailto://\2">\2</a>\4',default['description'])

    default['name'] = '\n\t<name>{}</name>'.format(default['name']) if default['name'] else ''
    default['description'] = '\n\t<description><![CDATA[\n<br />{}\n]]></description>\n'.format(default['description']) if default['description'] else ''

    resp = """
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.google.com/earth/kml/2">
	<Document>
	<name>dinamickml.kml</name>
	<Style id="iconStyle">
      <IconStyle>
        <Icon>
          <href>{0!s}</href>
        </Icon>
        <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />
      </IconStyle>
    </Style>
  <Placemark>{1!s}{2!s}
    <styleUrl>#iconStyle</styleUrl>
    <Point>
      <coordinates>{3!s}</coordinates>
    </Point>
  </Placemark>
  </Document>
</kml>
"""[1:-1].format(default['icon'],default['name'],default['description'],default['ll'])

    start_response(status, response_headers)
    return [resp+'\n']
#'''
