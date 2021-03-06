#-*- coding: utf-8 -*-
import urllib, urllib2
import StringIO, gzip
# to require bs4
from bs4 import BeautifulSoup
# to read xls file
from xlrd import open_workbook


xls = open_workbook('test.xls')
sheet0 = xls.sheet_by_index(0)

#to write in xls file
from tempfile import TemporaryFile
from xlwt import Workbook
        
book = Workbook()
sheet1 = book.add_sheet('result 1', cell_overwrite_ok=True) 

import re
#import time

for row_index in range(sheet0.nrows):

#    time.sleep(0.7)
    keyword = sheet0.cell(row_index,0).value
    params = {'q' : keyword, 'hl' : 'ko'}
    enc_params = urllib.urlencode(params)
    
    request = urllib2.Request('http://sky-kpkr.sandbox.google.com/'+'search'+'?'+enc_params)
    #user-agent 모바일로 변경
    request.add_header('User-agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    compressedstream = StringIO.StringIO(response.read())
    gzipper = gzip.GzipFile(fileobj=compressedstream)

    data = gzipper.read()
    soup = BeautifulSoup(data)
          
    sandbox = soup.find_all(id="kno-result")      
    #class = "kno-sh ellip" : 함께 찾은 검색어도 minibox에 들어가버림
    onebox = soup.find_all(class_="g ssr noknav")
    #q="은교"의 경우, onebox가 SRP 하단에 위치함.
    #q="표어 뜻"의 경우, class="g tpo"로 li tag로 출력됨.
    #q="millinery"의 경우, class="head" 이지만 구분기준은 되기 어려움.
    
    
    # sandbox & onebox, 또는 onebox & topstuff, 또는 topstuff & sandbox, 또는 sandbox & onebox & topstuff 일 경우에 모두 박스 종류값을 리턴해줘야한다.
    # 고민 중
    
    if sandbox:
        sheet1.write(row_index, 1, "kp")
        print "y"
    elif onebox:
        sheet1.write(row_index, 1, "srs")
        print "y"
    else: 
        #nobox
        sheet1.write(row_index, 1, "0")
        print "n"
        
book.save('google_result.xls')    
    

    
    
   
