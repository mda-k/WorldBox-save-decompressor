#imports. (pip installed ones: ctk and colorama.)
from colorama import Fore, Style, init
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import zlib
import gzip
from pathlib import Path
import shutil
import os
import sys
import time


#ctk.
ctk.set_appearance_mode("System")
root = ctk.CTk()
root.title("worldbox save recompressor")
root.geometry("500x340")
messagebox.showerror("ATTENTION!", """THIS PYTHON SCRIPT REQUIRES YOU TO GET THE ORIGINAL .wbox SAVE!
IT WILL INFACT OVERWRITE YOUR ORIGINAL .wbox SAVE! IF YOU DO NOT GIVE IT THE ORIGINAL .wbox SAVE, IT WILL NOT WORK!
PLEASE MAKE BACKUPS BEFORE USING THIS PYTHON PROGRAM!
PLEASE NAME YOUR original .wbox SAVE 'map.wbox', AND YOUR .json EDITED FILE 'map.json' AND PUT IT IN THE SAME FOLDER!""")



#boring warnings
init()
print(Fore.RED + "INFO...this program uses your system theme (light, or dark)." + Style.RESET_ALL)
print(Fore.RED + ".......you need to make the folder you are making the program rewrite the .wbox file to, or else, it won't work." + Style.RESET_ALL)
print(Fore.RED + ".......please enter the proper path to the file, including the file itself in the path!" + Style.RESET_ALL)
print(Fore.RED + ".......for any misuse of the program, i'm not taking ANY responsibilities!!!" + Style.RESET_ALL)
print(Fore.RED + ".......THE PROGRAM NEEDS YOUR ORIGINAL .wbox SAVE AS 'map.wbox'!!! IT NEEDS IT TO DETERMINE THE COMPRESSION!" + Style.RESET_ALL)
print("")
print("")
print("")
print(Fore.YELLOW + "OTHER..this program is compiled into a .exe with pyinstaller. and yes, the console is intentional." + Style.RESET_ALL)
print(Fore.YELLOW + ".......this program is nowhere perfect. it MIGHT (couldn't recreate any cases of damage tho, but better be careful) cause damage if you do not use the program correctly. and even small typos, or anything can break this program." + Style.RESET_ALL)




print("")
print("")


def recomp():
#ui part.
    recompress.configure(fg_color="gray")
    root.after(200, lambda: recompress.configure(fg_color="black"))
#decompressor part.
    folder = Path(pathentry.get())
    orig_wbox = folder / "map.wbox"
    edited_json = folder / "map.json"
    if edited_json.exists():
        print(f"selected json path: {edited_json}")
    if not edited_json.exists():
        messagebox.showerror("ERROR!", "the edited .json file does not exist. please put it in the folder you have typed in the path to. if you already did, please name it 'map.json'! if you did all this, and it's still not working, then resort to reading README.txt.")
    if orig_wbox.exists():
        print(f"selected original wbox path: {orig_wbox}")
    if not orig_wbox.exists():
        messagebox.showerror("ERROR!", "the original .wbox file does not exist. please put it in the folder you have typed in the path to. if you already did, please name it 'map.wbox'! if you did all this, and it's still not working, then resort to reading README.txt.")
        orig_format = "zlib"
        print("")
        print("")
        print("selected format: zlib")
    else:
        with orig_wbox.open("rb") as f:
            head = f.read(2)
            print("")
            print("")
            print(head)
            f.seek(0)
            time.sleep(2)
            raw = f.read()
            print(raw)
        if head.startswith(b"\x1f\x8b"):
            orig_format = "gzip"
            print("selected format: gzip")
        else:
            try:
                zlib.decompress(raw)
                orig_format = "zlib"
                print("selected format: zlib")
            except zlib.error:
                try:
                    zlib.decompress(raw, -zlib.MAX_WBITS)
                    orig_format = "raw"
                    print("selected format: raw")
                except zlib.error:
                    print("could not determine original compression exactly. defaulting to zlib-wrapped.")
                    orig_format = "zlib"
    text = edited_json.read_text(encoding="utf-8")
    print("")
    print("")
    print(text)
    time.sleep(3)
    data = text.encode("utf-8")
    print(data)
    out_bytes = None
    if orig_format == "gzip":
        out_bytes = gzip.compress(data)
    elif orig_format == "zlib":
        out_bytes = zlib.compress(data)
    elif orig_format == "raw":
        comp = zlib.compressobj(level=9, wbits=-zlib.MAX_WBITS)
        out_bytes = comp.compress(data) + comp.flush()
    else:
        out_bytes = zlib.compress(data)
    with orig_wbox.open("wb") as f:
        f.write(out_bytes)
    txtvar.set("done!")



#ctk ui.
pathentry = ctk.CTkEntry(root, width=460)
pathentry.place(relx=0.5, y=50, anchor="center")
info = ctk.CTkLabel(root, text="type in path to the folder which has the original .wbox save and the edited .json save.")
info.place(relx=0.5, y=10, anchor="center")
info0 = ctk.CTkLabel(root, text="""NOTE: THIS PROGRAM WILL OVERWRITE YOUR ORIGINAL .wbox SAVE!
IT REQUIRES YOUR ORIGINAL .wbox SAVE!
YOU NEED TO ONLY ADD THE PATH OF THE FOLDER,
PLEASE DO NOT PUT THE FILE NAME IN THE PATH.
PLEASE HAVE BOTH OF THE FILES
(the original .wbox save and the .json edited save)
IN THE SAME FOLDER!""")
info0.place(relx=0.5, y=120, anchor="center")
recompress = ctk.CTkButton(root, text="recompress", fg_color="black", hover_color="#333333", text_color="white", command=recomp, corner_radius=5)
recompress.place(relx=0.5, y=300, anchor="center")
txtvar = tk.StringVar()
info1 = ctk.CTkLabel(root, text="status")
info1.place(relx=0.5, y=205, anchor="center")
done = ctk.CTkEntry(root, width=440, state="readonly", textvariable=txtvar)
done.place(relx=0.5, y=250, anchor="center")



#for pyinstaller
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS #temp of pyinstaller i think
else:
    base_path = os.path.dirname(__file__)
    
#for ctk
icon_path = os.path.join(base_path, "recompressor.ico")
root.iconbitmap(icon_path)

#to avoid, or reduce the time of freezing when closing.
def on_closing():
    try:
        root.after_cancel(root.after_id)
    except AttributeError:
        pass
    root.destroy()



root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
