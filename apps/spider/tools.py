import html5lib
import lxml
import lxml.cssselect
import urllib2
import tempfile
import hashlib
import Image
import os

from django.conf import settings
from django.core.files import File


if not os.path.exists(settings.PROXY_ROOT):
    os.makedirs(settings.PROXY_ROOT)


def clean_proxy():
    for the_file in os.listdir(settings.PROXY_ROOT):
        try:
            os.unlink(os.path.join(settings.PROXY_ROOT, the_file))
        except:
            pass


class WebPage():

    def __init__(self, url):
        self.url = url
        self.htmlparser = html5lib.HTMLParser(
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),
            namespaceHTMLElements=False
            )
        self.request = urllib2.Request(url)
        self.request.add_header("User-Agent",
                                "Mozilla/5.0 (X11; U; Linux x86_64; fr; " \
                                "rv:1.9.1.5) Gecko/20091109 Ubuntu/9.10 " \
                                "(karmic) Firefox/3.5.5")

    def download(self):
        try:
            self.response = urllib2.urlopen(self.request)
            self.html = self.htmlparser.parse(self.response)
            return True
        except:
            return False

    def getByCss(self, selector, source=None):
        selector = lxml.cssselect.CSSSelector(selector)
        if source is not None:
            return selector(source)
        return selector(self.html)


class YoyaFile():

    def __init__(self, url):
        self.tmp_file = None
        fname = os.path.splitext(url)
        self.file_original_name = os.path.basename(fname[0])
        if len(fname) > 1:
            self.file_ext = fname[1]
            if len(self.file_ext) > 4:
                if 'gif' in self.file_ext:
                    self.file_ext = '.gif'
                if 'jpeg' in self.file_ext:
                    self.file_ext = '.jpg'
                if 'jpg' in self.file_ext:
                    self.file_ext = '.jpg'
                if 'png' in self.file_ext:
                    self.file_ext = '.png'
        else:
            self.file_ext = '.jpg'

    def getFileName(self, original=''):
        if original:
            valid_chars = '_abcdefghijklmnopqrstuvwxyzABCD' \
                          'EFGHIJKLMNOPQRSTUVWXYZ0123456789'
            original = original.replace(' ', '_')
            return ''.join(c for c in original
                           if c in valid_chars)[:16] + self.file_ext
        else:
            return os.path.basename(self.tmp_file.name)

    def getFile(self):
        return File(self.tmp_file)

    def getHexFileName(self):
        return str(hashlib.md5(self.tmp_file.name) \
                   .hexdigest()[:16]) + self.file_ext

    def close(self):
        self.tmp_file.close()


class ProxyFile(YoyaFile):

    def __init__(self, file_name):
        YoyaFile.__init__(self, file_name)
        try:
            self.tmp_file = open(os.path.join(settings.PROXY_ROOT,
                                              file_name), 'r')
        except:
            raise Exception("File '%s' doesn't exist in the proxy." %
                                                                    file_name)


class DownloadFile(YoyaFile):

    def __init__(self, url, to_proxy=False):
        self.url = url
        self.proxy = to_proxy
        YoyaFile.__init__(self, url)
        self.tmp_dir = tempfile.gettempdir()

    def download(self):
        if self.proxy:
            self.tmp_file = open(os.path.join(settings.PROXY_ROOT,
                                              self.file_original_name
                                               + self.file_ext), 'w')
        else:
            self.tmp_file = tempfile.NamedTemporaryFile()
        self.tmp_file.write(urllib2.urlopen(self.url).read())

    def cropForKwejk(self, fname):
        im = Image.open(fname)
        box = (0, 0, im.size[0], im.size[1] - 40)
        region = im.crop(box)
        region.save(fname)
