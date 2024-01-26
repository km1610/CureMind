import re
import tkinter as tk
import tkinter.font as tkFont
from markdown2 import Markdown
from tkhtmlview import HTMLLabel
import google.generativeai as genai
from tkinter import ttk
from tkinter import *
import tkinter.messagebox
import pyttsx3
import os

LARGEFONT = ("Pristina", 30)
SMALLFONT = ("Verdana",12)

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel('gemini-pro')

def generate():
  name_e = name.get()
  age_e = age.get()
  gen_e = gen_combobox.get()
  sex_e = sex_combobox.get()
  problem_e = problem.get()

  if name_e and age_e and gen_e and sex_e and problem_e:
    suggestion_txt.config(state=tk.NORMAL)
    global response
    response = model.generate_content([f"Hi, I am {name_e}, my age is {age_e}, I am a {gen_e} and I am {sex_e}. You are a mental health doctor. The problem I am facing is that {problem_e}. Suggest me an activity or give me some random suggestion."],safety_settings=[{
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
    },{
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE",
    },{
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE",
    },{
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_NONE",
    }])
    try:
      print(response.text)
      md2html = Markdown()
      suggestion_txt.set_html(md2html.convert(response.text))

    except ValueError:
      messagebox.showerror("Error","Some error occurred. Try again later.")
      print(response.prompt_feedback)
    
    response = model.generate_content([f"Hi, I am {name_e}, my age is {age_e}, I am a {gen_e} and I am {sex_e}. You are a mental health doctor. The problem I am facing is that {problem_e}. Give me an inspiring quote"],safety_settings=[{
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
    },{
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE",
    },{
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE",
    },{
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_NONE",
    }])
    try:
      print(response.text)
      md2html = Markdown()
      quote_txt.set_html(md2html.convert(response.text))
    except ValueError:
      messagebox.showerror("Error","Some error occurred. Try again later.")
      print(response.prompt_feedback)


parent = tk.Tk()
parent.configure(bg="#FFFAE6")
parent.title("CureMind")

heading = tk.Label(parent, text ="Welcome to CureMind", font = LARGEFONT,bg="#FFFAE6")
heading.grid(row = 0, column = 0, padx = 10, pady = 2, columnspan = 6)

slogan = tk.Label(parent, text ="Taking a deep breath for mental clarity",font=SMALLFONT,bg="#FFFAE6")
slogan.grid(row = 1, column = 0, padx = 10, pady = 5, columnspan = 6)

fill_lbl = tk.Label(parent, text ="", font = SMALLFONT,bg="#FFFAE6")
fill_lbl.grid(row = 2, column = 0, padx = 10, pady = 2)

name_lbl = tk.Label(parent, text ="Name: ", font = SMALLFONT,bg="#FFFAE6")
name_lbl.grid(row = 3, column = 0, padx = 10, pady = 2)

name = tk.Entry(parent, width=50)
name.grid(row = 3, column = 1, padx = 10, pady = 2)

age_lbl = tk.Label(parent, text ="Age: ", font = SMALLFONT,bg="#FFFAE6")
age_lbl.grid(row = 4, column = 0, padx = 10, pady = 2)

age = tk.Entry(parent, width=50)
age.grid(row = 4, column = 1, padx = 10, pady = 2)

gen_lbl = tk.Label(parent, text ="Gender: ", font = SMALLFONT,bg="#FFFAE6")
gen_lbl.grid(row = 5, column = 0, padx = 10, pady = 2)

gen_options = ["Male", "Female", "Other"]
gen_combobox = ttk.Combobox(parent, values=gen_options,width=47,state="readonly")
gen_combobox.grid(row = 5, column = 1, padx = 10, pady = 2)

sex_lbl = tk.Label(parent, text ="Sexuality: ", font = SMALLFONT,bg="#FFFAE6")
sex_lbl.grid(row = 6, column = 0, padx = 10, pady = 2)

sex_options = ["Heterosexual","Homosexual","Bisexual","Pansexual","Asexual","Demisexual","Queer","Questioning"]

sex_combobox = ttk.Combobox(parent, values=sex_options,width=47,state="readonly")
sex_combobox.grid(row = 6, column = 1, padx = 10, pady = 2)

problem_lbl = tk.Label(parent, text ="Share your problem: ", font = SMALLFONT,bg="#FFFAE6")
problem_lbl.grid(row = 7, column = 0, padx = 10, pady = 2)

problem = tk.Entry(parent, width=50)
problem.grid(row = 7, column = 1, padx = 10, pady = 2)

submit_btn = tk.Button(parent,text="Done",bg="#FFFAE6",width=80,height=2,command=generate)
submit_btn.grid(row = 8, column = 0, padx = 10, pady = 2,columnspan=2)

suggestion_lbl = tk.Label(parent, text ="Today's Suggestion", font = SMALLFONT,bg="#FFFAE6")
suggestion_lbl.grid(row = 2, column = 2, padx = 10, pady = 2)

suggestion_txt = HTMLLabel(parent,height=6, background="white", html="")
suggestion_txt.grid(row=3, column=2, padx = 10, pady = 2,rowspan=4)
suggestion_txt.config(state=tk.DISABLED)

quote_lbl = tk.Label(parent, text ="Quote for you", font = SMALLFONT,bg="#FFFAE6")
quote_lbl.grid(row = 7, column = 2, padx = 10, pady = 2)

quote_txt = HTMLLabel(parent,height=2, background="white", html="")
quote_txt.grid(row=8, column=2, padx = 10, pady = 2)
quote_txt.config(state=tk.DISABLED)

scroll1 = tk.Scrollbar(parent, command=suggestion_txt.yview)
suggestion_txt.configure(yscrollcommand=scroll1.set)
scroll1.grid(row=3, column=3, pady=10,rowspan=4)

scroll2 = tk.Scrollbar(parent, command=quote_txt.yview)
quote_txt.configure(yscrollcommand=scroll2.set)
scroll2.grid(row=8, column=3, pady=10)

parent.mainloop()
