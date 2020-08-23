import requests
import json


class Trassir():

    def __init__(self, ip, port, port_video, username, password, verify=True):
        self.url = f'https://{ip}:{port}'
        self.url_video = f'http://{ip}:{port_video}/'
        self.verify = verify
        params = {'password': password, 'username': username}
        r = requests.get(self.url+'/login/', params, verify=self.verify)
        rep = json.loads(r.content)
        self.sid = rep['sid']
   
    def getHealth(self):
        params = {'sid': self.sid}
        r = requests.get(self.url + '/health/', params, verify=self.verify)
        content =r.content.decode('utf-8').split('/')[0]
        return json.loads(content)

    def getChannels(self):
        params = {'sid': self.sid}
        r = requests.get(self.url + '/channels/', params, verify=self.verify)
        content =r.content.decode('utf-8').split('/')[0]
        return json.loads(content)['channels']

    def getToken(self, channel, container, stream, quality=100, framerate=0):
        params = {
            'channel': channel,
            'container': container,
            'quality': quality,
            'stream': stream,
            'framerate': framerate,
            'sid': self.sid}
        r = requests.get(self.url + '/get_video/', params, verify=self.verify)
        rep = json.loads(r.content)
        return rep['token']

    def getVideoUPL(self, channel, quality=100, framerate=0):
        token = self.getToken(channel, 'mjpeg', 'sub', quality, framerate)
        return self.url_video + token

    def getHiVideoUPL(self, channel, quality=100, framerate=0):
        token = self.getToken(channel, 'mjpeg', 'main', quality, framerate)
        return self.url_video + token

    def getJpegUPL(self, channel, quality=100):
        token = self.getToken(channel, 'jpeg', 'sub', quality)
        return self.url_video + token

    def getHiJpegUPL(self, channel, quality=100):
        token = self.getToken(channel, 'jpeg', 'main', quality)
        return self.url_video + token

    def getFlvUPL(self, channel):
        token = self.getToken(channel, 'flv', 'sub')
        return self.url_video + token

    def getHiFlvUPL(self, channel):
        token = self.getToken(channel, 'flv', 'main')
        return self.url_video + token

    def getAuto(self):
        params = {'sid': self.sid}
        r = requests.get(self.url + '/lpr_events/', params, verify=self.verify)
        print(r.content)
        # rep = json.loads(r.content)
        # return rep['token']

