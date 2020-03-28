#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests

def lineNotify(message):
    payload = {'message':message}
    return _lineNotify(payload)

def notifyFile(filename):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message': 'test'}
    return _lineNotify(payload,file)

def notifyPicture(url):
    payload = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
    return _lineNotify(payload)

def notifySticker(stickerID,stickerPackageID):
    payload = {'message':" ",'stickerPackageId':stickerPackageID,'stickerId':stickerID}
    return _lineNotify(payload)

def _lineNotify(payload,file=None):
    url = 'https://notify-api.line.me/api/notify'
    token = 'obRD3hjMQQsCiYHYtECjmHYel6fD3CaqNwpI9aavMcm'
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data=payload, files=file)

# notifyFile('./logo.png')
lineNotify('ทดสอบภาษาไทย hello')
notifySticker(40,2)
notifyPicture("https://www.honey.co.th/wp-content/uploads/2017/03/cropped-logo_resize.png")