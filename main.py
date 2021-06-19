import requests,json,qrcode,time,base64
from PIL import Image

def Bili_Login() :
    response = requests.get("http://passport.bilibili.com/qrcode/getLoginUrl").json()
    response = response['data']
    oauthKey = response['oauthKey']
    print(oauthKey)
    img = qrcode.make(response['url'])
    img.save('test.png')
    img.show()
    response = requests.post("http://passport.bilibili.com/qrcode/getLoginInfo",data = {'oauthKey':oauthKey}).json()
    #print(response['data'])
    response = requests.post("http://passport.bilibili.com/qrcode/getLoginInfo",data = {'oauthKey':oauthKey})
    DataJson = response.json()
    while DataJson['data'] == -4 or DataJson['data'] == -5:
        time.sleep(1)
        response = requests.post("http://passport.bilibili.com/qrcode/getLoginInfo",data = {'oauthKey':oauthKey})
        DataJson = response.json()
        print("waiting for a scan...")


    while DataJson['data'] == -1:
        #密钥错误
        print("an error occured...program gonna exit...")


    while DataJson['data'] == -2:
        #密钥超时
        print("time out...")
        return -2
        break

    cookie = requests.utils.dict_from_cookiejar(response.cookies)
    return cookie
    
def GetInfo(cookie) :
    res = requests.get("http://api.bilibili.com/x/web-interface/nav",cookies = cookie).json()
    return res

def UploadImage(file,cookie) :


    files = {'file_up':('pic.png',open(file,'rb'),'image/png')}
    data = {'category':'daily'}
    res = requests.post("http://api.vc.bilibili.com/api/v1/drawImage/upload",data = data,files = files,cookies = cookie).json()
    if res['code'] == 0 :
        res = res['data']
        return res['image_url']
    else :
        return res['code']


cookie = Bili_Login()
UploadImage("test.png", cookie)
