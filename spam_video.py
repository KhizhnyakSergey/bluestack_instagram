from dataclasses import dataclass
from random import randint
import pyautogui 
import time
from colorama import init, Fore, Style
from datetime import datetime
from logger import log
import subprocess
import os, json
from pathlib import Path


init()
success = f'{Fore.GREEN}success{Style.RESET_ALL}'
failed = f'{Fore.RED}failed{Style.RESET_ALL}'
slip = f'{Fore.BLUE}sleeping{Style.RESET_ALL}'
refresh = f'{Fore.CYAN}<--refreshing app-->{Style.RESET_ALL}'
ban = f"{Fore.RED}| BAN | Account can't sand video{Style.RESET_ALL}"
done = f'{Fore.GREEN}-END-{Style.RESET_ALL}'

@dataclass(frozen=True, slots=True)
class Coord:
    click_found_first = (765, 144)
    click_found_second = (766, 210)
    

def send_failed(nickname):
    with open('users.txt', 'r') as file:
        nicknames = [user.strip() for user in file if user]
        nicknames.remove(nickname)
    with open('users.txt', 'w') as file:
        for nick in nicknames:
            file.write(nick + '\n')
    with open('failed.txt', 'a') as file:
        file.write(f'\n{nickname}')

def send_success(nickname):
    with open('users.txt', 'r') as file:
        nicknames = [user.strip() for user in file if user]
        nicknames.remove(nickname)
    with open('users.txt', 'w') as file:
        for nick in nicknames:
            file.write(nick + '\n')
    with open('used.txt', 'a') as file:
        file.write(f'\n{nickname}')

def get_users():
    with open('users.txt', 'r', encoding='utf-8') as file:
        return [user.strip() for user in file if user]

def override_email(mail: str):

    with open(f'{os.getcwd()}\\eccounts.json', 'r', encoding='utf-8') as reader:
        data = json.load(reader)
        used = {
            mail: data[mail]
        }
        del data[mail]
    with open(f'{os.getcwd()}\\eccounts.json', 'w', encoding='utf-8') as overriter:
        json.dump(data, overriter, indent=4, ensure_ascii=False)

    if Path(str(f'{os.getcwd()}\\used_accounts.json')).exists():
        with open(f'{os.getcwd()}\\used_accounts.json', 'r', encoding='utf-8') as reader:
            data = json.load(reader)
            data.update(used)
        with open(f'{os.getcwd()}\\used_accounts.json', 'w', encoding='utf-8') as overriter:
            json.dump(data, overriter, indent=4, ensure_ascii=False)
    else:
        with open(f'{os.getcwd()}\\used_accounts.json', 'w', encoding='utf-8') as writer:
            json.dump(used, writer, indent=4, ensure_ascii=False)

def from_txt_to_json(step: int = 2) -> None:
    new_data = {}
    with open(f'{os.getcwd()}\\accounts.txt', 'r', encoding='utf-8') as f:
        data = list(filter(lambda x: x if x else None, map(lambda x: x.strip(), f.read().split('\n'))))
    step = step
    buff = ''
    for index in range(len(data)):
        for d in data[index:step+index]:
            content = list(map(lambda x: x.strip(), d.split(':')))
            if content[0] == 'login':
                new_data[content[-1]] = {}
                buff = content[-1]
            else:
                new_data[buff].update({
                    content[0]: content[-1]
                })
    with open(f'{os.getcwd()}\\accounts.json', 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)

def find_and_click(path_img, confidence=0.8):
    while True:
        time.sleep(0.1)
        if (btn := pyautogui.locateOnScreen(f'{path_img}', confidence=confidence)):
            pyautogui.click(btn, duration=0.2)
            # print(btn)
            break

def start_bluestacks():
    # put correct path BlueStacks
    os.system(rf'start "" /max "C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe"') 

    # checking when app opened
    while True:
        if (pyautogui.locateOnScreen('src\\application_opened.png', confidence=0.7)): # app opened
            break

    find_and_click('src\\full_screen_stacks.png') # full screen
    time.sleep(1)

    start_inst = datetime.now().timestamp()
    while True:
        estimate_inst = datetime.now().timestamp() - start_inst
        if estimate_inst >= 15:
            log('trabl with inst icon')
            clouse_bluestacks()
            return start_bluestacks()

        find_and_click('src\\instagramm_icon.png') # click on instagramm icon

        # If you have been logged in and asked for a password to login
        start = datetime.now().timestamp()
        while True:
            estimate = datetime.now().timestamp() - start
            if estimate >= 4:
                break
            if (sign_in := pyautogui.locateOnScreen('src\\sign_in.png', confidence=0.7)): # btn "Войти"
                pyautogui.click(sign_in)
                time.sleep(1.5)
                password = pyautogui.locateOnScreen('src\\password.png', confidence=0.7) # find password line 
                pyautogui.click(password)

                for letter in 'uf2vjPmUG5zmx9l': # put password in line 
                    pyautogui.write(letter, interval=0.1)

                confirm = pyautogui.locateOnScreen('src\\confirm_btn.png', confidence=0.7) # btn "Войти"
                pyautogui.click(confirm)
                time.sleep(2)
                break
        # if text "Instagram" on screen 
        if pyautogui.locateOnScreen('src\\instagramm_text_in_main_screen.png', confidence=0.6): 
            break
        
def clouse_bluestacks():
    '''Put correct name'''
    subprocess.call(r'TASKKILL /F /IM HD-Player.exe', shell=True, stdout=subprocess.DEVNULL)

def change_account():
    
    time.sleep(1)
    pyautogui.click(1170, 1019, duration=0.2) # click on avatar (правый нижний угол)
    find_and_click('src\\sandwich_settings.png',confidence=0.9) # sandwich setting btn
    find_and_click('src\\settings_btn.png',confidence=0.9) # setting btn
    find_and_click('src\\settings_add_or_change_account_btn.png',confidence=0.9) # add or change account btn 
    find_and_click('src\\settings_add_account_btn.png',confidence=0.9) # add account btn 
    find_and_click('src\\settings_log_into_existing_account_btn.png',confidence=0.9) # log into existing account btn
    find_and_click('src\\settings_switch_accounts_btn.png',confidence=0.9) # switch accounts btn
    
    # login
    find_and_click('src\\login.png',confidence=0.9) # login line

    with open(f'{os.getcwd()}\\accounts.json', 'r', encoding='utf-8') as file:
        accounts = json.load(file)

    for account in accounts:
        for letter in account: # put login in line 
            pyautogui.write(letter, interval=0.1)
        # password
        find_and_click('src\\password.png',confidence=0.9) # password line
        time.sleep(1)
        for letter in accounts[account]["password"]: # put password in line 
            pyautogui.write(letter, interval=0.1)

        override_email(account)
        

    confirm = pyautogui.locateOnScreen('src\\confirm_btn_2.png', confidence=0.7) # btn "Войти"
    pyautogui.click(confirm)
    time.sleep(2)

def old_method_to_send_img():
    '''If the image is upside down after uploading, try changing the video upload method.'''
    # old metod to send files (Через иконку в левом нижнем углу)
    if pyautogui.locateOnScreen('src\\upload_btn_2.png') or pyautogui.locateOnScreen('src\\upload_btn_3.png') or pyautogui.locateOnScreen('src\\upload_btn_4.png'):
        pyautogui.click(680, 1010)
        time.sleep(0.5)
        find_and_click('src\\multy_img_btn.png')
        time.sleep(0.1)
        pyautogui.click(*Coord.first_video, duration=0.2)
        time.sleep(0.1)
        pyautogui.click(*Coord.second_video, duration=0.2)
        time.sleep(0.5)
        find_and_click('src\\ahead.png')
        time.sleep(0.1)
        find_and_click('src\\approve_sending.png')
        time.sleep(0.1)
        find_and_click('src\\send.png')

    time.sleep(2)
    while True:
        time.sleep(0.1)
        if pyautogui.locateOnScreen('src\\sending_arrow.png', confidence=0.7) is None:
            break

def click_and_send_by_img(nicknames: list[str]):
    time.sleep(1)
    start_bluestacks()

    for count, nickname in enumerate(nicknames, start=1):
        # sleeping after 10 users
        if count % 10 == 0:
            sleep_time = randint(60, 180)
            log(f'(-_-) {slip} for {sleep_time} seconds')
            time.sleep(sleep_time)

        # refrtesh app after 25 users
        if count % 25 == 0:
            log(f'{refresh}')
            clouse_bluestacks() # close app
            time.sleep(2)
            start_bluestacks() # start app

        # search btn on main screen and find line to search
        find_and_click('src\\grey_search_btn.png')
        time.sleep(0.4)
        find_and_click('src\\search.png', confidence=0.6)
        time.sleep(1.5)

        # user iteration
        for letter in nickname:
            pyautogui.write(letter, interval=0.1)


        not_found = False
        start = datetime.now().timestamp()
        while True:
            estimate = datetime.now().timestamp() - start

            if estimate >= 4: # if the waiting time exceeds the specified value, then click on the first elemtnt
                if pyautogui.locateOnScreen('src\\not_found_user.png', confidence=0.7): # not found user
                    not_found = True
                    break
                pyautogui.click(*Coord.click_found_first, duration=0.2) # click on first line
                break

            if (btn := list(pyautogui.locateAllOnScreen('src\\search_img_after_serching.png', confidence=0.9))): # list icon "LUPA"
                if pyautogui.locateOnScreen('src\\not_found_nickname.png') or pyautogui.locateOnScreen('src\\not_found_nickname_2.png'): # not found user
                    not_found = True
                    break
                else: # selection depending on the number of icon "LUPA"
                    if len(btn) == 1:
                        pyautogui.click(*Coord.click_found_second, duration=0.2) # first element "LUPA", select second row
                    elif len(btn) == 2:
                        pyautogui.click(758, 280, duration=0.2) # first and second elements "LUPA", select third row
                    elif len(btn) == 3:
                        pyautogui.click(760, 340, duration=0.2) # first, second and third elements "LUPA", select fourth row
                    elif not btn: 
                        pyautogui.click(*Coord.click_found_first, duration=0.2) # select first element
                break

        if not_found: # condition check (not_found)
            send_failed(nickname)
            find_and_click('src\\back_btn.png')
            log(f"not_found {nickname}")
            continue
                
        # find button "Сообщение", if there is no button, then the account is closed 
        is_only_subscribe = False
        start = datetime.now().timestamp()
        while True:
            estimate = datetime.now().timestamp() - start
            if estimate >= 6:
                is_only_subscribe = True
                break
            if (message := pyautogui.locateOnScreen('src\\message_btn.png', confidence=0.6)): # button "Сообщение"
                pyautogui.click(message, duration=0.2) # you went to direct
                break
        if is_only_subscribe:
            send_failed(nickname)
            log(f'({count}) {failed} closed profile -> {nickname}')
            continue

        # you can go to messages but you can't write
        is_private = False
        start = datetime.now().timestamp()
        while True:
            estimate = datetime.now().timestamp() - start
            if estimate >= 6:
                is_private = True
                break
            else:
                # click on upload btn in chat
                if (upload_btn := pyautogui.locateOnScreen('src\\upload_btn.png', confidence=0.6)):
                    btn = pyautogui.locateOnScreen('src\\upload_btn_in_chat.png', confidence=0.6)
                    pyautogui.click(btn, duration=0.2)
                    break

        # account privacy check  
        if is_private:
            send_failed(nickname)
            log(f"({count}) {failed} can't send message-> {nickname}")
            find_and_click('src\\back_btn.png')
            continue
        
        # when you first open the application, it requires permission to send files, and so on.
        time.sleep(1)
        if pyautogui.locateOnScreen('src\\allow.png', confidence=0.6):
            find_and_click('src\\allow.png') # btn "Разрешить"
            time.sleep(0.5)
            find_and_click('src\\allow.png') # btn "Разрешить"
            time.sleep(0.5)
            find_and_click('src\\allow.png') # btn "Разрешить"
            time.sleep(0.5)

        # tracking the icon and when it is there, the elements for sending are selected and sent
        while True:
            time.sleep(0.1)
            if pyautogui.locateOnScreen('src\\icon_to_wait.png', confidence=0.7):
                time.sleep(0.1)    
                pyautogui.click(750, 450, duration=0.2) # first element
                time.sleep(0.2)
                pyautogui.click(950, 450, duration=0.2) # second element
                time.sleep(0.2)
                find_and_click('src\\send_btn.png') # send btn
                time.sleep(1)
                break
        
        # tracking the send icon ->
        while True:
            time.sleep(0.1)
            if pyautogui.locateOnScreen('src\\sending_arrow.png', confidence=0.7) is None:
                break
        
        # tracking the failed sending icon (x)
        is_banned = False
        while True:
            time.sleep(1.5)
            if pyautogui.locateOnScreen('src\\failed_sanding.png', confidence=0.8):
                is_banned = True
                log(f"{ban}")
                find_and_click('src\\back_btn.png')
                change_account()
                break
            else:
                break
        if is_banned: # adding an username to the end of the list if an error occurred on this user
            with open('users.txt', 'r+', encoding='utf-8') as file:
                data = file.read().split('\n')
                data.remove(nickname)
                file.seek(0)
                for d in data:
                    file.write(f'{d}\n')
                file.truncate()
            with open('users.txt', 'a', encoding='utf-8') as file:
                file.write(f'\n{nickname}')
            continue

        log(f'({count}) {success} -> {nickname}')
        send_success(nickname)
        find_and_click('src\\back_btn.png') # back btn
        find_and_click('src\\back_btn.png') # back btn
        find_and_click('src\\back_btn.png') # back btn
        time.sleep(0.5)

    log(f'{done}')
        
def main():
    # print(pyautogui.displayMousePosition())
    from_txt_to_json()
    click_and_send_by_img(nicknames=get_users())
    
if __name__ == '__main__':
    main()