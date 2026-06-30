from urllib.request import Request, urlopen
from html.parser import HTMLParser


class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()


url = "https://open.spotify.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

req = Request(url, headers=headers)

with urlopen(req, timeout=10) as response:
    html = response.read().decode("utf-8", errors="ignore")

print("网页前 500 个字符：")
print(html[:500])

parser = TitleParser()
parser.feed(html)

print("\n网页标题：")
print(parser.title)