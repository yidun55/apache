#!/usr/bin/env python
#coding: utf-8

import sys
import urllib
from json import dump
import codecs

reload(sys)
sys.setdefaultencoding("utf-8")

#a = """10.1.80.81 - - [10/May/2016:00:00:01 +0800] "POST /probe/ mobile_json=%7B%22ip%22%3A%2259.38.67.245%22%2C%22appid%22%3A%22kawboynq5oxwp3q2e61v8m1tqwruwb9hhly4vzda7t4wv0i2i%22%2C%22device%22%3A%7B%22resolution%22%3A%22750+x+1334%22%2C%22mc%22%3A%2202%3A00%3A00%3A00%3A00%3A00%22%2C%22iid%22%3A%22F17AyiKgwpw4QlPFugmg8K36Q6h4ELn9%22%2C%22timezone%22%3A%228%22%2C%22carrier%22%3A%22%5Cu4e2d%5Cu56fd%5Cu79fb%5Cu52a8%22%2C%22sv%22%3A%222.1.0.3050%22%2C%22package_name%22%3A%22com.lakala.shanghutong%22%2C%22os%22%3A%22iOS%22%2C%22access%22%3A%22WiFi%22%2C%22language%22%3A%22zh-Hans-CN%22%2C%22device_model%22%3A%22iPhone8%2C1%22%2C%22channel%22%3A%22App+Store%22%2C%22display_name%22%3A%22shanghutong%22%2C%22app_version%22%3A%222.1.0%22%2C%22sdk_version%22%3A%22v2.6.7%22%2C%22os_version%22%3A%229.0.2%22%2C%22is_jailbroken%22%3Afalse%2C%22device_id%22%3A%229A6AA6D5-044F-4C06-89B7-6E2DD9F8E755%22%7D%2C%22events%22%3A%7B%22event%22%3A%5B%5D%2C%22launch%22%3A%7B%22date%22%3A1.462809539826625E12%2C%22sessionId%22%3A%22z1MeQqrPCP4LQJ5mZyGFFDlZ03OVKJw8%22%7D%2C%22terminate%22%3A%7B%22activities%22%3A%5B%5D%2C%22sessionId%22%3A%22z1MeQqrPCP4LQJ5mZyGFFDlZ03OVKJw8%22%2C%22duration%22%3A61924%7D%7D%7D HTTP/1.1" 200 1150 "-" "/probe/"   "/home/www" "Apache-HttpClient/4.2.5 (java 1.5)" """
#aDecoded = urllib.unquote(a)

def find_json(line_str):
    """
    pick out json from line
    """
    assert type(line_str) == str, "line_str must be string"
    stack = []
    start = 0
    end = 0 
    for value, key in enumerate(line_str):
        if key == u"{":
            stack.append(value)
        elif key == u"}":
            if len(stack) == 0:
                break
            else:
                start = stack.pop()
                end = value
    if start != end and start != 0:
        json_str = line_str[start:end + 1]
        try:
            false = False
            true = True
            return eval(json_str)
        except:
            pass

def pick_field(input_dict):
    """
    process json to string
    appid,ip,device,events_launch,events_terminate,events_event       
    """
    type(input_dict) == dict,"input_dict must be dict"
    fields = ["appid", "ip", "device", "events_launch",\
            "events_terminate", "events_event"]
    t = input_dict
    try:
        length = len(t['events']['event'])
    except KeyError,e:
        t['events'].update({'event':[]})
        length = len(t['events']['event'])

    flag = True
    tmp_all = []
    for i in xrange(0, length+1):
        tmp = []
        for field in fields:
            if field == "events_event":
                try:
                    tmp.append(t["events"]["event"][i])
                    flag = False 
                except IndexError:
                    if flag == False:   #not the first time
                        tmp = []
                        break
                    else:
                        tmp.append("")
                except:
                    tmp = []
                    break

            elif field.count("_")==1:
                fTmp = field.split("_")
                tmp.append(t[fTmp[0]][fTmp[1]])
            else:
                tmp.append(t[field])
        if  len(tmp) != 0:
            oStr = "\001".join([str(i) for i in tmp]).decode("unicode_escape")
            tmp_all.append(oStr)
    reStr = "\n".join(tmp_all)
    if reStr != None:
        return reStr


#urllib.unquote(sys.stdin)

if __name__ == '__main__':
    path = "E:/deny/ML/python/xiaodai/20160513_mobile-access-log_.1463137199455.tmp"
    # path = "C:/Users/yn/Desktop/writeJson.txt"
    f = open(path, "r")
    # f.next()
    # line = f.next()
    # print "fdsfj",line, "dfsafds"
    # for line in sys.stdin:
    i = 0
    for line in f:
        stdinput = urllib.unquote(line)
        # print stdinput
        json = find_json(stdinput)
        if json!=None:                   #filter out None
            a = pick_field(json).decode("unicode_escape")
            # print a
            if a!=None:
                i += 1
    print i



