# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil
import tkinter as tk
from tkinter import filedialog as fd


window = tk.Tk()
window.geometry("500x300")
window.iconphoto(False, tk.PhotoImage(file='logo.png'))
window.title("SbobbinaPippo")

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_vosk(audio_listened, language="it-IT")
                # text = r.recognize_google(audio_listened, language="it-IT")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

def delete(path):
    """path could either be relative or absolute. """
    # check if file or directory exists
    if os.path.isfile(path) or os.path.islink(path):
        # remove file
        os.remove(path)
    elif os.path.isdir(path):
        # remove directory and all its content
        shutil.rmtree(path)
    else:
        raise ValueError("Path {} is not a file or dir.".format(path))


if (os.path.exists('export.txt')):
    delete(r'export.txt')
if (os.path.exists('audio-chunks')):
    delete(r'audio-chunks')
    
def avvia():
    f = open("export.txt","w+")
    file = fd.askopenfilename()
    # sound = AudioSegment.from_mp3(src)
    # sound.export(dst, format="wav")
    out = get_large_audio_transcription(file)
    f.write(out)

        
    delete(r'audio-chunks')
    text = "Lavoro Terminato!"
    text_output = tk.Label(window, text=text, fg="green", font=("Helvetica", 16))
    text_output.grid(row=2, column=1, padx=50, sticky="W")
    

button = tk.Button(text="Seleziona File", command=avvia)
button.grid(row=1, column=1)

if __name__ == "__main__":
    window.mainloop()