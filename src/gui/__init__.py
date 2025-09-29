import tkinter as tk
from tkinter import messagebox

class TrainingSurvey:
    def __init__(self, root):
        self.root = root
        self.root.title = 'Spørsmål for å planlegge øktene dine!'

        self.answers = {}

        #Treningsnivå
        tk.Label(root, text = 'Hvilket treningsnivå befinner du deg på?').pack(anchor = 'w', padx = 10, pady = 5)
        self.experience_var = tk.StringVar(value = 'Nybegynner')
        experiences = ['Nybegynner', 'Viderekommen', 'Erfaren', 'Profesjonell']
        for i in experiences:
            tk.Radiobutton(root, text = i, variable = self.experience_var, value = i).pack(anchor = 'w', padx = 20)

        #Treningsmål
        tk.Label(root, text = 'Hvilket mål ønsker du å oppnå ved hjelp av treningen?').pack(anchor = 'w', padx = 10, pady = 5)
        self.goal_var = tk.StringVar(value = 'Komme i bedre form')
        goals = ['Komme i bedre form', 'Bedre livsstil', 'Øke utholdenheten', 'Bli sterkere', 'Redusere vekten']
        for i in goals:
            tk.Radiobutton(root, text = i, variable = self.goal_var, value = i).pack(anchor = 'w', padx = 20)

        #Type trening
        tk.Label(root, text = 'Hvilken type trening foretrekker du?').pack(anchor = 'w', padx = 10, pady = 5)
        self.pref_var = tk.StringVar(value = 'Styrketrening')
        preferances = ['Styrketrening', 'Løping', 'Sykling', 'Svømming', 'Variert']
        for i in preferances:
            tk.Radiobutton(root, text = i, variable = self.pref_var, value = i).pack(anchor = 'w', padx = 20)

        #Antall økter
        tk.Label(root, text = 'Hvor mange økter ønsker du i løp av uken?').pack(anchor = 'w', padx = 10, pady = 5)
        self.session_var = tk.StringVar(value = '1-2')
        sessions = ['1-2', '3-4', '5-7']
        for i in sessions:
            tk.Radiobutton(root, text = i, variable = self.session_var, value = i).pack(anchor = 'w', padx = 20)

        #Varighet på øktene
        tk.Label(root, text = 'Hvor lenge ønsker du at en økt varer?').pack(anchor = 'w', padx = 10, pady = 5)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.insert(0, '90')
        self.duration_entry.pack(anchor = 'w', padx = 20)

        tk.Button(root, text = 'Send inn svar', command = self.submit).pack(pady = 10)

    def submit(self):
        self.answers['Erfaring'] = self.experience_var.get()
        self.answers['Mål'] = self.goal_var.get()
        self.answers['Preferanse'] = self.pref_var.get()
        self.answers['Antall'] = self.session_var.get()
        self.answers['Varighet'] = self.duration_entry.get()

        messagebox.showinfo('Svar registrert' f'Takk for svarene! \n\n{self.answers}')
    
if __name__ == '__main__':
    root = tk.Tk()
    app = TrainingSurvey(root)
    root.mainloop()
