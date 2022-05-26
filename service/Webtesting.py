from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import numpy as np
from io import BytesIO
from PIL import Image
from service.OcrModel import OcrModel
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
class Webtesting:
    def __init__(self, url):
        self.images = []
        self.urls = [url]
        self.linkstmp = []
        self.links = []
        chrome_options = Options()
        self.windows__y__size = 768
        self.driver = webdriver.Chrome('/Users/hugoalberola/Documents/ecole/entreprenaria/computer-vision-api/service/chromedriver')
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, self.windows__y__size)
        self.driver.get(url)

        self.actions = ActionChains(self.driver)
    # def handlecookie(self):
        
    def ocr_apply(self,):
        print(self.driver.execute_script('return "toto"'))
        self.driver.save_screenshot("./service/img/test.png")
        self.actions.move_by_offset(15,15).click().perform()
        print(self.driver.get_window_size())
        img = Image.open("./service/img/test.png")
        img = img.resize((1024, self.windows__y__size), Image.ANTIALIAS)
        image = np.asarray(img.convert('RGB'))
        texts, boxes = OcrModel().read_text(image)
        # top = boxes[texts.index('Tout accepter')][0][0]
        # left = boxes[texts.index('Tout accepter')][0][1] 
        # self.driver.execute_script("document.elementFromPoint("+str(top)+", "+str(left)+")?.click()")
        print(texts)
        for id,boxe in enumerate(boxes):
            # print(self.driver.execute_script(js))
            result = boxe[1][0] - boxe[0][0]
            result1 = boxe[1][1] - boxe[0][1]
            # top = boxe[0][0] + int(result/3)
            # left = boxe[0][1] + int(result1/3)
            top = boxe[0][0] +10
            left = boxe[0][1] +10
            target = [top,left]
            sleep(1)
            print("test")
            print(texts[id])
            try:
              self.driver.execute_script("document.elementFromPoint(arguments[0], arguments[1])?.click()",str(top),str(left))
            except:
              print('An exception occurred')
            # self.driver.execute_script(js)
            # self.actions.move_by_offset(target[0],target[1]).click().perform()
            if(self.driver.current_url not in self.urls and self.driver.current_url.split("/")[2] == self.urls[0].split("/")[2]):
                print(self.driver.current_url)
                self.urls.append(self.driver.current_url)
                self.linkstmp.append(self.driver.current_url)
            sleep(1)
            self.driver.get(self.urls[self.increment])
            self.driver.execute_script("window.scrollTo(0, arguments[0]);", self.scrollY) 
            # self.actions.move_by_offset(-target[0],-target[1]).perform()
    def scroll(self):
        last_height = self.driver.execute_script("return window.scrollY;")
        self.scrollY = last_height
        self.ocr_apply() 
        while True:
            sleep(1)
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, arguments[0]);", self.scrollY) 
            # Wait to load page
            self.scrollY += self.scrollY
            sleep(1)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return window.scrollY;")
            if new_height == last_height:
                break
            last_height = new_height
            self.ocr_apply()  
            # break 
    def start(self):
        for id, url in enumerate(self.urls):
            self.increment = id
            self.scroll()
            self.links =  self.links + list(map(lambda value: {"source":url,"target":value},self.linkstmp))
            self.linkstmp = []
        print(self.urls[id])
        print(self.links)
        self.driver.close()
# driver = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities=DesiredCapabilities.CHROME)





# print(driver.execute_script('return document.elementFromPoint(18,155).outerHTML'))
# actions.move_to_element_with_offset(driver.findElement('body'), 0,0)



# print(driver.current_url)
# driver.close()
# "var rect = elem.getBoundingClientRect(); console.log(rect.top, rect.right, rect.bottom, rect.left);"