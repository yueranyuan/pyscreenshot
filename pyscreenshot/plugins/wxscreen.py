from PIL import Image
import logging

log = logging.getLogger(__name__)

class WxScreen(object):

    '''based on: http://stackoverflow.com/questions/69645/take-a-screenshot-via-a-python-script-linux
    '''
    name = 'wx'
    childprocess = False

    def __init__(self):
        import wx
        self.wx = wx
        self.app = None

    def grab(self, bbox=None):
        wx = self.wx
        if not self.app:
            self.app = wx.App()
        screen = wx.ScreenDC()
        size = screen.GetSize()
        if bbox is None:
            bbox = [0, 0, size[0], size[1]]
        x, y, w, h = bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]
        if wx.__version__ >= '4':
            bmp = wx.Bitmap(w, h)
        else:
            bmp = wx.EmptyBitmap(w, h)
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, w, h, screen, x, y)
        del mem
        if hasattr(bmp, "ConvertToImage"):
            myWxImage = bmp.ConvertToImage()
        else:
            myWxImage = wx.ImageFromBitmap(bmp)
        im = Image.new('RGB', (myWxImage.GetWidth(), myWxImage.GetHeight()))
        if hasattr(Image, 'frombytes'):
            # for Pillow
            im.frombytes(buffer(myWxImage.GetData()))
        else:
            # for PIL
            im.fromstring(myWxImage.GetData())
        return im

    def grab_to_file(self, filename, bbox=None):
        # bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
        im = self.grab(bbox)
        im.save(filename)

    def backend_version(self):
        return self.wx.__version__
