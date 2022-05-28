from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from time import sleep

js = '''return JSON.stringify((function() {
    "use strict";
    let style = `.dot {
        background: red;
        position: absolute;
        width: 15px;
        height: 15px;
        z-index: 10000;
        }`;
    let retoto = "";
    var styleSheet = document.createElement("style");
    styleSheet.innerText = style;
    document.head.appendChild(styleSheet);
    // document.onclick = handleMouseMove;
    document.onmousemove = handleMouseMove;

    function handleMouseMove(event) {
      var dot, eventDoc, doc, body, pageX, pageY;
      console.log(event);
        retoto = event 

      event = event || window.event; // IE-ism
      
      // If pageX/Y aren't available and clientX/Y
      // are, calculate pageX/Y - logic taken from jQuery
            // Calculate pageX/Y if missing and clientX/Y available
      if (event.pageX == null && event.clientX != null) {
        eventDoc = (event.target && event.target.ownerDocument) || document;
        doc = eventDoc.documentElement;
        body = eventDoc.body;

        event.pageX = event.clientX +
          (doc && doc.scrollLeft || body && body.scrollLeft || 0) -
          (doc && doc.clientLeft || body && body.clientLeft || 0);
        event.pageY = event.clientY +
          (doc && doc.scrollTop  || body && body.scrollTop  || 0) -
          (doc && doc.clientTop  || body && body.clientTop  || 0 );
      }

      // Add a dot to follow the cursor
      dot = document.createElement('div');
      dot.className = "dot";
      dot.style.left = event.pageX + "px";
      dot.style.top = event.pageY + "px";
      document.body.appendChild(dot);
    }
    return retoto
  })());'''
class Web_testing:
    def __init__(self, url):
        self.images = []
        self.urls = [url]
        self.linkstmp = []
        self.links = []
        chrome_options = Options()
        self.driver = webdriver.Chrome('/Users/hugoalberola/Documents/ecole/entreprenaria/computer-vision-api/service/chromedriver')
        self.driver.get(url)
        self.actions = ActionChains(self.driver)
    # def handlecookie(self): 
            # break 
    def start(self,methode):
        for increment, url in enumerate(self.urls):
            self.increment = increment
            methode()
            print('url :',url)
            self.links =  self.links + list(map(lambda value: {"source":url,"target":value},self.linkstmp))
            self.linkstmp = []
        print(self.urls)
        # print(self.links)
        self.driver.close()
        return self.links
      
    def url_append(self, url):
      # print(url.split("/"))
      if(url not in self.urls and len(url.split("/")) >= 3 ):
        if(url.split("/")[2] == self.urls[0].split("/")[2] and len(url.split("/")[-1].split("."))<2):
            self.urls.append(url)
      if(url not in self.linkstmp):
          self.linkstmp.append(url)
# driver = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities=DesiredCapabilities.CHROME)





# print(driver.execute_script('return document.elementFromPoint(18,155).outerHTML'))
# actions.move_to_element_with_offset(driver.findElement('body'), 0,0)



# print(driver.current_url)
# driver.close()
# "var rect = elem.getBoundingClientRect(); console.log(rect.top, rect.right, rect.bottom, rect.left);"