#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Libraries
import os
import numpy as np
import pandas as pd
from webbrowser import open_new
from psychopy import core
from psychopy.visual import Window, ImageStim
from psychopy.visual.shape import ShapeStim
from psychopy.visual.textbox2 import TextBox2
from psychopy.hardware.keyboard import Keyboard
from psychopy.event import Mouse

## PC Objects

win = Window(monitor="testMonitor", fullscr = True, color=[1,1,1]) # White Window
mouse = Mouse()
kb = Keyboard()
clock = core.Clock()
rng = np.random.default_rng()
font = 'Times New Roman'

## Experiment Settings
def screen_input(question: str, sona = False):
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
            if len(typed_text) == 5 or sona is False:
                text_completed = True
        elif pressed[-1].name == 'space':
            typed_text = typed_text + " "
        elif pressed[-1].name == 'backspace':
            typed_text = typed_text[:-1]
        elif "num_" in pressed[-1].name:
            typed_text = typed_text + pressed[-1].name.replace("num_", "")
        else:
            typed_text = typed_text + pressed[-1].name
        show_text.text = typed_text

        question_box.draw()
        finish_box.draw()
        show_text.draw()
        win.flip()
    return typed_text

participant_ID = screen_input("Welcome! Please fill in your SONA ID to start the task:",
                              sona=True)
condition = [0]
path = f"data/files/data_{participant_ID}.csv"
df = pd.DataFrame(columns=["id", "block", "trial", "stimA", "stimB", "choice"])

max_wait = 4

## Instruction objects

instructions = ["instructions/pages/instruction0001-" + str(i).zfill(2) + ".png" for i in range(1,23)]
instruction = ImageStim(win, image=instructions[0], size=(None, 1.7), units='norm')
spacebar_instruction = TextBox2(win, "Press SPACE to Continue", letterHeight=0.05,
                                alignment='center', color="black", pos=(0, -0.7),
                                units='norm', font=font, 
                                size=(None, 0.06))
instruction_time = 0
instruction_time_long = 0

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

## Arm Images (Main Task)

arm_files = ["stimuli/arms/arm" + str(i) + ".png" for i in range(1,10)]
ref_image = ImageStim(win, image="stimuli/arms/arm_reference.png", pos=(0, 0.2),
                      units='norm', size=(0.35, None))
arm_pairs = [np.random.choice([arm_files[x], arm_files[y]], 2, replace=False) \
                for y in range(len(arm_files)) \
                    for x in range(y + 1, len(arm_files))]
extra_arms = np.random.choice(arm_files, 1)
arm_pairs.append([extra_arms[0], extra_arms[0]])
np.random.shuffle(arm_pairs)

## Attention Check Message

attention_check = TextBox2(win, "This is an attention check, please press Q", 
                           pos=(0, 0.7), units='norm', letterHeight=0.05,
                           alignment='center', color="black",
                           font=font, size=(None, 0.06), borderColor='black')

## Part 1: Citrus Block (Practice)

citrus_question = TextBox2(win, "Which of the two citrus fruits do YOU LIKE MORE?", 
                           pos=(0, 0.7), units='norm', letterHeight=0.05,
                           alignment='center', color="black",
                           font=font, size=(None, 0.06), borderColor='black')

timeout_message = TextBox2(win,
                           "You have not yet responded, we really care about your response!",
                           color='black', letterHeight=0.07, font=font)

citrus_run = True
if citrus_run:
    for i in range(1, 5):
        instruction.setImage(instructions[i])
        instruction.draw()
        win.flip()
        core.wait(instruction_time)
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()

        press = kb.waitKeys(keyList=["space", "escape"])
        if press[-1].name == 'escape':
            win.close()
            core.quit()

    for file in range(len(citrus_pairs)):
        if citrus_pairs[file][0] == citrus_pairs[file][1]:
            keylist = ["q", "escape"]
            attention_check.draw()
        else:
            keylist = ["d", "k", "escape"]
            citrus_question.draw()
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
            timeout_message.draw()
            win.flip()
            core.wait(2)
        elif press[-1].name == 'escape':
            win.close()
            core.quit()()
        elif press[-1].name == "d":
            choice = "d"
            rt = press[-1].rt
            citrus_question.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            win.flip()
            core.wait(0.3)
        elif press[-1].name == "k":
            choice = "k"
            rt = press[-1].rt
            citrus_question.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            right_border.draw()
            win.flip()
            core.wait(0.3)
        else:
            choice = "q"
            rt = press[-1].rt
            attention_check.draw()
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
        df = pd.concat([df, data])
        if file == 0:
            header = True
        else:
            header = False
        data.to_csv(path, mode="a", header = header, index = False)

    citrus_question.autoDraw = False

## Part 2: Arm Liking (Main Task 1)

# Recreate images to set new size
left_image = ImageStim(win, image=arm_files[0], pos=(-0.5, -0.2), units='norm',
                       size=(0.7, None))
left_border = ShapeStim(win, vertices=left_image.verticesPix, units="pix", 
                        lineColor=(0,0,1), fillColor=None, colorSpace='rgb',
                        lineWidth=4)
right_image = ImageStim(win, image=arm_files[1], pos=(0.5, -0.2), units='norm',
                        size=(0.7, None))
right_border = ShapeStim(win, vertices=right_image.verticesPix, units="pix", 
                         lineColor=(0,0,1), fillColor=None, colorSpace='rgb', 
                         lineWidth=4)

left_caption.text = "ROBOTIC ARM A"
right_caption.text = "ROBOTIC ARM B"
left_caption.pos -= (0, 0.05)
right_caption.pos -= (0, 0.05)

# Reset images
images = [left_image, right_image, left_caption, right_caption]

arm_question1 = ImageStim(win, "instructions/trial_instructions/arm1_" +
                          str(condition[0]) + ".png", pos=(0, 0.7), 
                          units='norm', size=(None, 0.22))

main1 = True
if main1:
    for i in range(5, 10):
        instruction.setImage(instructions[i])
        instruction.draw()
        win.flip()
        if i == 6:
            core.wait(instruction_time_long)
        else:
            core.wait(instruction_time)
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space", "escape"])
        if press[-1].name == 'escape':
            win.close()
            core.quit()()

    for file in range(len(arm_pairs)):
        if arm_pairs[file][0] == arm_pairs[file][1]:
            keylist = ["q", "escape"]
            attention_check.draw()
        else:
            keylist = ["d", "k", "escape"]
            arm_question1.draw()
        left_image.setImage(arm_pairs[file][0])
        right_image.setImage(arm_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        win.flip()
        kb.clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            choice = "timeout"
            rt = max_wait
            timeout_message.draw()
            win.flip()
            core.wait(1)
        elif press[-1].name == 'escape':
            win.close()
            core.quit()
        elif press[-1].name == "d":
            choice = "d"
            rt = press[-1].rt
            arm_question1.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            win.flip()
            core.wait(0.3)
        elif press[-1].name == "k":
            choice = "k"
            rt = press[-1].rt
            arm_question1.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            right_border.draw()
            win.flip()
            core.wait(0.3)
        else:
            choice = "q"
            rt = press[-1].rt
            attention_check.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            right_border.draw()
            win.flip()
            core.wait(0.3)
        data = pd.DataFrame({"id": [participant_ID], "condition": [condition[0]], 
                             "block": ["arm1"], "trial": [file], "stimA": [arm_pairs[file][0]],
                             "stimB":[arm_pairs[file][1]], "choice": [choice],
                             "rt": [rt]})

        df = pd.concat([df, data])
        data.to_csv(path, mode="a", header = False, index = False)
    arm_question1.autoDraw = False


## Part 3: Arm Eeriness (Main Task 2)

arm_pairs = [np.random.choice([arm_files[x], arm_files[y]], 2, replace=False) \
                for y in range(len(arm_files)) \
                    for x in range(y + 1, len(arm_files))]
extra_arms = np.random.choice(arm_files, 1)
arm_pairs.append([extra_arms[0], extra_arms[0]])
np.random.shuffle(arm_pairs)

arm_question2 = ImageStim(win, "instructions/trial_instructions/arm2_" + 
                          str(condition[0]) + ".png", 
                          pos=(0, 0.7), units='norm', size=(None, 0.22))

main2 = True
if main2:
    for i in range(11,13):
        instruction.setImage(instructions[i])
        instruction.draw()
        win.flip()
        core.wait(instruction_time)
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space", "escape"])
        if press[-1].name == 'escape':
            win.close()
            core.quit()()

    arm_question2.autoDraw = True
    for file in range(len(arm_pairs)):
        if arm_pairs[file][0] == arm_pairs[file][1]:
            keylist = ["q", "escape"]
            attention_check.draw()
        else:
            keylist = ["d", "k", "escape"]
            arm_question2.draw()
        left_image.setImage(arm_pairs[file][0])
        right_image.setImage(arm_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        win.flip()
        kb.clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            choice = "timeout"
            rt = max_wait
            timeout_message.draw()
            win.flip()
            core.wait(1)
        elif press[-1].name == 'escape':
            win.close()
            core.quit()()
        elif press[-1].name == "d":
            choice = "d"
            arm_question2.draw()
            rt = press[-1].rt
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            win.flip()
            core.wait(0.3)
        elif press[-1].name == "k":
            choice = "k"
            rt = press[-1].rt
            arm_question2.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            right_border.draw()
            win.flip()
            core.wait(0.3)
        else:
            choice = "q"
            rt = press[-1].rt
            attention_check.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            right_border.draw()
            win.flip()
            core.wait(0.3)
        data = pd.DataFrame({"id": [participant_ID], "condition": [condition[0]], 
                             "block": ["arm2"], "trial": [file], "stimA": [arm_pairs[file][0]],
                             "stimB":[arm_pairs[file][1]], "choice": [choice],
                             "rt": [rt]})
        df = pd.concat([df, data])
        data.to_csv(path, mode="a", header = False, index = False)
    arm_question2.autoDraw = False

## Part 4: Arm comparison (Main Task 3)

# Recreate images to set new size
left_image = ImageStim(win, image=arm_files[0], pos=(-0.5, -0.1), units='norm',
                       size=(0.5, None))
left_border = ShapeStim(win, vertices=left_image.verticesPix, units="pix", 
                        lineColor=(0,0,1), fillColor=None, colorSpace='rgb',
                        lineWidth=4)
right_image = ImageStim(win, image=arm_files[1], pos=(0.5, -0.1), units='norm',
                        size=(0.5, None))
right_border = ShapeStim(win, vertices=right_image.verticesPix, units="pix", 
                         lineColor=(0,0,1), fillColor=None, colorSpace='rgb', 
                         lineWidth=4)

left_caption.text = "ROBOTIC ARM A"
right_caption.text = "ROBOTIC ARM B"
left_caption.pos -= (0, 0.1)
right_caption.pos -= (0, 0.1)

# Reset images
images = [left_image, right_image, left_caption, right_caption]

arm_pairs = [np.random.choice([arm_files[x], arm_files[y]], 2, replace=False) \
                for y in range(len(arm_files)) \
                    for x in range(y + 1, len(arm_files))]
extra_arms = np.random.choice(arm_files, 1)
arm_pairs.append([extra_arms[0], extra_arms[0]])
np.random.shuffle(arm_pairs)

arm_question3 = ImageStim(win, "instructions/trial_instructions/arm3_" + 
                          str(condition[0]) + ".png", 
                          pos=(0, 0.7), units='norm', size=(None, 0.22))

main3 = True
if main3:
    for i in range(14, 17):
        instruction.setImage(instructions[i])
        instruction.draw()
        win.flip()
        core.wait(instruction_time)
        instruction.draw()
        spacebar_instruction.draw()
        win.flip()
        press = kb.waitKeys(keyList=["space", "escape"])
        if press[-1].name == 'escape':
            win.close()
            core.quit()()

    for file in range(len(arm_pairs)):
        if arm_pairs[file][0] == arm_pairs[file][1]:
            keylist = ["q", "escape"]
            attention_check.draw()
        else:
            keylist = ["d", "k", "escape"]
            arm_question3.draw()
        left_image.setImage(arm_pairs[file][0])
        right_image.setImage(arm_pairs[file][1])
        [image.draw() for image in images]
        [guide.draw() for guide in guides]
        ref_image.draw()
        win.flip()
        kb.clock.reset()
        press = kb.waitKeys(maxWait=max_wait, keyList=keylist, waitRelease=False)
        if press == None:
            choice = "timeout"
            rt = max_wait
            timeout_message.draw()
            win.flip()
            core.wait(1)
        elif press[-1].name == "escape":
            win.close()
            core.quit()()
        elif press[-1].name == "d":
            choice = "d"
            rt = press[-1].rt
            arm_question3.draw()
            ref_image.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            win.flip()
            core.wait(0.3)
        elif press[-1].name == "k":
            choice = "k"
            rt = press[-1].rt
            arm_question3.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            right_border.draw()
            ref_image.draw()
            win.flip()
            core.wait(0.3)
        else:
            choice = "q"
            rt = press[-1].rt
            attention_check.draw()
            ref_image.draw()
            [image.draw() for image in images]
            [guide.draw() for guide in guides]
            left_border.draw()
            right_border.draw()
            win.flip()
            core.wait(0.3)
        data = pd.DataFrame({"id": [participant_ID], "condition": [condition[0]], 
                             "block": ["arm3"], "trial": [file], "stimA": [arm_pairs[file][0]],
                             "stimB":[arm_pairs[file][1]], "choice": [choice],
                             "rt": [rt]})

        df = pd.concat([df, data])
        data.to_csv(path, mode="a", header = False, index = False)
    arm_question3.autoDraw = False

## Part 5: Demographics (END)

closing_message = TextBox2(win, "Thank you for participating in the experiment." \
"\nYou will now be redirected to a survey.", font=font, letterHeight=0.05, 
                  color = 'black', alignment='center')
closing_message.draw()
win.flip()
core.wait(instruction_time)
closing_message.draw()
spacebar_instruction.draw()
win.flip()
press = kb.waitKeys(keyList = ["space", "escape"])
if press[-1].name == "escape":
    win.close()
    core.quit()

win.close()
open_new("https://uva.fra1.qualtrics.com/jfe/form/SV_26lJCoqTzq0hZSm")
df.to_csv("data/experiment_data.csv", mode = "a", header = False, index = False)
core.quit()
