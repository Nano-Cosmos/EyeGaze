from threading import Thread
import time
from tkinter import *
import cv2
import mediapipe as mp
import numpy as np
import pyautogui as py
from wordSuggestor import WordSuggestor


def program1():


    cam = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = py.size()
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = mp_face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[:]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 1, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y
                    py.moveTo(screen_x, screen_y)
            left = [landmarks[145], landmarks[159]]
            right = [landmarks[374],landmarks[386]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 0, 255))
            for landmark in right:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0,0,255))
            if (left[0].y - left[1].y) < 0.014 or (right[0].y - right[1].y) < 0.014:
                print(str(left[0].y - left[1].y)+" "+ str(right[0].y - right[1].y))
                py.click()
                py.sleep(1)

        cv2.imshow("Video Stream", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cam.release()
    cv2.destroyAllWindows()
    while True:
        print("Program 1 is running...")
        time.sleep(1)

def program2():
    # Add code for program 2 here...

    # Create an instance of WordSuggestor
    suggestor = WordSuggestor()

    # Set the path to the text file for training the suggestor
    file_path = "sample.txt"  # Update with the path to your TXT file

    # Train the suggestor using the provided text file
    suggestor.train(file_path)

    # Function to handle key presses
    def press_key(key):
        if key == 'Clear':
            display.delete(1.0, END)
        elif key == 'Backspace':
            display.delete("end - 2c")
        elif key == 'Left':
            current_index = display.index(INSERT)
            if current_index != "1.0":
                display.mark_set(INSERT, "insert-1c")
        elif key == 'Right':
            current_index = display.index(INSERT)
            if current_index != END:
                display.mark_set(INSERT, "insert+1c")
        elif key == 'Up':
            current_line, _ = map(int, display.index(INSERT).split('.'))
            if current_line > 1:
                display.mark_set(INSERT, f"{current_line - 1}.0")
        elif key == 'Down':
            current_line, _ = map(int, display.index(INSERT).split('.'))
            total_lines = int(display.index(END).split('.')[0])
            if current_line < total_lines:
                display.mark_set(INSERT, f"{current_line + 1}.0")
        elif key == 'Enter':
            display.insert(END, "\n")
        elif key == 'Caps':
            pass
        else:
            display.insert(END, key)

        update_suggestions()

    def add_space():
        display.insert(END, ' ')
        update_suggestions()

    # Function to update suggestions based on the entered prefix
    def update_suggestions():
        # Clear all suggestion buttons
        for button in suggestion_buttons:
            button.config(text="")

        # Get the current prefix
        text = display.get(1.0, END).strip()
        prefix = text.split()[-1]

        # Get suggestions for the prefix
        suggestions = suggestor.suggest_words(prefix)

        # Update suggestion buttons with the suggestions
        for i, suggestion in enumerate(suggestions):
            if i < len(suggestion_buttons):
                suggestion_buttons[i].config(text=suggestion)

    # Function to select a suggestion from the suggestion buttons
    def select_suggestion(idx):
        prefix = suggestion_buttons[idx].cget("text")
        current_text = display.get(1.0, END).strip()
        prefix_index = current_text.rfind(' ') + 1
        new_text = current_text[:prefix_index] + prefix
        display.delete(1.0, END)
        display.insert(END, new_text)

    # Function to add space when the space button is clicked
    def add_space():
        display.insert(END, ' ')  # Add space to the entry
        update_suggestions()  # Update suggestions when space is clicked

    window = Tk()  # Create the main window
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.title("On_screen_keyboard")  # Set the title of the window
    window.config(bg="#151515")  # Set the background color of the window

    main_frame = Frame(window,
                       width=600,
                       height=500, bd=2,
                       relief=SOLID,
                       highlightthickness=3,
                       highlightbackground="#37B5F7",
                       bg="#37B5F7"
                       )
    main_frame.pack(pady=90, anchor='n')  # Pack the main frame into the window

    pixel = PhotoImage(width=1, height=1)  # Create a 1x1 pixel image

    display_frame = Frame(main_frame)  # Create a frame for the display
    display_frame.pack()  # Pack the display frame into the main frame
    display = Text(display_frame,
                   bg="#37B5F7",
                   height=3,
                   width=26,
                   fg="black",
                   font=('Arial', 30),
                   wrap="word",
                   bd=2,
                   relief=FLAT
                   )
    display.pack()  # Pack the display widget into the display frame

    suggestion_frame = Frame(main_frame)
    suggestion_frame.pack()

    suggestion_buttons = []
    for i in range(5):
        btn = Button(suggestion_frame,
                     text="",
                     height=50,
                     width=160,
                     image=pixel,
                     compound=CENTER,
                     bg="#171717",
                     fg="#37B5F7",
                     font=("Arial", 12, "bold"),
                     command=lambda idx=i: select_suggestion(idx))
        btn.pack(side=LEFT)
        suggestion_buttons.append(btn)

    key_frame_1 = Frame(main_frame,
                        bg="#37B5F7"
                        )
    key_frame_1.pack()
    key_frame_2 = Frame(main_frame,
                        bg="#37B5F7")
    key_frame_2.pack()
    key_frame_3 = Frame(main_frame,
                        bg="#37B5F7"
                        )
    key_frame_3.pack()

    keys = [
        'Left', 'Right', 'Enter', 'Clear', 'Backspace',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', '!',
        'Caps', 'Up', 'Down', 'Space', '123'
    ]
    row = 0
    col = 0

    btn_left = Button(key_frame_1,
                      text=keys[0],
                      height=50,
                      width=105,
                      command=lambda: press_key(keys[0]),
                      bg="#171717",
                      fg="#37B5F7",
                      font=("Arial", 10, "bold"),
                      image=pixel, compound=CENTER,
                      relief=SUNKEN,
                      bd=3
                      )
    btn_left.grid(row=0, column=0, padx=2, pady=2)
    btn_right = Button(key_frame_1,
                       text=keys[1],
                       height=50,
                       width=105,
                       command=lambda: press_key(keys[1]),
                       bg="#171717",
                       fg="#37B5F7",
                       font=("Arial", 10, "bold"),
                       image=pixel, compound=CENTER,
                       relief=SUNKEN,
                       bd=3
                       )
    btn_right.grid(row=0, column=1, padx=2, pady=2)
    btn_enter = Button(key_frame_1,
                       text=keys[2],
                       height=50,
                       width=160,
                       command=lambda: press_key(keys[2]),
                       bg="#171717",
                       fg="#37B5F7",
                       font=("Arial", 10, "bold"),
                       image=pixel, compound=CENTER,
                       relief=SUNKEN,
                       bd=3
                       )
    btn_enter.grid(row=0, column=2, padx=2, pady=2)
    btn_clear = Button(key_frame_1,
                       text=keys[3],
                       height=50,
                       width=160,
                       command=lambda: press_key(keys[3]),
                       bg="#171717",
                       fg="#37B5F7",
                       font=("Arial", 10, "bold"),
                       image=pixel, compound=CENTER,
                       relief=SUNKEN,
                       bd=3
                       )
    btn_clear.grid(row=0, column=3, padx=2, pady=2)
    btn_backspace = Button(key_frame_1,
                           text=keys[4],
                           height=50,
                           width=240,
                           command=lambda: press_key(keys[4]),
                           bg="#171717",
                           fg="#37B5F7",
                           font=("Arial", 10, "bold"),
                           image=pixel, compound=CENTER,
                           relief=SUNKEN,
                           bd=3
                           )
    btn_backspace.grid(row=0, column=4, padx=2, pady=2)

    for key in keys[5:35]:
        button = Button(key_frame_2,
                        text=key,
                        width=70,
                        height=50,
                        command=lambda key=key: press_key(key),
                        bg="#171717",
                        fg="#37B5F7",
                        font=("Arial", 13, "bold"),
                        image=pixel, compound=CENTER,
                        relief=SUNKEN,
                        bd=3)
        button.grid(row=row, column=col, padx=2, pady=2)
        col += 1
        if col > 9:
            col = 0
            row += 1

    btn_caps = Button(key_frame_3,
                      text=keys[35],
                      height=50,
                      width=130,
                      command=lambda: press_key(keys[35]),
                      bg="#171717",
                      fg="#37B5F7",
                      font=("Arial", 10, "bold"),
                      image=pixel, compound=CENTER,
                      relief=SUNKEN,
                      bd=3
                      )
    btn_caps.grid(row=0, column=0, padx=2, pady=2)
    btn_up = Button(key_frame_3,
                    text=keys[36],
                    height=50,
                    width=105,
                    command=lambda: press_key(keys[36]),
                    bg="#171717",
                    fg="#37B5F7",
                    font=("Arial", 10, "bold"),
                    image=pixel, compound=CENTER,
                    relief=SUNKEN,
                    bd=3
                    )
    btn_up.grid(row=0, column=1, padx=2, pady=2)
    btn_down = Button(key_frame_3,
                      text=keys[37],
                      height=50,
                      width=105,
                      command=lambda: press_key(keys[37]),
                      bg="#171717",
                      fg="#37B5F7",
                      font=("Arial", 10, "bold"),
                      image=pixel, compound=CENTER,
                      relief=SUNKEN,
                      bd=3
                      )
    btn_down.grid(row=0, column=2, padx=2, pady=2)
    btn_space = Button(key_frame_3,
                       text="Space",
                       height=50,
                       width=300,
                       command=add_space,
                       bg="#171717",
                       fg="#37B5F7",
                       font=("Arial", 10, "bold"),
                       image=pixel, compound=CENTER,
                       relief=SUNKEN,
                       bd=3
                       )
    btn_space.grid(row=0, column=3, padx=2, pady=2)
    btn_num = Button(key_frame_3,
                     text=keys[39],
                     height=50,
                     width=130,
                     command=lambda: press_key(keys[39]),
                     bg="#171717",
                     fg="#37B5F7",
                     font=("Arial", 10, "bold"),
                     image=pixel, compound=CENTER,
                     relief=SUNKEN,
                     bd=3
                     )
    btn_num.grid(row=0, column=4, padx=2, pady=2)

    window.update()
    window.state('zoomed')
    window.mainloop()

    while True:
        print("Program 2 is running...")
        time.sleep(1)

if __name__ == "__main__":
    # Create and start threads for each program
    thread1 = Thread(target=program1)
    thread2 = Thread(target=program2)

    thread1.start()
    thread2.start()

    # Wait for threads to finish
    thread1.join()
    thread2.join()
