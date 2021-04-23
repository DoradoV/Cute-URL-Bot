import pyshorteners
import validators

class short:

  def cuttly(self, api, url, short, act = "expand"):
    # Cutt.ly
    if act == "expand":
      return pyshorteners.Shortener(api_key = api, api_url = url).cuttly.expand(short)
    else:
      return pyshorteners.Shortener(api_key = api, api_url = url).cuttly.short(short)

  def tinyurl(self, short, act = "expand"):
    # TinyURL.com
    if act == "expand":
      return pyshorteners.Shortener().tinyurl.expand(short)
    else:
      return pyshorteners.Shortener().tinyurl.short(short)

  def dagd(self, short, act):
    # Da.gd
    if act == "expand":
      return pyshorteners.Shortener().dagd.expand(short)
    else:
      return pyshorteners.Shortener().dagd.short(short)

  def isgd(self, short, act):
    if act == "expand":
      return pyshorteners.Shortener().isgd.expand(short)
    else:
      return pyshorteners.Shortener().isgd.short(short)

  def bitly(self, api, short, act):
    # Bit.ly Free: o_35htgecvam
    if act == "clicks":
      return pyshorteners.Shortener(api_key = api).bitly.total_clicks(short)
    else:
      return pyshorteners.Shortener(api_key = api).bitly.short(short)


  def valid(self, url):
    # Проверка URL на правильность
    if validators.url(url):
      return True
    else:
      return False
