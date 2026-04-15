#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Libraries
import os
import numpy as np
import pandas as pd
from psychopy import core
from psychopy.visual import Window, ImageStim
from psychopy.visual.shape import ShapeStim
from psychopy.visual.textbox2 import TextBox2
from psychopy.visual.slider import Slider
from psychopy.hardware.keyboard import Keyboard
from psychopy.event import Mouse

## PC Objects

win = Window(monitor="testMonitor", fullscr = True, color=[1,1,1]) # White Window
mouse = Mouse()
kb = Keyboard()
clock = core.Clock()
rng = np.random.default_rng()
font = 'Liberation Serif'

## Experiment Settings
def screen_input(question: str):
    typed_text = ''
    text_completed = False
    question_box = TextBox2(win, question, color='black', letterHeight=0.05,
                            units='norm', pos=(0, 0.25), font=font, 
                            alignment='center', size=(None, 0.06))
    finish_box = TextBox2(win, "Press ENTER to continue", color='black', 
                          letterHeight=0.05,units='norm', pos=(0, -0.25), 
                          font=font, alignment='center', size=(None, 0.06))
    show_text = TextBox2(win, typed_text, color='blue', letterHeight=0.05,
                         units = 'norm', alignment='center', size=(None, 0.06))
    question_box.draw()
    finish_box.draw()
    show_text.draw()
    win.flip()
    while not text_completed:
        pressed=kb.waitKeys()
        if pressed[-1].name == 'escape':
            win.close()
            core.quit()
        elif pressed[-1].name == 'return':
            text_completed = True
        elif pressed[-1].name == 'space':
            typed_text = typed_text + " "
        elif pressed[-1].name == 'backspace':
            typed_text = typed_text[:-1]
        else:
            typed_text = typed_text + pressed[-1].name
        show_text.text = typed_text

        question_box.draw()
        finish_box.draw()
        show_text.draw()
        win.flip()
    return typed_text

participant_ID = screen_input("Participant ID: ")
condition = np.random.choice([0,1,2], size=1)
path = f"data/data_{participant_ID}.csv"
df = pd.DataFrame(columns=["id", "block", "trial", "stimA", "stimB", "choice"])

max_wait = 4



## Instruction objects

instructions = ["instructions/images/instruction0001-" + str(i) + ".png" for i in range(1,23)]
instruction = ImageStim(win, image=instructions[0], size=(None, 1.7), units='norm')
spacebar_instruction = TextBox2(win, "Press SPACE to Continue", letterHeight=0.05,
                                alignment='center', color="black", pos=(0, -0.7),
                                units='norm', font=font, 
                                size=(None, 0.06))

## Key Guides

key_guide_d = TextBox2(win, "D", pos=(-0.5, -0.7), units='norm', letterHeight=0.05,
                       alignment='center', color="black", font=font,
                       size=(None, 0.06))
key_guide_k = TextBox2(win, "K", pos=(0.5, -0.7), units='norm', letterHeight=0.05,
                       alignment='center', color="black", font=font,
                       size=(None, 0.06))

# method to set autoDraw for both key guides at the same time
guides = [key_guide_d, key_guide_k]

## Citrus Images (Practice)

citrus_files = ["stimuli/citrus/" + file for file in os.listdir("stimuli/citrus")]
left_image = ImageStim(win, image=citrus_files[0], pos=(-0.5, -0.2), units='norm',
                       size=(0.5, None))
left_border = ShapeStim(win, vertices=left_image.verticesPix, units="pix", 
                        lineColor=(0,0,1), fillColor=None, colorSpace='rgb',
                        lineWidth=4)
left_caption = TextBox2(win, "CITRUS FRUIT A", pos=(-0.5, 0.3), units='norm', 
                        letterHeight=0.05, alignment='center', color="black", 
                        font=font, size=(None, 0.06))
right_image = ImageStim(win, image=citrus_files[1], pos=(0.5, -0.2), units='norm',
                        size=(0.5, None))
right_border = ShapeStim(win, vertices=right_image.verticesPix, units="pix", 
                         lineColor=(0,0,1), fillColor=None, colorSpace='rgb', 
                         lineWidth=4)
right_caption = TextBox2(win, "CITRUS FRUIT B", pos=(0.5, 0.3), units='norm', 
                         letterHeight=0.05, alignment='center', color="black", 
                         font=font,size=(None, 0.06))

# Method to set autoDraw for both images and captions at the same time
images = [left_image, right_image, left_caption, right_caption]

citrus_pairs = [np.random.choice([citrus_files[x], citrus_files[y]], 2, replace=False) \
                for y in range(len(citrus_files)) \
                    for x in range(y + 1, len(citrus_files))]
extra_fruit = np.random.choice(citrus_files, 1)
citrus_pairs.append([extra_fruit[0], extra_fruit[0]])
np.random.shuffle(citrus_pairs)

## Dog Images (Main Task)

dog_files = ["stimuli/dogs/dog" + str(i) + ".png" for i in range(1,9)]
ref_image = ImageStim(win, image="stimuli/dogs/dog_reference.png", pos=(0, 0.4),
                      units='norm', size=(0.35, None))
dog_pairs = [np.random.choice([dog_files[x], dog_files[y]], 2, replace=False) \
                for y in range(len(dog_files)) \
                    for x in range(y + 1, len(dog_files))]
extra_dogs = np.random.choice(dog_files, 1)
dog_pairs.append([extra_dogs[0], extra_dogs[0]])
np.random.shuffle(dog_pairs)

## Part 1: Citrus Block (Practice)

citrus_question = TextBox2(win, "Which of the two citrus fruits do YOU LIKE MORE?", 
                                 pos=(0, 0.7), units='norm', letterHeight=0.05,
                                 alignment='center', color="black",
                                 font=font, size=(None, 0.06), borderColor='black')

citrus_timeout = TextBox2(win,
                          "You have not yet responded, we really care about your response!", color='black', letterHeight=0.07, font=font)

citrus_run = True
if citrus_run:
    for i in range(1, 5):
        instruction.setImage(instructions[i])
        instruction.draw()
        win.flip()
        core.wait(1)
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()

        press = kb.waitKeys(keyList=["space", "escape"])
        if press[-1].name == 'escape':
            win.close()
            core.quit()

    citrus_question.autoDraw = True
    for file in range(len(citrus_pairs)):
        if citrus_pairs[file][0] == citrus_pairs[file][1]:
            keylist = ["q", "escape"]
            citrus_question.text = "This is an attention check, please press Q"
        else:
            keylist = ["d", "k", "escape"]
            citrus_question.text = "Which of the two citrus fruits do YOU LIKE MORE?"
        left_image.setImage(citrus_pairs[file][0])
        right_image.setImage(citrus_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        win.flip()
        kb.clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False,
                            clear=True)
        if press == None:
            choice = "timeout"
            rt = max_wait
            citrus_timeout.draw()
            win.flip()
            core.wait(2)
        elif press[-1].name == 'escape':
            win.close()
            core.quit()()
        elif press[-1].name == "d":
            choice = "d"
            rt = press[-1].rt
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            win.flip()
            core.wait(0.3)
        elif press[-1].name == "k":
            choice = "k"
            rt = press[-1].rt
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            right_border.draw()
            win.flip()
            core.wait(0.3)
        else:
            choice = "q"
            rt = press[-1].rt
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            right_border.draw()
            win.flip()
            core.wait(0.3)
        data = pd.DataFrame({"id": [participant_ID], "condition": [condition[0]], 
                             "block": ["citrus"], "trial": [file], "stimA": [citrus_pairs[file][0]],
                             "stimB":[citrus_pairs[file][1]], "choice": [choice],
                             "rt": [rt]})
        if file == 0:
            header = True
        else:
            header = False
        data.to_csv(path, mode="a", header = header)

    citrus_question.autoDraw = False

## Part 2: Dog Liking (Main Task 1)

left_caption.text = "ROBOTIC DOG A"
right_caption.text = "ROBOTIC DOG B"

condition_text = ["COMPANIONSHIP", "CARE AND SUPPORT", "SECURITY"]

dog_question1_text = f"Imagine you are looking for a robotic dog used for \
{condition_text[condition[0]]} \n Which of the two robotic dogs do YOU LIKE MORE?"
dog_question1 = TextBox2(win, dog_question1_text, 
                         pos=(0, 0.7), units='norm', letterHeight=0.05,
                         alignment='center', color="black",
                         font=font, size=(None, 0.18), borderColor='black')

instruction_numbers = [5, 6 + condition[0], 9, 10, 11]

dog_timeout = TextBox2(win,"You have not yet responded, we really care about your response!",
                       color='black', letterHeight=0.07, font=font)

main1 = True
if main1:
    for i in instruction_numbers:
        instruction.setImage(instructions[i])
        instruction.draw()
        win.flip()
        core.wait(3)
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space", "escape"])
        if press[-1].name == 'escape':
            win.close()
            core.quit()()

    dog_question1.autoDraw = True
    for file in range(len(dog_pairs)):
        if dog_pairs[file][0] == dog_pairs[file][1]:
            keylist = ["q", "escape"]
            dog_question1.text = "This is an attention check, please press Q"
        else:
            keylist = ["d", "k", "escape"]
            dog_question1.text = dog_question1_text
        left_image.setImage(dog_pairs[file][0])
        right_image.setImage(dog_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        win.flip()
        kb.clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            choice = "timeout"
            rt = max_wait
            dog_timeout.draw()
            win.flip()
            core.wait(1)
        elif press[-1].name == 'escape':
            win.close()
            core.quit()()
        elif press[-1].name == "d":
            choice = "d"
            rt = press[-1].rt
            left_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            core.wait(0.3)
        elif press[-1].name == "k":
            choice = "k"
            rt = press[-1].rt
            right_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            core.wait(0.3)
        else:
            choice = "q"
            rt = press[-1].rt
            left_border.draw()
            right_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            core.wait(0.3)
        data = pd.DataFrame({"id": [participant_ID], "condition": [condition[0]], 
                             "block": ["dog1"], "trial": [file], "stimA": [dog_pairs[file][0]],
                             "stimB":[dog_pairs[file][1]], "choice": [choice],
                             "rt": [rt]})
        data.to_csv(path, mode="a", header = False)
    dog_question1.autoDraw = False


## Part 3: Dog Eeriness (Main Task 2)

dog_pairs = [np.random.choice([dog_files[x], dog_files[y]], 2, replace=False) \
                for y in range(len(dog_files)) \
                    for x in range(y + 1, len(dog_files))]
extra_dogs = np.random.choice(dog_files, 1)
dog_pairs.append([extra_dogs[0], extra_dogs[0]])
np.random.shuffle(dog_pairs)

dog_question2_text = f"Imagine you are looking for a robotic dog used for \
{condition_text[condition[0]]} \n Which of the two robotic dogs FEELS MORE EERIE?"
dog_question2 = TextBox2(win, dog_question2_text, 
                         pos=(0, 0.7), units='norm', letterHeight=0.05,
                         alignment='center', color="black",
                         font=font, size=(None, 0.18), borderColor='black')

main2 = True
if main2:
    for i in range(13, 15):
        instruction.setImage(instructions[i])
        instruction.draw()
        win.flip()
        core.wait(3)
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space", "escape"])
        if press[-1].name == 'escape':
            win.close()
            core.quit()()

    dog_question2.autoDraw = True
    for file in range(len(dog_pairs)):
        if dog_pairs[file][0] == dog_pairs[file][1]:
            keylist = ["q", "escape"]
            dog_question2.text = "This is an attention check, please press Q"

        else:
            keylist = ["d", "k", "escape"]
            dog_question2.text = dog_question2_text
        left_image.setImage(dog_pairs[file][0])
        right_image.setImage(dog_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        win.flip()
        kb.clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            choice = "timeout"
            rt = max_wait
            dog_timeout.draw()
            win.flip()
            core.wait(1)
        elif press[-1].name == 'escape':
            win.close()
            core.quit()()
        elif press[-1].name == "d":
            choice = "d"
            rt = press[-1].rt
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            win.flip()
            core.wait(0.3)
        elif press[-1].name == "k":
            choice = "k"
            rt = press[-1].rt
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            right_border.draw()
            win.flip()
            core.wait(0.3)
        else:
            choice = "q"
            rt = press[-1].rt
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            right_border.draw()
            win.flip()
            core.wait(0.3)
        data = pd.DataFrame({"id": [participant_ID], "condition": [condition[0]], 
                             "block": ["dog2"], "trial": [file], "stimA": [dog_pairs[file][0]],
                             "stimB":[dog_pairs[file][1]], "choice": [choice],
                             "rt": [rt]})
        data.to_csv(path, mode="a", header = False)
    dog_question2.autoDraw = False
            

## Part 4: Dog comparison (Main Task 3)

dog_pairs = [np.random.choice([dog_files[x], dog_files[y]], 2, replace=False) \
                for y in range(len(dog_files)) \
                    for x in range(y + 1, len(dog_files))]
extra_dogs = np.random.choice(dog_files, 1)
dog_pairs.append([extra_dogs[0], extra_dogs[0]])
np.random.shuffle(dog_pairs)

dog_question3_text = "Your task is to decide which of the two robotic dogs is " \
"MORE SIMILAR to the dog on top."
dog_question3 = TextBox2(win, dog_question3_text, 
                         pos=(0, 0.8), units='norm', letterHeight=0.05,
                         alignment='center', color="black",
                         font=font, size=(None, 0.18), 
                         borderColor='black')

main3 = True
if main3:
    for i in range(16, 19):
        instruction.setImage(instructions[i])
        instruction.draw()
        win.flip()
        core.wait(3)
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space"])

    dog_question3.autoDraw = True
    for file in range(len(dog_pairs)):
        if dog_pairs[file][0] == dog_pairs[file][1]:
            keylist = ["q", "escape"]
            dog_question3.text = "This is an attention check, please press Q"
        else:
            keylist = ["d", "k", "escape"]
            dog_question3.text = dog_question3_text
        left_image.setImage(dog_pairs[file][0])
        right_image.setImage(dog_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        ref_image.draw()
        win.flip()
        kb.clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            choice = "timeout"
            rt = max_wait
            dog_timeout.draw()
            win.flip()
            core.wait(1)
        elif press[-1].name == "escape":
            win.close()
            core.quit()()
        elif press[-1].name == "d":
            choice = "d"
            rt = press[-1].rt
            ref_image.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            win.flip()
            core.wait(0.3)
        elif press[-1].name == "k":
            choice = "k"
            rt = press[-1].rt
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            right_border.draw()
            ref_image.draw()
            win.flip()
            core.wait(0.3)
        else:
            choice = "q"
            rt = press[-1].rt
            ref_image.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            right_border.draw()
            win.flip()
            core.wait(0.3)
        data = pd.DataFrame({"id": [participant_ID], "condition": [condition[0]], 
                             "block": ["dog3"], "trial": [file], "stimA": [dog_pairs[file][0]],
                             "stimB":[dog_pairs[file][1]], "choice": [press[-1].name],
                             "rt": [press[-1].rt]})
        data.to_csv(path, mode="a", header = False)
    dog_question3.autoDraw = False

## Part 5: Demographics

data = pd.read_csv(path)

data['age'] = screen_input("Please input your age:")

## Gender

gender_instruction = TextBox2(win, "Please indicate your gender by clicking one " \
                              "of the boxes below", 
                              letterHeight=0.05, alignment='center', 
                              color="black", pos=(0, 0.7), units='norm', 
                              font=font, size=(None, 0.2),
                              borderColor='black', borderWidth=2)

male_box = TextBox2(win, "Male", letterHeight=0.05,
                    alignment='center', color="black", pos=(-0.5, 0),
                    units='norm', font=font, 
                    size=(0.4, 0.4), fillColor='lightGrey')

female_box = TextBox2(win, "Female", letterHeight=0.05,
                      alignment='center', color="black", pos=(0, 0),
                      units='norm', font=font, 
                      size=(0.4, 0.4), fillColor='lightGrey')

neither_box = TextBox2(win, "Non-Binary /\nPrefer not to respond", letterHeight=0.05,
                       alignment='center', color="black", pos=(0.5, 0),
                       units='norm', font=font, 
                       size=(0.4, 0.4), fillColor='lightGrey')

boxes = [male_box, female_box, neither_box]

done = False
mouse.clickReset()

while done == False:
    gender_instruction.draw()
    [box.draw() for box in boxes]
    win.flip()
    if mouse.isPressedIn(male_box, buttons=[0]):
        data['gender'] = "male"
        male_box.fillColor = 'lightBlue'
        gender_instruction.draw()
        [box.draw() for box in boxes]
        win.flip()
        core.wait(0.2)
        done = True
    elif mouse.isPressedIn(female_box, buttons=[0]):
        data['gender'] = "female"
        female_box.fillColor = 'lightBlue'
        gender_instruction.draw()
        [box.draw() for box in boxes]
        win.flip()
        core.wait(0.2)
        done = True
    elif mouse.isPressedIn(neither_box, buttons=[0]):
        data['gender'] = "X"
        neither_box.fillColor = 'lightBlue'
        gender_instruction.draw()
        [box.draw() for box in boxes]
        win.flip()
        core.wait(0.2)
        done=True
    else:
        continue
    keys = kb.getKeys()
    if 'escape' in keys:
        win.close()
        core.quit()()

## Likert Questions

likert_instruction = TextBox2(win, "Please indicate your familiarity with " \
                              "robotic dogs by dragging and dropping the round " \
                              "markers.", 
                              letterHeight=0.05, alignment='center', 
                              color="black", pos=(0, 0.7), units='norm', 
                              font=font, size=(None, 0.2),
                              borderColor='black', borderWidth=2)

enter_instruction = TextBox2(win, "Press enter to Continue", letterHeight=0.05,
                             alignment='center', color="black", pos=(0, -0.7),
                             units='norm', font=font, 
                             size=(None, 0.06))

s1 = "To what extent are you familiar with robotic dogs?"
s2 = "To what extent are you familiar with robots in the health domain (online or in real life) "

statement1 = TextBox2(win, s1, pos=(0, 0.4), letterHeight=0.04, size=(1, 0.15),
                      color='black', font=font)
statement2 = TextBox2(win, s2, pos=(0, -0.3), letterHeight=0.04, size=(1, 0.15),
                      color='black', font=font)

statements = [statement1, statement2]

slider1 = Slider(win, ticks=(1,2,3,4,5,6,7), granularity=1, size=(1, 0.05),
                labels=['strongly agree', 'strongly disagree'], color='black',
                lineColor='black', startValue=4, pos=(0, 0.3), labelHeight=0.04,
                labelWrapWidth=1, markerColor='black', font=font)
slider2 = Slider(win, ticks=(1,2,3,4,5,6,7), granularity=1, size=(1, 0.05),
                labels=['strongly agree', 'strongly disagree'], color='black',
                lineColor='black', startValue=4, pos= (0, -0.4), labelHeight=0.04,
                labelWrapWidth=1, markerColor='black', font=font)

sliders = [slider1, slider2]

done = False

while done is False:
    likert_instruction.draw()
    enter_instruction.draw()
    [slider.draw() for slider in sliders]
    [statement.draw() for statement in statements]
    win.flip()
    slider_values = [slider.getRating() for slider in sliders]
    for slider in sliders:
        if slider.rating:
            slider.markerColor = 'blue'
    
    if kb.getKeys(keyList='escape'):
        win.close()
        core.quit()()
    elif kb.getKeys(keyList='return') and not None in slider_values:
        done = True

data['familiarity'] = slider_values[0]
data['familiarity_health'] = slider_values[1]

likert_instruction.text = "Please indicate how strongly you agree or  disagree " \
"with these statements by dragging and dropping the round markers."

s1 = "It is absurd to consider a robotic dog and a dog to be the same kind of thing."
s2 = "Even if a robotic dog might one day look and move the same as a real dog, it would never be anything like a real dog."
s3 = "It would be alright if someday we could not tell robotic dogs from real dogs."
s4 = "Robotic dogs are fundamentally different from dogs."

statement1 = TextBox2(win, s1, pos=(0, 0.5), letterHeight=0.04, size=(1, 0.15),
                      color='black', font=font)
statement2 = TextBox2(win, s2, pos=(0, 0.2), letterHeight=0.04, size=(1, 0.15),
                      color='black', font=font)
statement3 = TextBox2(win, s3, pos=(0, -0.1), letterHeight=0.04, size=(1, 0.15),
                      color='black', font=font)
statement4 = TextBox2(win, s4, pos=(0, -0.4), letterHeight=0.04, size=(1, 0.15),
                      color='black', font=font)

statements = [statement1, statement2, statement3, statement4]

slider1 = Slider(win, ticks=(1,2,3,4,5,6,7), granularity=1, size=(1, 0.05),
                labels=['strongly agree', 'strongly disagree'], color='black',
                lineColor='black', startValue=4, pos=(0, 0.4), labelHeight=0.04,
                labelWrapWidth=1, markerColor='black', font=font)
slider2 = Slider(win, ticks=(1,2,3,4,5,6,7), granularity=1, size=(1, 0.05),
                labels=['strongly agree', 'strongly disagree'], color='black',
                lineColor='black', startValue=4, pos= (0, 0.1), labelHeight=0.04,
                labelWrapWidth=1, markerColor='black', font=font)
slider3 = Slider(win, ticks=(1,2,3,4,5,6,7), granularity=1, size=(1, 0.05),
                labels=['strongly agree', 'strongly disagree'], color='black',
                lineColor='black', startValue=4, pos=(0, -0.2), labelHeight=0.04,
                labelWrapWidth=1, markerColor='black', font=font)
slider4 = Slider(win, ticks=(1,2,3,4,5,6,7), granularity=1, size=(1, 0.05),
                labels=['strongly agree', 'strongly disagree'], color='black',
                lineColor='black', startValue=4, pos=(0, -0.5), labelHeight=0.04,
                labelWrapWidth=1, markerColor='black', font=font)

sliders = [slider1, slider2, slider3, slider4]

done = False

while done is False:
    likert_instruction.draw()
    enter_instruction.draw()
    [slider.draw() for slider in sliders]
    [statement.draw() for statement in statements]
    win.flip()
    slider_values = [slider.getRating() for slider in sliders]
    for slider in sliders:
        if slider.rating:
            slider.markerColor = 'blue'
    
    if kb.getKeys(keyList='escape'):
        win.close()
        core.quit()()
    elif kb.getKeys(keyList='return') and not None in slider_values:
        done = True

data['uniqueness_1'] = slider_values[0]
data['uniqueness_2'] = slider_values[1]
data['uniqueness_3'] = slider_values[2]
data['uniqueness_4'] = slider_values[3]

for slider in sliders:
    slider.reset()
    slider.markerColor = 'black'

statement1.text = "I feel apprehensive about using technology."
statement2.text = "I have avoided technology because it is unfamiliar to me."
statement3.text = "I am able to keep up with important technological advances."
statement4.text = "I feel anxious when using new technologies."

done = False

while done is False:
    likert_instruction.draw()
    enter_instruction.draw()
    [slider.draw() for slider in sliders]
    [statement.draw() for statement in statements]
    win.flip()
    slider_values = [slider.getRating() for slider in sliders]
    for slider in sliders:
        if slider.rating:
            slider.markerColor = 'blue'
    
    if kb.getKeys(keyList='escape'):
        win.close()
        core.quit()()
    elif kb.getKeys(keyList='return') and not None in slider_values:
        done = True

ending = TextBox2(win, "Thank you for completing this experiment!\n" \
                  "You may now leave the cubicle and inform the experimenter " \
                  "that you are finished.", font=font, letterHeight=0.05, 
                  color = 'black', alignment='center')

data['anxiety_1'] = slider_values[0]
data['anxiety_2'] = slider_values[1]
data['anxiety_3'] = slider_values[2]
data['anxiety_4'] = slider_values[3]

data.to_csv(path, mode = 'w')

ending.draw()
win.flip()
kb.waitKeys(keyList = ['return', 'escape', 'space'])

win.close()
core.quit()
