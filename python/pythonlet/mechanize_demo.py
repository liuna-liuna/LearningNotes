#!/usr/bin/env python
# -*- coding: utf-8 -*-

# title         : mechanize demo
# description   : n.a
# author        : liuna
# version       : 0.1
# usage         : python mechanize_demo.py
# date          : 2017-11-07
# notes         : n.a
# python version: 2
# ================================================================================
# imports
import mechanize
import cookielib

# consts
URL_BAIDU = 'https://www.baidu.com'
URL_IMG_URL_BAIDU = 'https://www.baidu.com/img/bd_logo1.png'
URL_REGEX_BAIDU = 'baidu.com'

# functions
pass

# class
class MechanizeDemo(object):
    def __init__(self, url=URL_BAIDU, img_url=URL_IMG_URL_BAIDU):
        self.url = url
        self.img_url = img_url

    def emulate_browser(self):
        def create_browser():
            # Browser
            br = mechanize.Browser()
    
            # Cookie Jar
            cj = cookielib.LWPCookieJar()
            br.set_cookiejar(cj)
    
            # Browser options
            br.set_handle_equiv(True)
            br.set_handle_gzip(True)
            br.set_handle_redirect(True)
            br.set_handle_referer(True)
            br.set_handle_robots(False) # 设置对方网站的robots.txt是否起作用
    
            # Follows refresh 0 but not hangs on refresh > 0
            br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
            # for Debugging
            # br.set_debug_http(True)
            # br.set_debug_redirects(True)
            # br.set_debug_responses(True)
    
            # User-Agent
            br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) \
                              AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50')]
    
            return br

        def open_page(br, url):
            # open one site
            # if authentication necessary,
            # br.add_password(site, username, password)
            resp = br.open(url)
            return resp

        def print_page(br, resp):
            html = resp.read()
    
            # show title
            print br.title()
    
            # show the source
            # print html                 # or print br.response().read()       # too long
            print len(html)              # or print br.response().read()
    
            # show the response headers
            print resp.info()       # or print br.response().info()

            # pause by waiting for any-key input
            raw_input()
    
            # show the available forms
            for f in br.forms():
                print f.name
    
            # select the first form: index == 0
            br.select_form(nr=0)
    
            # will fail when the form is read-only
#            # let's search
#            br.form['f'] = 'weekend codes'  # hard code form name 'f' here
#            br.submit()
#            print br.response().read()
    
            # look at some results in link formats
            for l in br.links(url_regex=URL_REGEX_BAIDU):
                print l
                # manage browser history, make sure it not hangs
                # br.follow_link(l)       # 接受 link对象 或者 参数列表 
                # br.back()

            # pause by waiting for any-key input
            raw_input()

        def download_image(br, img_url):
            f = br.retrieve(img_url)[0]
            print f
            with open(f) as fh:
                content = fh.read()
            # print content     # too long

            # pause by waiting for any-key input
            raw_input()

            print len(content)

        # main steps in emulate_browser
        self.browser = create_browser()
        self.response = open_page(self.browser, self.url)
        print_page(self.browser, self.response)
        download_image(self.browser, self.img_url)


# main entry
if __name__ == '__main__':
    md = MechanizeDemo()
    md.emulate_browser()


