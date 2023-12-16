import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from pygame import mixer
mixer.init()
from CTkMessagebox import CTkMessagebox
from main import activate



root = ctk.CTk()
root.geometry("1050x700")
ctk.set_appearance_mode("Dark")
root.title("HarmoniSync")
root.resizable(False, False)
root.iconbitmap("logo.ico")

# Global Variables
global uploaded_image, output_file, convert_button, play_image, pause_image
global playing, image_label, pp_button, down_button, bar, slider
playing = False
# Functions
def play():
    global output_file, playing, convert_button
    playing = True
    convert_button.configure(state="disabled")
    mixer.init()
    mixer.music.load(output_file)
    mixer.music.play(loops=0)

def update_slider():
    global playing
    if playing:
        slider.set(mixer.music.get_pos() / 1000)
        if int(slider.get()) == 100:
            mixer.music.stop()
    root.after(100, update_slider)

def download_clicked():
    global output_file
    file_path = ctk.filedialog.asksaveasfilename(defaultextension=".midi", filetypes=[("MIDI files", "*.midi")])
    if file_path:
        try:
            if isinstance(output_file, str):
                output_to_save = output_file.encode('utf-8')
            with open(file_path, 'wb') as midi_file:
                midi_file.write(output_to_save)
            CTkMessagebox(title="Success", message="Successfully downloaded", icon = "check")
        except Exception as e:
            CTkMessagebox(title="Failed", message=f"Error downloading {e}", icon = "warning")


def pp_clicked():
    global play_image, pause_image, pp_button, playing
    if pp_button._image == pause_image:
        mixer.music.pause()
        playing = False
        pp_button.configure(image=play_image)
    elif pp_button._image == play_image:
        mixer.music.unpause()
        playing = True
        pp_button.configure(image=pause_image)


def upload_button_click():
    global convert_button, uploaded_image, image_label,file_path
    convert_button.configure(state="disabled")
    file_path = ctk.filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
    print(file_path)
    if file_path:
        image_label.place_forget()
        uploaded_image = Image.open(file_path)
        uploaded_image_ctk = ctk.CTkImage(uploaded_image, size=(350,400))
        image_label = ctk.CTkLabel(master=frame, image=uploaded_image_ctk, text="")
        image_label.place(x=100,y=50)
        convert_button.configure(state="normal")


def convert_button_click():
    global uploaded_image, output_file,file_path
    mixer.music.stop()
    bar.place(x=100, y=480)
    bar.start()
    activate(file_path)
    output_file = "output/output.mid"
    bar.place_forget() 
    slider.place(x=125, y=550)
    slider.set(0)
    down_button.place(x=425, y=535)
    pp_button.place(x=68, y=535)
    play()



# Image
image = Image.open("logo.png")
ctk_image = ctk.CTkImage(image, size=(100,100))
photo_label = ctk.CTkLabel(master=root, image=ctk_image, text="")
photo_label.place(x=10, y=10)
# Text
text_label = ctk.CTkLabel(master=root, text="HarmoniSync", text_color="#F5F7F8", font=("Times New Roman",40))
text_label.place(x=110, y=40)

welcome = ctk.CTkLabel(master=root, text="Welcome to HarmoniSync!\n\n\nHarmoniSync is a tool that converts sheet music to MIDI files. To get started, click the upload button below to upload an image of your sheet music. Then, click the convert button to convert your sheet music to a MIDI file. Finally, click the play button to play your MIDI file. You can also pause, resume, and download your MIDI file. Enjoy!", text_color="#F5F7F8", font=("Lucida Fax",25), justify="left" , wraplength=500)
welcome.place(x=20, y=150)
# Frame
frame = ctk.CTkFrame(root, height=700, width=550, corner_radius=0, fg_color="#232D3F")
frame.place(x=500,y=0)
# Uploaded Image Label
image_label = ctk.CTkLabel(master=frame, text="")
# Upload Button
upload_button = ctk.CTkButton(master=frame, width=150, height=50, corner_radius=0, fg_color="#005B41", text="Upload", font=("Arial", 15), command=upload_button_click, hover_color="#008170")
upload_button.place(x=100,y=600)
# Convert Button
convert_button = ctk.CTkButton(master=frame, width=150, height=50, corner_radius=0, fg_color="#005B41", text="Convert", font=("Arial", 15), command=convert_button_click, hover_color="#008170")
convert_button.configure(state="disabled")
convert_button.place(x=300,y=600)
# Progress Bar
bar = ctk.CTkProgressBar(master=frame, width=350, height=15, orientation='horizontal', mode='indeterminate', corner_radius=0)

# Slider
slider = ctk.CTkSlider(master=frame, width=300, height=18, from_=0, to=100, orientation='horizontal')
# Download Button
down_icon = Image.open("download.png")
down_image = ctk.CTkImage(down_icon, size=(40,40))
down_button = ctk.CTkButton(master=frame, image=down_image, text="", width=40, height=40, fg_color="#232D3F", hover_color="#232D3F", command=download_clicked)
# play-pause Button
play_icon = Image.open("play.png")
pause_icon = Image.open("pause.png")
play_image = ctk.CTkImage(play_icon, size=(40,40))
pause_image = ctk.CTkImage(pause_icon, size=(40,40))
pp_button = ctk.CTkButton(master=frame, image=pause_image, text="", width=40, height=40, fg_color="#232D3F", hover_color="#232D3F", command=pp_clicked)
root.after(100, update_slider)
root.mainloop()