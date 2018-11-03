from selenium import webdriver
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.chrome.options import Options
import time
import os
import colorama
import urllib.request
import zipfile
import sys
import getpass

#TODO upload checker
#TODO psutil
#TODO loop until correct name and password or exit
#TODO save download dir and username and password
#TODO better username and password checker
#TODO linux version

class OneDriveUser():
    """Class of OneDrive user"""

    def __init__(self):

        #Ask for username and password
        self.user_name = input(">Enter username: ")
        self.password = getpass.getpass(">Enter password: ")

        #Ask for the path where downloadfiles will be stored and checks if a proper path was given
        self.dir_download = input(">Enter full path for download dir or press Enter for default: ")

        #If no path given make Download dir in the current path
        if self.dir_download == "":
            self.dir_download = os.getcwd() +  "\\Downloads_onedive" if os.name == "nt" else "/Downloads_onedrive"

            #Check if Download dir exists
            if not os.path.isdir(self.dir_download):
                os.mkdir(self.dir_download)
        else:
            while not os.path.isdir(self.dir_download):
                print("You enter an incorrect path.")
                self.dir_download = input(">Enter again")

        print(">Initialize chromedriver...")

        #Initialize current path
        self.current_path = "/root"
        self.url_s = []
        self.index_of_url_s = 0
        self.cur_url = "https://onedrive.live.com/about/en-gb/signin/"
        self.start_download = False

        #Check if os is windows or linux and  write proper path
        if os.name == "nt":
            dir_path = os.environ["userprofile"]+"\\ch"
            chrome_path = os.environ["userprofile"]+"\\ch"+"\\chromedriver.exe"
            zip_path = os.environ["userprofile"]+"\\ch"+"\\ch.zip"
        else:
            dir_path = os.path.expanduser("~")+"/ch"
            chrome_path = os.path.expanduser("~")+"/ch"+"/chromedriver.exe"
            zip_path = os.path.expanduser("~")+"/ch"+"/ch.zip"

        #Set the dir where the chromedriver will be
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        #Download and extract chromedriver
        if not os.path.isfile(chrome_path):
            url = "https://chromedriver.storage.googleapis.com/2.41/chromedriver_win32.zip"
            urllib.request.urlretrieve(url, zip_path)
            zipf = zipfile.ZipFile(zip_path, "r")
            zipf.extractall(dir_path)
            zipf.close()
            os.remove(zip_path)

    def download_dir(self):
        """Set the right parameters so that headless chromedriver can download"""

        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.dir_download}}
        command_result = self.driver.execute("send_command", params)

    def set_download_dir(self):
        """Function ofr change download dir"""

        self.dir_download = input(">Enter full path for download dir")
        while not os.path.isdir(self.dir_download):
            print("You enter an incorrect path.")
            self.dir_download = input(">Enter again")

        self.download_dir()

    def logging(self):
        """Function for setting up parameters for logging"""

        print("Wait untill login...")

        #Check if os is windows or linux and  write proper path
        if os.name == "nt":
            chrome_path = os.environ["userprofile"]+"\\ch"+"\\chromedriver"
        else:
            chrome_path = os.path.expanduser("~")+"/ch"+"/chromedriver"

        #Setting up chromedriver options for headless and silent mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
        self.download_dir()
        self.driver.get('https://onedrive.live.com/about/en-gb/signin/')

        #Wait untill username input element is avaible in webpage
        input = self.driver.find_elements_by_xpath("//input[@type='email']")
        while len(input) == 0:
            input = self.driver.find_elements_by_xpath("//input[@type='email']")

        #Enable automate actions in browser
        action = action_chains.ActionChains(self.driver)

        #When element is avaible sent username
        action.send_keys(self.user_name)
        action.send_keys(keys.Keys.ENTER)
        action.perform()

        #Wait untill new url has been loaded
        time.sleep(5)

        #Wait untill password input element is avaible in webpage
        passw = self.driver.find_elements_by_xpath("//input[@type='password']")
        while len(passw) == 0:
            passw = self.driver.find_elements_by_xpath("//input[@type='password']")
            input = self.driver.find_elements_by_xpath("//input[@type='email']")

            #If wrong username exit
            if self.driver.current_url == self.cur_url:
                print("You enter wrong username")
                self.driver.quit()
                exit()

        #Save current url
        self.cur_url = self.driver.current_url

        #Enable automate actions in browser
        action = action_chains.ActionChains(self.driver)

        #When element is avaible sent password
        action.send_keys(self.password)
        action.send_keys(keys.Keys.ENTER)
        action.perform()

        #Wait untill new url has been loaded
        time.sleep(5)

        #If wrong password exit
        if self.driver.current_url.find("root") <0:
            print("You enter wrong password")
            self.driver.quit()
            exit()

        #Save current url
        self.cur_url = self.driver.current_url

        print(">You are login. Press help for a full command list")

    def ls(self):
        """Fuction which shows a full list of files and folders"""

        #Enables colorama and autoreset the color of the cmd
        colorama.init(autoreset=True)

        #Wait untill all the files and folders are avaible in webpage
        elements = self.driver.find_elements_by_xpath("//div[@data-item-index]")
        while len(elements) == 0:
            elements = self.driver.find_elements_by_xpath("//div[@data-item-index]")

        #Pass through all the elements, take their name and print it
        for i in range(0, len(elements)):

            #Check if the element is a folder and if it is, print it with red color
            if elements[i].text[elements[i].text.find(",")+2:elements[i].text.find(",")+8] == "Folder":
                print(colorama.Fore.RED + elements[i].text[0:elements[i].text.find(",")])
            else:
                print(elements[i].text[0:elements[i].text.find(",")])

    def cd(self, dir):
        """Function which change current path from dir1 to dir2"""

        #Flag to check if the dir exists
        dir_ex = 0

        #If dir == .. return to the parent folder
        if dir == "..":

            dir_ex = 1

            #Take the previous folder's url and go there
            if self.index_of_url_s > 0:
                self.index_of_url_s -= 1
                self.driver.get(self.url_s[self.index_of_url_s])
                del self.url_s[self.index_of_url_s]
                self.current_path = self.current_path[0:self.current_path.rfind("/")]
                return
            else:

                #You are already on root
                print("You are on root")
                return

        #Wait untill all the files and folders are avaible in webpage
        elements = self.driver.find_elements_by_xpath("//div[@data-item-index]")
        while len(elements) == 0:
            elements = self.driver.find_elements_by_xpath("//div[@data-item-index]")

        #Pass through all the elements, take their name save the folder's url and go to the specific folder dir != ..
        for i in range(0, len(elements)):
            try:

                #Check if the name of the dir correspond to a folder's or file's name
                if elements[i].text[0:elements[i].text.find(",")] == dir:

                    #Check if the element is a folder and if it is, go to it
                    if elements[i].text[elements[i].text.find(",")+2:elements[i].text.find(",")+8] == "Folder":

                        #Flag to 1 because dir exists
                        dir_ex = 1

                        #Keeps previous folder's url
                        self.url_s.append(self.driver.current_url)
                        self.index_of_url_s += 1

                        #Click to the corresponding folder
                        action = action_chains.ActionChains(self.driver)
                        action.click(elements[i])
                        action.perform()

                        #Add the dir to the current path
                        self.current_path += "/" + dir
                    else:
                        print(dir+" is not a folder")

            except:
                sys.stdout.write("")

        #No folder found
        if dir_ex == 0:
            print(dir + " does not exist")

    def super_cd(self, dir):
        """Function which change from path1 to path2"""

        #Split path
        dir_list = dir.split("/")

        #Check if the path given was onle a dir's name
        if len(dir_list) <= 1:
            self.cd(dir_list[0])

        #If the path name was a rel goes here
        elif dir[0:2] == "./":
            dir_list = dir_list[1:]

            #Calls cd for every one of the dirs
            for i in range(0, len(dir_list)):
                self.cd(dir_list[i])

        #If the path name was an abs goes here
        else:
            if "root" in dir_list:
                #Initialize current path
                self.url_s = []
                self.index_of_url_s = 0
                self.driver.get('https://onedrive.live.com/')
                self.current_path = "/" + "root"
                dir_list = dir_list[2:]

            #If the path name starts with ../ goes here
            else:
                dir_list = dir_list[0:]

            #Call cd for every one of the dirs
            for i in range(0, len(dir_list)):
                self.cd(dir_list[i])

    def upload_file(self, file_name):
        """Function which uploads a file"""

        #Wait untill upload button is avaible in webpage and takes the proper path of the upload file
        upload_f = self.driver.find_elements_by_xpath("//input[@type='file']")
        if os.name == "nt":
            send = (os.getcwd() + '\\' + file_name) if not file_name.find("\\") > 0 else file_name
        else:
            send = (os.getcwd() + '/' + file_name) if not file_name.find("/") > 0 else file_name
        while len(upload_f) == 0:
            upload_f = self.driver.find_elements_by_xpath("//input[@type='file']")

        #Check if the file exists and starts upload
        if os.path.isfile(file_name):
            try:
                upload_f[0].send_keys(send)
            except:
                print("Problem with upload. Please retry")
        else:
            print("File does not exist")

    def mkdir(self, folder_name):
        """Function which makes a new folder"""

        #Wait untill New button is avaible in webpage
        new = self.driver.find_elements_by_xpath("//button[@name='New']")
        while len(new) == 0:
            new = self.driver.find_elements_by_xpath("//button[@name='New']")

        #If button is ready, click it
        action = action_chains.ActionChains(self.driver)
        action.click(new[0])
        action.perform()

        #Wait untill Folder button is avaible in webpage
        folder = self.driver.find_elements_by_xpath("//button[@name='Folder']")
        while len(folder) == 0:
            folder = self.driver.find_elements_by_xpath("//button[@name='Folder']")

        #If button is ready, click it
        action = action_chains.ActionChains(self.driver)
        action.click(folder[0])
        action.perform()

        #Wait and afterwards sent the folders name and create it
        time.sleep(0.1)
        action = action_chains.ActionChains(self.driver)
        action.send_keys(folder_name)
        action.send_keys(keys.Keys.ENTER)
        action.perform()

    def d(self, d_file, download_or_delete):
        """Function which download or delete folder/s or file/s (Both are in the same function becaause their implementation code was almost the same)"""

        #Split file or folder names
        d_list = d_file.split(" ")

        #flag
        fl = 0

        #Wait untill all the files and folders are avaible in webpage
        elements = self.driver.find_elements_by_xpath("//div[@data-item-index]")
        while len(elements) == 0:
            elements = self.driver.find_elements_by_xpath("//div[@data-item-index]")

        #Wait untill all the checkboxes of files and folders are avaible in webpage
        circle = self.driver.find_elements_by_xpath("//i[@data-icon-name='CircleRing']")
        while len(circle) == 0:
            circle = self.driver.find_elements_by_xpath("//i[@data-icon-name='CircleRing']")

        #Search if every name of d_file exists and check their checkboxes
        for i in range(0, len(d_list)):
            for j in range(0, len(elements)):
                if d_list[i] == elements[j].text[0:elements[j].text.find(",")]:
                    action = action_chains.ActionChains(self.driver)
                    action.click(circle[j])
                    action.perform()
                    fl = 1
                    break

            if fl == 0:
                print(d_list[i] + " does not exist give a proper name.\n Try to enter the file's name you want to download without its extension")
                return

        #Check if we want download or delete
        if download_or_delete == 'download':

            time.sleep(2)

            #Wait untill Download button is avaible in webpage
            d_b = self.driver.find_elements_by_xpath("//button[@name='Download']")
            while len(d_b) == 0:
                d_b = self.driver.find_elements_by_xpath("//button[@name='Download']")

            #If button is ready, click it
            action = action_chains.ActionChains(self.driver)
            action.click(d_b[0])
            action.perform()

            #Uncheck box so it wouldn't be mistaken deleted or downloaded again
            for i in range(0, len(d_list)):
                for j in range(0, len(elements)):
                    if d_list[i] == elements[j].text[0:elements[j].text.find(",")]:
                        action = action_chains.ActionChains(self.driver)
                        action.click(circle[j])
                        action.perform()
                        break

            self.start_download = True

        else:

            time.sleep(2)

            #Wait untill Delete button is avaible in webpage
            d_b = self.driver.find_elements_by_xpath("//button[@name='Delete']")
            while len(d_b) == 0:
                d_b = self.driver.find_elements_by_xpath("//button[@name='Delete']")

            #If button is ready, click it
            action = action_chains.ActionChains(self.driver)
            action.click(d_b[0])
            action.perform()

    def get_download_progress_all(self):
        """Get a list with all unfinished downloads"""

        #Take all the files names from download dir
        names = os.listdir(self.dir_download)

        #Wait until first download starts
        while len(names) == 0 and self.start_download:
            names = os.listdir(self.dir_download)

        self.start_download = False

        crd = []

        #Keep track of an unfinished download
        flag = 0

        #Print all the files that has not finished download
        for name in names:

            #unfinished files extensions
            if name.find(".crdownload") > 0:
                if flag == 0:
                    print("Still download:\n")
                    flag = 1

                #Add download files name in the list
                crd.append(name)

                #Print all the download files
                print(name[0:name.find(".crdownload")] + "\n")

        return crd

    def stop_download(self):
        """Stop all unfinished downloads"""

        #Get list with unfinished Downloads
        names = self.get_download_progress_all()

        #Return if all downloads have finished
        if len(names) == 0:
            return

        #remove all the unfinished downloads
        for name in names:
            os.remove(self.dir_download + "\\" + name)

    def quit(self):
        """ Quit from the program"""

        #Check if there is an unfinished download
        answer = input(">Are you sure you want to exit? [Y/n]")

        #If yes quit and delete all unfinished downloads
        if answer == "Y" or answer == "Yes" or answer == "y" or answer == "yes":
            self.driver.quit()

            #Stop all downloads
            self.stop_download()

            return True
        else:
            return False

        return True
