from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from bs4 import BeautifulSoup
import os

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

class WhatsApp:
    def __init__(self, driver_path):
        self.__link = 'https://web.whatsapp.com/'
        self.__userBox = '//span[@title = "{}"]' # => xpath of the user element
        self.__writingBox = '_3u328' # => class name of the writing box
        self.__sendingBox = '_3M-N-' # => class name of the sending box
        self.__notificationBox = 'P6z4j' #//span[@class = 'P6z4j'
        try:
            if(driver_path != None):
                self.__driver = webdriver.Chrome(driver_path)
            else:
                self.__driver = webdriver.Chrome()
        except WebDriverException as err:
            print('Please include the webdriver in the path or provide the driver location in the object instance')
            exit()

        # Driver is located
        self.__driver.get(self.__link)
        print('Waiting for the user to scan the QR code')
        input('Press anything if you are logged')

    def close(self):
        self.__driver.close()

    def send_message(self, user: str, message: str):
        #! This could raise NoSuchElementException
        try:
            userElement = self.__driver.find_element_by_xpath(self.__userBox.format(user.strip()))
            userElement.click()
        except NoSuchElementException:
            print('User dont found!')
            self.__driver.close()
            exit()

        try:
            msgElement = self.__driver.find_element_by_class_name(self.__writingBox)
        except NoSuchElementException:
            print('Writing box or Sending box dont found!')
            self.__driver.close()
            exit()

        if message != None:
            msgElement.send_keys(message)
            sendingElement = self.__driver.find_element_by_class_name(self.__sendingBox)
            sendingElement.click()
    
    def get_messages(self):
        '''
        //*[@id="pane-side"]/div[1]/div/div/div[15]/div/div/div[2]/div[2]/div[2]/span[1]/div/span

        //*[@id="pane-side"]/div[1]/div/div/div[15]/div/div/div[2]
        '''

        #Open the sender element box
        # element = self.__driver.find_element_by_xpath(self.__notificationBox)
        # element.click()
        # element.click()
        # print(element)
        
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        notification = soup.find('span', class_=self.__notificationBox).findParent('div', class_='_2WP9Q')
        xpath = xpath_soup(notification)
        # print(xpath)
        self.__driver.find_element_by_xpath(xpath).click()

c = WhatsApp('/home/pedro/Área de Trabalho/Projetos/Python/Untitled Folder/chromedriver')
# c.send_message('Renan', 'Teste')
c.get_messages()
input('Waiting input for closing')
c.close()