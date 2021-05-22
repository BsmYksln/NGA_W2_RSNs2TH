"""
NGA_W2_RSNs2TH

Module for web automation tool in order to download unscaled record time histories from
NGA-West2 Database (https://ngawest2.berkeley.edu/) by Record Sequence Numbers (RSNs)
                                                        Besim Yukselen - 2020
                                                        Last Major Update: 12/05/2021
"""

import sys
import os
import time
import zipfile
import requests
from selenium import webdriver


class NGA_W2_RSNs2TH:
    def __init__(self, username, password, download_path=os.getcwd()):
        # Initial Assignments
        self.download_path = download_path
        self.username = username
        self.password = password
        self.RSN_str = ''
        # Initial Controls
        self.op_sys = sys.platform
        if self.op_sys.startswith('win'):
            self.aim_driver = 'chromedriver.exe'
            self.zip_name_extension = '_win32'
        elif self.op_sys.startswith('linux'):
            self.aim_driver = 'chromedriver'
            self.zip_name_extension = '_linux64'
        elif self.op_sys.startswith('darwin'):
            self.aim_driver = 'chromedriver'
            self.zip_name_extension = '_mac64'
        try:
            self.path_of_driver = os.path.join([i for i in sys.path if 'site-packages' in i][0], self.aim_driver)
        except IndexError:
            self.path_of_driver = os.path.join([i for i in sys.path if 'dist-packages' in i][0], self.aim_driver)
        self.check_and_download_chrome()
        # Initiate driver in headless mode
        self.driver_opt = webdriver.ChromeOptions()
        self.driver_opt.headless = True
        preference = {"download.default_directory": self.download_path}
        self.driver_opt.add_experimental_option("prefs", preference)
        # self.driver_opt.download_path = self.download_path
        self.driver = webdriver.Chrome(executable_path=self.path_of_driver, options=self.driver_opt)
        url_sign_in = 'https://ngawest2.berkeley.edu/users/sign_in'
        self.driver.get(url_sign_in)
        self.driver.implicitly_wait(10)

    def check_and_download_chrome(self):
        """
        This function will be used in order to download
        the chrome_driver compatible with the current operating system
        !!! Important the drivers will be searched (and to be downloaded if the case)
        at the location where the site-packages located!!!
        """

        def find_latest_ver():
            """
            Find latest version of chromedriver available on 'https://chromedriver.chromium.org/'
            """

            r = requests.get('https://chromedriver.chromium.org/')
            r_txt = r.text
            start = r_txt.find('Latest stable')
            text = r_txt.replace(r_txt[0:start], '')
            start = text.find('path=')
            text = text.replace(text[0:start + 5], '')
            end = text.find("/")
            latest_ver = text.replace(text[end::], '')
            return latest_ver

        def download_from_url(url, save_path, chunk_size=128):
            """
            This function will download latest version compatible stable version of chromedriver as zip file
            """
            r = requests.get(url, stream=True)
            with open(save_path, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)

        def add_driver_to_the_path(save_path):
            """
            This function will add chromedriver to the path and authorise if needed.
            Later the zip file contains chromedriver will be deleted.
            """
            try:
                site_package_dirs = [i for i in sys.path if 'site-packages' in i][0]
            except IndexError:
                site_package_dirs = [i for i in sys.path if 'dist-packages' in i][0]
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                zip_ref.extractall(site_package_dirs)
            print('chromedriver downloaded successfully!!')
            os.remove(save_path)
            if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
                os.chmod(self.path_of_driver, 0o777)

        # Searching for the driver at local paths
        if os.path.exists(self.path_of_driver):
            #  If driver exists checking for the latest version
            #  Check existing version
            headless_opt = webdriver.ChromeOptions()
            headless_opt.headless = True
            driver = webdriver.Chrome(executable_path=self.path_of_driver, options=headless_opt)
            driver.quit()
            if 'browserVersion' in driver.capabilities:
                present_driver_release = driver.capabilities['browserVersion']
            else:
                present_driver_release = driver.capabilities['version']
            latest_driver_version = find_latest_ver()
            if present_driver_release[:9] != latest_driver_version[:9]:
                print("There is a newer version of chromedriver existing one will be replaced...")
                os.remove(self.path_of_driver)
                print('Downloading the chromedriver!!')
                save_path = os.path.join(os.getcwd(), 'chromedriver.zip')
                url = f"https://chromedriver.storage.googleapis.com/{latest_driver_version}" \
                      f"/chromedriver{self.zip_name_extension}.zip"
                download_from_url(url, save_path, chunk_size=128)
                add_driver_to_the_path(save_path)
            else:
                pass
        else:
            print('Downloading the chromedriver!!')
            latest_driver_version = find_latest_ver()
            save_path = os.path.join(os.getcwd(), 'chromedriver.zip')
            url = f"https://chromedriver.storage.googleapis.com/{latest_driver_version}" \
                  f"/chromedriver{self.zip_name_extension}.zip"
            download_from_url(url, save_path, chunk_size=128)
            add_driver_to_the_path(save_path)

    def sign_in_with_given_credentials(self):
        """
        This function used to sing in to 'https://ngawest2.berkeley.edu/' with given account credentials.
        """
        print("Signing in with given account!...")
        self.driver.find_element_by_id('user_email').send_keys(self.username)
        self.driver.find_element_by_id('user_password').send_keys(self.password)
        self.driver.find_element_by_id('user_submit').click()
        try:
            alert = self.driver.find_element_by_css_selector('p.alert')
            warn = alert.text
            if str(warn) == 'Invalid email or password.':
                self.driver.quit()
                raise ValueError('Invalid email or password.')
        except Exception as e:
            print(e)
            pass
        return self

    def download_by_RSN(self):
        """
        This function searches and downloads the ground motion records from NGA-W2 database.
        """
        def download_wait(download_directory):
            """
            This function used to explicitly sleeps the code until the download have been completed.
            Download completion status has been controlled by the increase of the size of download directory.
            """
            def dir_size(download_dir):
                """
                This functions checks the size of the given directory.
                """
                total_size = 0
                for path, dirs, files in os.walk(download_dir):
                    for f in files:
                        fp = os.path.join(path, f)
                        total_size += os.path.getsize(fp)
                return total_size

            delta_size = 100
            flag = 0
            flag_lim = 5
            while delta_size > 0 and flag < flag_lim:
                size_0 = dir_size(download_directory)
                time.sleep(6)
                size_1 = dir_size(download_directory)
                if size_1 - size_0 > 0:
                    delta_size = size_1 - size_0
                else:
                    flag += 1
                    print(flag_lim - flag)

        url_get_record = 'https://ngawest2.berkeley.edu/spectras/new?sourceDb_flag=1'
        print("Listing the Records!....")
        self.driver.get(url_get_record)
        self.driver.find_element_by_xpath("//button[@type='button']").submit()
        self.driver.find_element_by_id('search_search_nga_number').send_keys(self.RSN_str)
        self.driver.find_element_by_xpath(
            "//button[@type='button' and "
            "@onclick='uncheck_plot_selected();reset_selectedResult();OnSubmit();']").submit()
        try:
            note = self.driver.find_element_by_id('notice').text
        except Exception as e:
            print(e)
            note = 'NO'
        if 'NO' in note:
            self.driver.quit()
            raise ValueError("Ground motion data could not found for given RSNs")
        else:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            self.driver.find_element_by_xpath(
                "//button[@type='button' and @onclick='getSelectedResult(true)']").click()
            print("Downloading the Records!...")
            alert_obj = self.driver.switch_to.alert
            alert_msg = alert_obj.text
            print("Alert shows following message: " + alert_msg)
            alert_obj.accept()
            alert_obj = self.driver.switch_to.alert
            alert_msg = alert_obj.text
            print("Alert shows following message: " + alert_msg)
            alert_obj.accept()
            print("Downloading the Records!...")
            download_wait(self.download_path)
            self.driver.quit()

    def RSNs_2_TH(self, RSN_list):
        """
        This function will download time histories of given list of RNSs
        """
        RSN_str = ''
        for i in RSN_list:
            RSN_str += str(int(i)) + ','
        self.RSN_str = RSN_str[:-1:]
        self.sign_in_with_given_credentials()
        file_set_before_download = set(os.listdir(self.download_path))
        self.download_by_RSN()
        file_set_after_download = set(os.listdir(self.download_path))
        new_file = list(file_set_after_download.difference(file_set_before_download))[0]
        new_name = 'PEERNGARecords_Unscaled_' + time.strftime('%d_%m_%Y-%H%M_%S', time.localtime())+'.zip'
        os.rename(os.path.join(self.download_path, new_file), os.path.join(self.download_path, new_name))
        print(f'Download has done!\nFiles can be found:\n{os.path.join(self.download_path, new_name)}')

