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


class InputField:
    def __init__(self, master, label, row_io, column_io):
        self.master = master
        # self.entry = Entry(master)
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        # self.entry.insert(0, "")

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)


root = Tk()
root.title("Opensea Uploade Automation")


collection_link_input = InputField(root, "Collection_link:", 2, 0)
start_num_input = InputField(root, "Start num:", 3, 0)
uplode_amount = InputField(root, "uplode_amount:", 4, 0)
price = InputField(root, "price:", 5, 0)
title = InputField(root, "title:", 6, 0)
file_format = InputField(root, "File format:", 7, 0)
external_link = InputField(root, "External link:", 8, 0)
description = InputField(root, "Description:", 9, 0)

main_directory = os.path.join(sys.path[0])


# _____MAIN_CODE_____
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


def main_program_loop():  # DEBUG ONLY
    print("Main started")
    ###START###
    project_path = main_directory
    file_path = img_folder_path
    collection_link = collection_link_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    up_amount = int(uplode_amount.input_field.get())
    price_ALI = float(price.input_field.get())
    title_ALI = title.input_field.get()
    file_format_ALI = file_format.input_field.get()
    external_link_ALI = str(external_link.input_field.get())
    description_ALI = description.input_field.get()

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

    ###wait for methods
    def wait_for(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

    while up_amount != 0:
        print(str(start_num) + " and this many left > " + str(up_amount))
        url = collection_link
        driver.get(url)
        # time.sleep(3)

        wait_for(
            ".styles__StyledLink-sc-l6elh8-0.cnTbOd.Blockreact__Block-sc-1xf18x6-0.Buttonreact__StyledButton-sc-glfma3-0.bhqEJb.gMiESj"
        )
        additem = driver.find_element_by_css_selector(
            ".styles__StyledLink-sc-l6elh8-0.cnTbOd.Blockreact__Block-sc-1xf18x6-0.Buttonreact__StyledButton-sc-glfma3-0.bhqEJb.gMiESj"
        )
        additem.click()
        time.sleep(1)

        wait_xpath('//*[@id="media"]')
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        imagePath = os.path.abspath(
            file_path + "\\" + str(start_num) + "." + file_format_ALI
        )  # change folder here
        imageUpload.send_keys(imagePath)

        name = driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys(
            title_ALI + str(start_num)
        )  # +1000 for other folders #change name before "#"
        time.sleep(0.5)

        ext_link = driver.find_element_by_xpath('//*[@id="external_link"]')
        ext_link.send_keys(external_link_ALI)
        time.sleep(0.5)

        desc = driver.find_element_by_xpath('//*[@id="description"]')
        desc.send_keys(description_ALI)
        time.sleep(0.5)

        create = driver.find_element_by_css_selector(
            ".Blockreact__Block-sc-1xf18x6-0.Buttonreact__StyledButton-sc-glfma3-0.bhqEJb.gMiESj"
        )
        create.click()
        time.sleep(1)

        wait_for(
            ".Iconreact__Icon-sc-1gugx8q-0.Modalreact__StyledIcon-sc-xyql9f-1.irnoQt.byuytI.material-icons"
        )
        cross = driver.find_element_by_css_selector(
            ".Iconreact__Icon-sc-1gugx8q-0.Modalreact__StyledIcon-sc-xyql9f-1.irnoQt.byuytI.material-icons"
        )
        cross.click()
        time.sleep(1)

        main_page = driver.current_window_handle

        wait_for(
            "a[class='styles__StyledLink-sc-l6elh8-0 cnTbOd Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 jxgnwF gMiESj OrderManager--second-button']"
        )
        sell = driver.find_element_by_css_selector(
            "a[class='styles__StyledLink-sc-l6elh8-0 cnTbOd Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 jxgnwF gMiESj OrderManager--second-button']"
        )
        sell.click()
        # time.sleep(1)

        wait_for("input[placeholder='Amount']")
        amount = driver.find_element_by_css_selector("input[placeholder='Amount']")
        # amount.click()
        amount.send_keys(str(price_ALI))
        # time.sleep(1)

        wait_for(
            "button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gMiESj']"
        )
        listing = driver.find_element_by_css_selector(
            "button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gMiESj']"
        )
        listing.click()
        # time.sleep(1)

        # time.sleep(5)
        wait_for(
            "button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gMiESj']"
        )
        sign = driver.find_element_by_css_selector(
            "button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gMiESj']"
        )
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
        wait_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]')
        sign = driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]'
        )
        sign.click()
        time.sleep(1)
        # change control to main page
        driver.switch_to.window(main_page)
        time.sleep(1)

        start_num = start_num + 1
        up_amount = up_amount - 1


# _____SAVE_____

# gets path to save file in current working directory.
def save_file_path():
    return os.path.join(sys.path[0], "Save_file.ali")


# saves GUI inputs to file.
def Save():
    thing_to_save_for_next_time = [
        img_folder_path,
        collection_link_input.input_field.get(),
        start_num_input.input_field.get(),
        int(uplode_amount.input_field.get()),
        float(price.input_field.get()),
        title.input_field.get(),
        file_format.input_field.get(),
        str(external_link.input_field.get()),
        description.input_field.get(),
    ]
    with open(save_file_path(), "wb") as outfile:
        pickle.dump(thing_to_save_for_next_time, outfile)


# opens save file, sets of variables, changes text on GUI.
def open_save():
    try:
        with open(save_file_path(), "rb") as infile:
            new_dict = pickle.load(infile)
            global img_folder_path
            Name_change_img_folder_button(new_dict[0])
            img_folder_path = new_dict[0]
            collection_link_input.insert_text(new_dict[1])
            start_num_input.insert_text(new_dict[2])
            uplode_amount.insert_text(new_dict[3])
            price.insert_text(new_dict[4])
            title.insert_text(new_dict[5])
            file_format.insert_text(new_dict[6])
            external_link.insert_text(new_dict[7])
            description.insert_text(new_dict[8])

    except FileNotFoundError:
        pass


#####BUTTON ZONE#######
# changes the name of Button to path.
def Name_change_img_folder_button(img_folder_input):
    img_folder_input_button["text"] = img_folder_input


# ask for directory on clicking button, changes button name.
def img_folder_input():
    global img_folder_path
    img_folder_path = filedialog.askdirectory()
    Name_change_img_folder_button(img_folder_path)


button_save = tkinter.Button(root, text="Save", command=Save)
button_save.grid(row=20, column=2)
button_start = tkinter.Button(root, text="Start", command=main_program_loop)
button_start.grid(row=20, column=1)
open_browser = tkinter.Button(root, text="Open Browser", command=open_chrome_profile)
open_browser.grid(row=2, column=2)
img_folder_input_button = tkinter.Button(
    root, height=3, width=60, text="Add Upload Folder", command=img_folder_input
)
img_folder_input_button.grid(row=0, columnspan=3)
#####BUTTON ZONE END#######

open_save()
root.mainloop()
