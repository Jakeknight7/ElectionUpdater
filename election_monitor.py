from selenium import webdriver
from selenium.webdriver.common.by import By
from random import seed
from random import randint
import time
import os
import winsound

class ElectionChecker:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver.exe'))
        self.state = {'Georgia':[["E_Geo", "R_Geo"], 0, 0], 'Pennsylvania':[["E_Pen", "R_Pen"], 0, 0], 'North Carolina':[["E_Nor", "R_Nor"], 0, 0], 'Nevada':[["E_Nev", "R_Nev"], 0, 0], 'Arizona':[["E_Ari", "R_Ari"], 0, 0]}
        self.incomming_message_sound = 'Sound_clips/incoming_message.wav'
        self.sound_clip_directory = os.path.join(os.getcwd(), "Sound_clips")
        seed(int(round(time.time() * 1000)))

    def state_grabber(self, state_name, element):
        holder = element.find_element(By.CLASS_NAME, "brdYAf")
        count = 0
        count = holder.text.split('\n')[1]
        if count == 0:
            return False
        if count != self.state[state_name][1]:
            self.state[state_name][1] = count
            self.state[state_name][2] = 1
            return True
        return False

    def display_update(self):
        print('New Update')
        for name in self.state.keys():
            print(name + ": " + str(self.state[name][1]))
            if self.state[name][2] > 0:
                self.state[name][2] = 0
                index = randint(0,1)
                sound_clip = os.path.join(self.sound_clip_directory, self.state[name][0][index] + ".wav")
                winsound.PlaySound(sound_clip, winsound.SND_NOSTOP)

    def checker(self):
        time.sleep(0.5)
        while(True):
            self.driver.get('https://www.google.com/search?q=election+results&oq=election+re&aqs=chrome.0.0i131i433i457j0i131i433j69i57j0i131i433l5.2091j0j7&sourceid=chrome&ie=UTF-8')
            web_states = self.driver.find_elements_by_xpath('//div[@class="fKE5Bb"]')
            decider = False
            for element in web_states:
                state_holder = element.find_element(By.CLASS_NAME, "PLaf5").text
                if(state_holder in self.state.keys()):
                    return_value = self.state_grabber(state_holder, element)
                    time.sleep(0.5)
                    decider = decider or return_value
            if decider:
                #winsound.PlaySound(self.incomming_message_sound, winsound.SND_ASYNC)
                self.display_update()
            time.sleep(10)

checker = ElectionChecker()
checker.checker()