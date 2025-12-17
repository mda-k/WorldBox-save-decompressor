#imports. (pip installed ones: ctk and colorama.)
import time
import zlib, gzip
from pathlib import Path
import tkinter as tk
import customtkinter as ctk
from colorama import init, Fore, Style
import sys
import os


#background console stuff.
asd = "encoded decompressed file as utf8."
sad = "decompressed file."
das = "decoding decompressed file..."



#ctk.
ctk.set_appearance_mode("System")
root = ctk.CTk()
root.title("worldbox save decompresser")
root.geometry("500x340")



#boring warnings
init()
print(Fore.RED + "INFO...this program uses your system theme (light, or dark)." + Style.RESET_ALL)
print(Fore.RED + ".......you need to make the folder you are making the program output the .json file to, or else, it won't work." + Style.RESET_ALL)
print(Fore.RED + ".......please enter the proper path to the file, including the file itself in the path!" + Style.RESET_ALL)
print(Fore.RED + ".......for any misuse of the program, i'm not taking ANY responsibilities!!!" + Style.RESET_ALL)
print("")
print("")
print("")
print(Fore.YELLOW + "OTHER..this program is compiled into a .exe with pyinstaller. and yes, the console is intentional." + Style.RESET_ALL)
print(Fore.YELLOW + ".......this program is nowhere perfect. it MIGHT (couldn't recreate any cases of damage tho, but better be careful) cause damage if you do not use the program correctly. and even small typos, or anything can break this program." + Style.RESET_ALL)



#the function that actually decompiles stuff.
def decomp():
#ui part.
    uncompress.configure(fg_color="gray")
    root.after(200, lambda: uncompress.configure(fg_color="black"))
#decompressor part.
    inp = Path(pathentry.get())
    outdir = Path(outputentry.get())
    out = outdir / (inp.stem + ".json")
    data = inp.read_bytes()
    decompressed = None
    try:
        decompressed = zlib.decompress(data)
    except zlib.error:
        try:
            decompressed = gzip.decompress(data)
        except OSError:
            decompressed = zlib.decompress(data, -zlib.MAX_WBITS)
    print(f"{decompressed}")
    print("")
    print("")
    print(Fore.GREEN + (sad) + Style.RESET_ALL)
    time.sleep(3)
    text = decompressed.decode("utf-8")
    print(f"{text}")
    print("")
    print("")
    print(Fore.GREEN + (asd) + Style.RESET_ALL)
    out.write_text(text, encoding="utf-8")
    done.delete(0, tk.END)
    p = str(inp)
    out = str(out)
    print("")
    print("")
    print(f"decompressed {p}. wrote decompressed .json file to {out}")
    print("")
    print(Fore.GREEN + "ready" + Style.RESET_ALL)
    txtvar.set(f"decompressed {p}. wrote decompressed .json file to {out}")
    


#ctk ui.
pathentry = ctk.CTkEntry(root, width=460)
pathentry.place(relx=0.5, y=50, anchor="center")
outputentry = ctk.CTkEntry(root, width=460)
outputentry.place(relx=0.5, y=150, anchor="center")
info = ctk.CTkLabel(root, text="type in path to the file you want to uncompress")
info.place(relx=0.5, y=10, anchor="center")
info0 = ctk.CTkLabel(root, text="type in path to where you want the uncompressed file")
info0.place(relx=0.5, y=105, anchor="center")
uncompress = ctk.CTkButton(root, text="decompress", fg_color="black", hover_color="#333333", text_color="white", command=decomp, corner_radius=5)
uncompress.place(relx=0.5, y=300, anchor="center")
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
icon_path = os.path.join(base_path, "decompressor.ico")
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