from robot.api.deco import keyword
from urllib import request
from urllib.error import URLError

class ProjectTimeLibrary:
    @keyword('Check Application Status At URL "${url}"')
    def check_application_status(self, url):
        with request.urlopen(url) as f:
            f.getcode()
