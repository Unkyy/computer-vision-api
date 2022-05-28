import numpy as np
from io import BytesIO
from PIL import Image
from service.OcrModel import OcrModel
from service.Web_testing import Web_testing

class Web_testing_ocr(Web_testing):

    def __init__(self, url):
        self.windows__y__size = 768
        super().__init__(url)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, self.windows__y__size)

    def ocr_apply(self,):
        print(self.driver.execute_script('return "toto"'))
        self.driver.save_screenshot("./service/img/test.png")
        # self.actions.move_by_offset(15,15).click().perform()
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
            # sleep(1)
            # print(texts[id])
            try:
              self.driver.execute_script("document.elementFromPoint(arguments[0], arguments[1])?.click()",str(top),str(left))
            except:
              print('An exception occurred')
            # self.driver.execute_script(js)
            # self.actions.move_by_offset(target[0],target[1]).click().perform()
            self.url_append(self.driver.current_url)
            # if(self.driver.current_url not in self.urls and self.driver.current_url.split("/")[2] == self.urls[0].split("/")[2]):
            #     self.urls.append(self.driver.current_url)
            # if(self.driver.current_url not in self.linkstmp):
            #     self.linkstmp.append(self.driver.current_url)
            # sleep(1)
            self.driver.get(self.urls[self.increment])
            self.driver.execute_script("window.scrollTo(0, arguments[0]);", self.scrollY) 
            # self.actions.move_by_offset(-target[0],-target[1]).perform()
    def scroll(self):
        last_height = self.driver.execute_script("return window.scrollY;")
        self.scrollY = self.windows__y__size
        self.ocr_apply() 
        while True:
            # sleep(1)
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, arguments[0]);", self.scrollY) 
            # Wait to load page
            self.scrollY += self.scrollY
            # sleep(1)
            # Calculate new scroll height and compare with last scroll height
 
            new_height = self.driver.execute_script("return window.scrollY;")
            print()
            print(new_height)
            print(last_height)
            if new_height == last_height:
                break
            last_height = new_height
            self.ocr_apply() 
    