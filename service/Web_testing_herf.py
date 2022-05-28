from mimetypes import init

from service.Web_testing import Web_testing
from service.wait_wraper import wait_wrapper

class Web_testing_herf(Web_testing):
    def __init__(self,url):
        super().__init__(url)
    def geturls(self):
        elems = self.driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            self.url_append(wait_wrapper(elem.get_attribute,"href"))    
        self.driver.get(self.urls[self.increment])
