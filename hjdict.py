from ..base import *
import requests
from bs4 import BeautifulSoup as bs4
def hjdict_japan(word):
    result = {}
    try:
        url=u'https://dict.hjenglish.com/jp/jc/{word}'.format(word=word)
        get_requests=requests.get(url,timeout=5,headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "upgrade-insecure-requests": "1",
    "referer": "https://dict.hjenglish.com/",
    "cookie": "HJ_UID=b1b80aa2-7817-a147-201a-06ad22414eaa; \
                    HJ_SID=f5d5c06c-b8a5-9710-2c6a-e2ad58ebbcd7; \
                    "
        })#设置超时
        soup=bs4(get_requests.content,'html.parser')
    except:
        return result
    result['pronounce'] = soup.find(
        attrs={'class': 'pronounces'}).span.text
    result['sound'] = soup.find(
        attrs={'class': 'word-audio'}).get('data-src')
    result['simple'] = soup.find(
        attrs={'class': 'simple'}).text
    result['detail'] = str(soup.find(
        attrs={'class': 'detail-groups'}).contents[1])
    result.update()#对result 字典更新
    return result

@register([u'沪江小D', u'hjdict-ja'])#词库名称
class hjdict(WebService):#接口名称
    def __init__(self):
        super(hjdict, self).__init__()#接口名称保持一致
    def _get_from_api(self):
        result=hjdict_japan(self.word)#获取dict
        return self.cache_this(result)

    @export('假名')#功能名称
    def kana_(self):#功能函数
        return self._get_field('pronounce')

    @export('发音')  # 功能名称
    def pronounce_(self):  # 功能函数
        audio_url = self.cache_result("sound")
        filename = u'_hj_{}.mp3'.format(self.word)
        if self.download(audio_url, filename):
            return self.get_anki_label(filename, 'audio')

    @export('简单解释')  # 功能名称
    def simple_(self):  # 功能函数
        return self._get_field('simple')

    @export('详细解释')  # 功能名称
    def detail_(self):  # 功能函数
        return self._get_field(u'detail')
