"""
@file fakes.py
@brief Test-Doubles für yt_dlp.YoutubeDL (kein Netzwerkzugriff).
"""


class FakeYDL:
    """
    @brief Ersetzt YoutubeDL; zeichnet Aufrufe auf und liefert feste Ergebnisse.
    """

    instances: list["FakeYDL"] = []
    retcode = 0
    info = None

    def __init__(self, opts):
        self.opts = opts
        self.urls = []
        self.post_processors = []
        FakeYDL.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def add_post_processor(self, pp, when):
        self.post_processors.append((pp, when))

    def download(self, urls):
        self.urls.extend(urls)
        return self.retcode

    def extract_info(self, url, download=False):
        return self.info

    @classmethod
    def reset(cls, retcode=0, info=None):
        cls.instances = []
        cls.retcode = retcode
        cls.info = info
