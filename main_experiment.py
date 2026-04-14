#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Libraries
import os
import numpy as np
import pandas as pd
from pdf2image import convert_from_path
from itertools import permutations
from psychopy.visual import Window, ImageStim
from psychopy.visual.shape import ShapeStim
from psychopy.visual.textbox2 import TextBox2
from psychopy.core import Clock, quit, wait
from psychopy.hardware.keyboard import Keyboard
from psychopy.event import Mouse

## Experiment Settings
participant_ID = input("Participant ID: ")
condition = np.random.choice([0,1,2], size=1)
path = f"data/data_{participant_ID}.csv"
df = pd.DataFrame(columns=["id", "block", "trial", "stimA", "stimB", "choice"])

win = Window(monitor="testMonitor", fullscr = True, size=(2880, 1800), color=[1,1,1]) # White Window
max_wait = 4

## PC Objects
kb = Keyboard()
clock = Clock()
rng = np.random.default_rng()

## Instruction objects

instructions = convert_from_path("instructions2.pdf")
instruction = ImageStim(win, image=instructions[0])
spacebar_instruction = TextBox2(win, "Press Spacebar to Continue", letterHeight=0.05,
                                alignment='center', color="black", pos=(0, -0.7),
                                units='norm', font="Liberation Serif", size=(None, 0.06))


## Key Guides

key_guide_d = TextBox2(win, "D", pos=(-0.6, -0.2), units='norm', letterHeight=0.05,
                       alignment='center', color="black", font="Liberation Serif",
                       size=(None, 0.06))
key_guide_k = TextBox2(win, "K", pos=(0.6, -0.2), units='norm', letterHeight=0.05,
                       alignment='center', color="black", font="Liberation Serif",
                       size=(None, 0.06))

# method to set autoDraw for both key guides at the same time
guides = [key_guide_d, key_guide_k]

## Citrus Images (Practice)

citrus_files = ["stimuli/citrus/" + file for file in os.listdir("stimuli/citrus")]
left_image = ImageStim(win, image=citrus_files[0], pos=(-0.35, -0.2), units='norm',
                       size=(0.35, None))
left_border = ShapeStim(win, vertices=left_image.verticesPix, units="pix", 
                        lineColor=(0,0,1), fillColor=None, colorSpace='rgb')
left_caption = TextBox2(win, "CITRUS FRUIT A", pos=(-0.35, 0.2), units='norm', 
                        letterHeight=0.05, alignment='center', color="black", 
                        font="Liberation Serif", size=(None, 0.06))
right_image = ImageStim(win, image=citrus_files[1], pos=(0.35, -0.2), units='norm',
                        size=(0.35, None))
right_border = ShapeStim(win, vertices=right_image.verticesPix, units="pix", 
                         lineColor=(0,0,1), fillColor=None, colorSpace='rgb')
right_caption = TextBox2(win, "CITRUS FRUIT B", pos=(0.35, 0.2), units='norm', 
                         letterHeight=0.05, alignment='center', color="black", 
                         font="Liberation Serif",size=(None, 0.06))

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
ref_image = ImageStim(win, image="stimuli/dogs/dog_reference.png", pos=(0, 0.5),
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
                                 font="Liberation Serif", size=(None, 0.06), borderColor='black')

citrus_timeout = TextBox2(win,
                          "You have not yet responded, we really care about your response!", color='black', letterHeight=0.07, font="Liberation Serif")

citrus_run = True
if citrus_run:
    instruction.autoDraw = True
    spacebar_instruction.autoDraw = True
    for i in range(5):
        instruction.setImage(instructions[i])
        win.flip()
        press = kb.waitKeys(keyList=["space"])
    instruction.autoDraw = False
    spacebar_instruction.autoDraw = False

    citrus_question.autoDraw = True
    for file in range(3):
        if citrus_pairs[file][0] == citrus_pairs[file][1]:
            keylist = ["q"]
            citrus_question.text = "Press Q"
        else:
            keylist = ["d", "k"]
            citrus_question.text = "Which of the two citrus fruits do YOU LIKE MORE?"
        left_image.setImage(citrus_pairs[file][0])
        right_image.setImage(citrus_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        win.flip()
        clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False,
                            clear=True)
        if press == None:
            citrus_timeout.draw()
            win.flip()
            wait(2)
            left_image.setImage(citrus_pairs[file][0])
            right_image.setImage(citrus_pairs[file][1])
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            clock.reset()
            press = kb.waitKeys(keyList=keylist, waitRelease=False)
        elif press[-1].name == "d":
            left_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        elif press[-1].name == "k":
            right_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        else:
            left_border.draw()
            right_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        # data = pd.DataFrame({"id": participant_ID, "condition": condition[0], 
        #                      "block": "citrus", "trial": file, "stimA": dog_pairs[file][0],
        #                      "stimB":dog_pairs[file][1], "choice": press[-1].name, "rt": press[-1].rt})
        # data.to_csv(path)

    citrus_question.autoDraw = False

## Part 2: Dog Liking (Main Task 1)

left_caption.text = "ROBOTIC DOG A"
right_caption.text = "ROBOTIC DOG B"
condition_text = ["COMPANIONSHIP", "CARE AND SUPPORT", "SAFETY AND SECURITY"]
dog_question1_text = f"Imagine you are looking for a robotic dog used for \
{condition_text[condition[0]]} \n Which of the two robotic dogs do YOU LIKE MORE?"
dog_question1 = TextBox2(win, dog_question1_text, 
                         pos=(0, 0.7), units='norm', letterHeight=0.05,
                         alignment='center', color="black",
                         font="Liberation Serif", size=(None, 0.18), borderColor='black')

instruction_numbers = [5, 6 + condition[0], 9, 10, 11]

dog_timeout = TextBox2(win,"You have not yet responded, we really care about your response!",
                       color='black', letterHeight=0.07, font="Liberation Serif")


main1 = True
if main1:
    for i in instruction_numbers:
        instruction.setImage(instructions[i])
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space"])

    dog_question1.autoDraw = True
    for file in range(3):
        if dog_pairs[file][0] == dog_pairs[file][1]:
            keylist = ["q"]
            dog_question1.text = "Press Q"
        else:
            keylist = ["d", "k"]
            dog_question1.text = dog_question1_text
        left_image.setImage(dog_pairs[file][0])
        right_image.setImage(dog_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        win.flip()
        clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            dog_timeout.draw()
            win.flip()
            wait(1)
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            clock.reset()
            press = kb.waitKeys(keyList=keylist, waitRelease=False)
        elif press[-1].name == "d":
            left_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        elif press[-1].name == "k":
            right_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        else:
            left_border.draw()
            right_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        # data = pd.DataFrame({"id": participant_ID, "condition": condition[0], 
        #                      "block": "citrus", "trial": file, "stimA": dog_pairs[file][0],
        #                      "stimB":dog_pairs[file][1], "choice": press[-1].name, "rt": press[-1].rt})
        # data.to_csv(path)
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
                         font="Liberation Serif", size=(None, 0.18), borderColor='black')

main2 = True
if main2:
    np.random.shuffle(dog_pairs)
    for i in range(13, 15):
        instruction.setImage(instructions[i])
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space"])

    dog_question2.autoDraw = True
    for file in range(3):
        if dog_pairs[file][0] == dog_pairs[file][1]:
            keylist = ["q"]
            dog_question2.text = "Press Q"
        else:
            keylist = ["d", "k"]
            dog_question2.text = dog_question2_text
        left_image.setImage(dog_pairs[file][0])
        right_image.setImage(dog_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        win.flip()
        clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            dog_timeout.draw()
            win.flip()
            wait(1)
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            clock.reset()
            press = kb.waitKeys(keyList=keylist, waitRelease=False)
        elif press[-1].name == "d":
            left_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        elif press[-1].name == "k":
            right_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        else:
            left_border.draw()
            right_border.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        # data = pd.DataFrame({"id": participant_ID, "condition": condition[0], 
        #                      "block": "citrus", "trial": file, "stimA": dog_pairs[file][0],
        #                      "stimB":dog_pairs[file][1], "choice": press[-1].name, "rt": press[-1].rt})
        # data.to_csv(path)
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
                         pos=(0, 0.85), units='norm', letterHeight=0.05,
                         alignment='center', color="black",
                         font="Liberation Serif", size=(None, 0.18), 
                         borderColor='black')

main3 = True
if main3:
    np.random.shuffle(dog_pairs)
    for i in range(16, 19):
        instruction.setImage(instructions[i])
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space"])

    dog_question3.autoDraw = True
    for file in range(3):
        if dog_pairs[file][0] == dog_pairs[file][1]:
            keylist = ["q"]
            dog_question3.text = "Press Q"
        else:
            keylist = ["d", "k"]
            dog_question3.text = dog_question3_text
        left_image.setImage(dog_pairs[file][0])
        right_image.setImage(dog_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        ref_image.draw()
        win.flip()
        clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            dog_timeout.draw()
            win.flip()
            wait(1)
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            clock.reset()
            press = kb.waitKeys(keyList=keylist, waitRelease=False)
        elif press[-1].name == "d":
            left_border.draw()
            ref_image.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        elif press[-1].name == "k":
            right_border.draw()
            ref_image.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        else:
            left_border.draw()
            right_border.draw()
            ref_image.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            win.flip()
            wait(0.3)
        # data = pd.DataFrame({"id": participant_ID, "condition": condition[0], 
        #                      "block": "citrus", "trial": file, "stimA": dog_pairs[file][0],
        #                      "stimB":dog_pairs[file][1], "choice": press[-1].name, "rt": press[-1].rt})
        # data.to_csv(path)
    dog_question3.autoDraw = False

## Part 5: Demographics



win.close()
quit()
