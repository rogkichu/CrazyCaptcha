import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import string

def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_captcha_image(text):
    width, height = 150, 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    for i, char in enumerate(text):
        position = (10 + i * 25, random.randint(5, 15))
        draw.text(position, char, font=font, fill=(0, 0, 0))
    return image

# Initialize tkinter window
root = tk.Tk()
root.title("Basic CAPTCHA")
root.geometry("300x300")

# Generate and display CAPTCHA
captcha_text = generate_captcha_text()
captcha_image = create_captcha_image(captcha_text)
captcha_image_tk = ImageTk.PhotoImage(captcha_image)
captcha_label = tk.Label(root, image=captcha_image_tk)
captcha_label.pack(pady=10)

# Input and submit button
entry_label = tk.Label(root, text="Enter the CAPTCHA text:", font=("Arial", 10))
entry_label.pack()
captcha_entry = tk.Entry(root, font=("Arial", 12))
captcha_entry.pack()

def check_captcha():
    user_input = captcha_entry.get()
    if user_input == captcha_text:
        result_label.config(text="CAPTCHA correct!", fg="green")
    else:
        result_label.config(text="Incorrect CAPTCHA! Try again.", fg="red")

submit_button = tk.Button(root, text="Submit", command=check_captcha, font=("Arial", 12))
submit_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
