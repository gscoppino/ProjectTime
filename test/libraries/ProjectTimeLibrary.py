from robot.api.deco import keyword
from urllib import request

class ProjectTimeLibrary:
    @keyword('Check Application Status At URL "${url}"')
    def check_application_status(self, url):
        http_handler = request.HTTPHandler()
        opener = request.build_opener(http_handler)
        request.install_opener(opener)
        with request.urlopen(url) as f:
            f.getcode()
