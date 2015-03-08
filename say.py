# -*- coding: utf-8 -*-
import sys
import base64
import urllib2
import json
import platform
import subprocess
 
# service URL
tts_url ='http://rospeex.ucri.jgn-x.jp/nauth_json/jsServices/VoiceTraSS'
 
# main 
if __name__=='__main__':
    # args
    argv = sys.argv[1:]

    # command
    tts_command = { "method":"speak",
    "params":["1.1",
    {"language":"ja","text":argv,"voiceType":"*","audioType":"audio/x-wav"}]}
  
    obj_command = json.dumps(tts_command)     # string to json object
    req = urllib2.Request(tts_url, obj_command)
    received = urllib2.urlopen(req).read()    # get data from server
     
    # extract wav file 
    obj_received = json.loads(received)
    tmp = obj_received['result']['audio'] # extract result->audio
    speech = base64.decodestring(tmp.encode('utf-8'))
 
    f = open ("out.wav",'wb')
    f.write(speech)
    f.close

    # pi: mpalyerコマンド, mac:afplayコマンドを使用
    p = platform.system()
    c = "mplayer"
    if p == "Darwin":
        c = "afplay"

    # play
    args = [c,"out.wav"]
    subprocess.call(args)

    # rm tmp wav file
    args = ["rm","out.wav"]
    subprocess.call(args)
