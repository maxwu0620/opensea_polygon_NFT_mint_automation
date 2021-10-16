import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions

root = Tk()
root.title("Opensea Upload Automation")
input_save_list = ["Upload folder:", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])

def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )

def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud") 

# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)

###input objects###
collection_link_input = InputField("Collection_link:", 2, 0, 1)
start_num_input = InputField("Start num:", 3, 0, 2)
uplode_amount = InputField("uplode_amount:", 4, 0, 3)
price = InputField("price:", 5, 0, 4)
title = InputField("title:", 6, 0, 5)
file_format = InputField("File format:", 7, 0, 6)
external_link = InputField("External link:", 8, 0, 7)
description = InputField("Description:", 9, 0, 8)

###save inputs###
def save():
    input_save_list.insert(0, upload_path)
    collection_link_input.save_inputs(1)
    start_num_input.save_inputs(2)
    uplode_amount.save_inputs(3)
    price.save_inputs(4)
    title.save_inputs(5)
    file_format.save_inputs(6)
    external_link.save_inputs(7)
    description.save_inputs(8)

# _____MAIN_CODE_____
def main_program_loop():  # DEBUG ONLY
    print("Main started")
    ###START###
    project_path = main_directory
    file_path = upload_path
    collection_link = collection_link_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    up_amount = int(uplode_amount.input_field.get())
    loop_price = float(price.input_field.get())
    loop_title = title.input_field.get()
    loop_file_format = file_format.input_field.get()
    loop_external_link = str(external_link.input_field.get())
    loop_description = description.input_field.get()

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

    ###wait for methods
    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))


    while up_amount != 0:
        print(str(start_num) + " and this many left > " + str(up_amount))
        driver.get(collection_link)
        # time.sleep(3)

        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        #additem = driver.find_element_by_css_selector("a[class='styles__StyledLink-sc-l6elh8-0 ekTmzq Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gMiESj']")
        additem.click()
        time.sleep(1)

        wait_xpath('//*[@id="media"]')
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        imagePath = os.path.abspath(file_path + "\\" + str(start_num) + "." + loop_file_format)  # change folder here
        imageUpload.send_keys(imagePath)

        name = driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys(loop_title + str(start_num))  # +1000 for other folders #change name before "#"
        time.sleep(0.5)

        ext_link = driver.find_element_by_xpath('//*[@id="external_link"]')
        ext_link.send_keys(loop_external_link)
        time.sleep(0.5)

        desc = driver.find_element_by_xpath('//*[@id="description"]')
        desc.send_keys(loop_description)
        time.sleep(0.5)

        create = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
        create.click()
        time.sleep(1)

        wait_css_selector("i[aria-label='Close'")
        cross = driver.find_element_by_css_selector("i[aria-label='Close'")
        cross.click()
        time.sleep(1)

        main_page = driver.current_window_handle

        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
        sell = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
        sell.click()
        # time.sleep(1)

        wait_css_selector("input[placeholder='Amount']")
        amount = driver.find_element_by_css_selector("input[placeholder='Amount']")
        # amount.click()
        amount.send_keys(str(loop_price))
        # time.sleep(1)

        wait_css_selector("button[type='submit']")
        listing = driver.find_element_by_css_selector("button[type='submit']")
        listing.click()
        # time.sleep(1)

        # time.sleep(5)
        wait_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
        sign = driver.find_element_by_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
        sign.click()
        time.sleep(2)
        ###login backup location
        # changing the handles to access login page
        for handle in driver.window_handles:
            if handle != main_page:
                login_page = handle
        # change the control to signin page
        driver.switch_to.window(login_page)
        # time.sleep(5)
        wait_css_selector("button[data-testid='request-signature__sign']")
        sign = driver.find_element_by_css_selector("button[data-testid='request-signature__sign']")
        sign.click()
        time.sleep(1)
        # change control to main page
        driver.switch_to.window(main_page)
        time.sleep(1)

        start_num = start_num + 1
        up_amount = up_amount - 1

#####BUTTON ZONE#######
button_save = tkinter.Button(root, text="Save", command=save) 
button_save.grid(row=20, column=2)
button_start = tkinter.Button(root, text="Start", command=main_program_loop)
button_start.grid(row=20, column=1)
open_browser = tkinter.Button(root, text="Open Browser", command=open_chrome_profile)
open_browser.grid(row=2, column=2)
upload_folder_input_button = tkinter.Button(root, height=3, width=60, text="Add Upload Folder", command=upload_folder_input)
upload_folder_input_button.grid(row=0, columnspan=3)
try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        Name_change_img_folder_button(new_dict[0])
        upload_path = new_dict[0]
except FileNotFoundError:
    pass
#####BUTTON ZONE END#######
root.mainloop()
