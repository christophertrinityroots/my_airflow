# -*- coding: utf-8 -*-
import requests

def lineNotify(message, token):
    payload = {'message':message}
    return _lineNotify(payload, token)

def notifyFile(filename, token):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message': 'test'}
    return _lineNotify(payload, token, file)

def notifyPicture(url, token):
    payload = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
    return _lineNotify(payload, token)

def notifySticker(stickerID,stickerPackageID, token):
    payload = {'message':" ",'stickerPackageId':stickerPackageID,'stickerId':stickerID}
    return _lineNotify(payload, token)

def _lineNotify(payload, token, file=None):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization':'Bearer ' + token}
    return requests.post(url, headers=headers , data=payload, files=file)

# notifyFile('./logo.png')
# lineNotify('ทดสอบภาษาไทย hello')
# notifySticker(40,2)
# notifyPicture("https://www.honey.co.th/wp-content/uploads/2017/03/cropped-logo_resize.png")