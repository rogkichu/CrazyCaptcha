import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageTk
import random
import string
import pyttsx3
from threading import Thread
import winsound

engine = pyttsx3.init()

def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_captcha_image(text):
    width, height = 220, 80
    image = Image.new('RGB', (width, height), (255, 255, 255))
    try:
        font = ImageFont.truetype("arial.ttf", 42)
    except IOError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    for i, char in enumerate(text):
        position = (15 + i * 35, random.randint(10, 20))
        draw.text(position, char, font=font, fill=(random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)))
    for _ in range(5):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=(0, 0, 0), width=2)
    return image.filter(ImageFilter.BLUR)

captcha_text = generate_captcha_text()
root = tk.Tk()
root.title("Motivational CAPTCHA Challenge")
root.geometry("400x550")
root.configure(bg="#ffe5e5")

button_style = {
    "font": ("Helvetica", 13, "bold"),
    "bg": "#ff6f61",
    "fg": "#ffffff",
    "activebackground": "#ff4c3b",
    "width": 15,
    "bd": 0,
    "relief": "flat",
    "highlightthickness": 0
}
label_font = ("Helvetica", 15, "bold")

container_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
container_frame.place(relx=0.5, rely=0.5, anchor="center")
container_frame.config(borderwidth=2, highlightbackground="#ff6f61")

incorrect_attempts = 0
time_left = 30

def update_captcha():
    global captcha_text, captcha_image_tk, time_left
    captcha_text = generate_captcha_text()
    captcha_image = create_captcha_image(captcha_text)
    captcha_image_tk = ImageTk.PhotoImage(captcha_image)
    captcha_label.config(image=captcha_image_tk)
    hint_label.config(text="")
    reset_timer()
    show_random_quote()

def voice_confirmation(message):
    engine.say(message)
    engine.runAndWait()

def play_warning_sound():
    winsound.Beep(1000, 200)

captcha_image_tk = ImageTk.PhotoImage(create_captcha_image(captcha_text))
captcha_label = tk.Label(container_frame, image=captcha_image_tk, bg="#ffffff")
captcha_label.pack(pady=10)

entry_label = tk.Label(container_frame, text="Enter CAPTCHA Text", font=label_font, bg="#ffffff", fg="#333333")
entry_label.pack()
captcha_entry = tk.Entry(container_frame, font=("Helvetica", 16), width=15, bg="#f5f5f5", borderwidth=2, relief="ridge")
captcha_entry.pack(pady=10)

morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}
morse_hint = ' '.join(morse_code[char] for char in captcha_text)
hint_label = tk.Label(container_frame, text="", font=("Helvetica", 12), bg="#ffffff", fg="#ff6347")
hint_label.pack(pady=5)

def show_random_quote():
    quotes = [
        "Keep pushing forward!",
        "Success is just around the corner!",
        "Believe in yourself!",
        "Every setback is a setup for a comeback!",
        "Don't give up!",
        "You're doing great, keep trying!"
    ]
    random_quote = random.choice(quotes)
    quote_label.config(text=random_quote)

def show_morse_hint():
    hint_label.config(text=f"Hint: {morse_hint}")

def countdown():
    global time_left
    if time_left > 0:
        timer_label.config(text=f"Time left: {time_left}s")
        time_left -= 1
        root.after(1000, countdown)
    else:
        timer_label.config(text="Too slow!")
        Thread(target=voice_confirmation, args=("Too slow!",)).start()
        update_captcha()

def reset_timer():
    global time_left
    time_left = 30
    countdown()

failure_phrases = [
    "Are you blind?",
    "Try again, it's not that hard!",
    "Oops! Not quite right.",
    "Come on, you can do better!",
]

def check_captcha():
    global incorrect_attempts
    result_label.config(text="Incorrect! Try again.", fg="red")
    incorrect_attempts += 1
    if incorrect_attempts >= 3:
        show_random_quote()
    random_failure_message = random.choice(failure_phrases)
    Thread(target=voice_confirmation, args=(random_failure_message,)).start()
    update_captcha()
    move_submit_button()

more_help_button = tk.Button(container_frame, text="More Help", command=show_morse_hint, **button_style)
more_help_button.pack(pady=10)

def move_submit_button():
    x, y = random.randint(50, 250), random.randint(300, 400)
    submit_button.place(x=x, y=y)

timer_label = tk.Label(container_frame, text="", font=("Helvetica", 12), bg="#ffffff", fg="#ff4500")
timer_label.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=check_captcha, **button_style)
submit_button.place(x=100, y=400)

result_label = tk.Label(container_frame, text="", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
result_label.pack(pady=15)

quote_label = tk.Label(container_frame, text="", font=("Helvetica", 14), bg="#ffffff", fg="#ff6347")
quote_label.pack(pady=10)

reset_timer()
root.mainloop()
