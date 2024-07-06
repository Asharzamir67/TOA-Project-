import tkinter as tk
from tkinter import messagebox, simpledialog

class TuringMachine:
    def __init__(self, tape):

        self.tape = list(tape)
        self.head = 1
        self.state = 'q0'
        self.temp=['']*len(tape)
        self.matched=0
        self.notmatch=0
        self.check=0
        self.done=1
        self.unique_chars=[0]*26
  

    def check_state(self):
        if self.tape[self.head] == '_':
            self.state = 'q_accept'
        else:
            self.state = 'q1'
        return self.state != 'q_accept'
    
    def reverse_one_step(self):
        if self.done==1:
            if self.check_state():
                print(self.tape[self.head]," popped from back; pushed to front",flush=True)
                self.tape.insert(1, self.tape.pop(self.head))
            #    print(self.tape[self.head]," popped from back; pushed to front",flush=True)
                self.head += 1  
            #    print(self.tape[self.head]," popped from back; pushed to front",flush=True)
            if not self.check_state():
                self.done=0
                self.check = 1
                self.head-=1
        else:
            if self.tape[self.head] == '_' and self.check==1:
                self.head += 1
            self.head -= 1         

    def count_occurrence(self, target):
        if self.done==1:
            char = self.tape[self.head]
            if char.lower() == target.lower():
                print(self.tape[self.head],"popped 1 pushed")
                char = '1'
            else:
                char = '0'
                print(self.tape[self.head],"popped 0 pushed")
            self.tape[self.head] = char
            self.head += 1
            if self.tape[self.head] == '_' and self.check==0:
                self.done=0
                self.check = 1
                self.head-=1
        else:
            if self.tape[self.head] == '_' and self.check==1:
                self.head += 1
            self.head -= 1

    def change_case(self):
        if self.done==1:
            char = self.tape[self.head]
            if char.islower():
                char = char.upper()
                print(self.tape[self.head],"popped ",char.upper()," pushed")
            elif char.isupper():
                char = char.lower()
                print(self.tape[self.head],"popped ",char.lower()," pushed")
            self.tape[self.head] = char
            self.head += 1
            if self.tape[self.head] == '_' and self.check==0:
                self.done=0
                self.check = 1
                self.head-=1
        else:
            if self.tape[self.head] == '_' and self.check==1:
                self.head += 1
            self.head -= 1

    def substring_match(self,sub):
        if self.matched<len(sub):
            if self.notmatch==0:
                if self.tape[self.head]==sub[self.matched]:
                    print(self.tape[self.head],"popped 1 pushed")
                    self.temp[self.matched]=self.tape[self.head]
                    self.tape[self.head]='1'
                    self.head+=1
                    self.matched+=1
                else:
                    if self.matched!=0:
                        self.notmatch=1
                        self.matched-=1
                        if self.head>1:
                            self.head-=1
                    else:
                        print(self.tape[self.head],"popped ",self.tape[self.head]," pushed")
                        self.head+=1
            else:
                if self.matched>-1:
                    if self.head>=1:
                        self.tape[self.head]=self.temp[self.matched]
                        print("1 popped ",self.tape[self.head]," pushed")
                    if self.matched==0:
                        self.notmatch=0
                        self.head+=1
                    else:
                        self.matched-=1
                        self.head-=1  
        elif self.tape[self.head] != '_':
            self.head-=1 

    def remove_duplicates_gui(self):
        if self.done==1:
            if self.tape[self.head] != '_'  and self.tape[self.head] != ' ':
                if self.unique_chars[ord(self.tape[self.head].lower())-97]!=1:
                    print(self.tape[self.head],"popped ",self.tape[self.head]," pushed")
                    self.unique_chars[ord(self.tape[self.head].lower())-97]=1
                else:
                    print(self.tape[self.head],"popped 0 pushed")
                    self.tape[self.head] = '0'
            self.head+=1
            if self.tape[self.head] == '_' and self.check==0:
                self.done=0
                self.check = 1
                self.head-=1
        else:
            if self.tape[self.head] == '_' and self.check==1:
                self.head += 1
            self.head -= 1


class TMGUI:
    def __init__(self, master):
        self.master = master
        master.title("Turing Machine Tape Drive")

        self.input_label = tk.Label(master, text="Enter a string:")
        self.input_label.pack()

        self.input_entry = tk.Entry(master, width=40)
        self.input_entry.pack()

        self.tape_label = tk.Label(master, text="Tape:")
        self.tape_label.pack()

        self.tape_frame = tk.Frame(master)
        self.tape_frame.pack()

        self.head_label = tk.Label(master, text="Tape Head Position:")
        self.head_label.pack()

        self.head_text = tk.Text(master, height=1, width=10)
        self.head_text.pack()

        self.reverse_button = tk.Button(master, text="Start Reversal", command=lambda: self.start_operation("reverse"))
        self.reverse_button.pack()

        self.count_button = tk.Button(master, text="Count Occurrence", command=lambda: self.start_operation("count"))
        self.count_button.pack()

        self.case_button = tk.Button(master, text="Change Case", command=lambda: self.start_operation("case"))
        self.case_button.pack()
        
        self.substring_button = tk.Button(master, text="Substring search", command=lambda: self.start_operation("substring"))
        self.substring_button.pack()

        self.remove_duplicates_button = tk.Button(master, text="Remove Duplicates", command=lambda: self.start_operation("remove_duplicates"))
        self.remove_duplicates_button.pack()

        self.turing_machine = None

    def create_tape_compartments(self, tape):
        for widget in self.tape_frame.winfo_children():
            widget.destroy()

        for char in tape:
            label = tk.Label(self.tape_frame, text=char, borderwidth=1, relief="solid", width=2)
            label.pack(side="left")

    def update_tape(self, updated_tape_contents, head_position):
        self.create_tape_compartments(updated_tape_contents)

        self.head_text.delete(1.0, tk.END)
        self.head_text.insert(tk.END, str(head_position))

    def start_operation(self, operation):
        input_string = self.input_entry.get()
        if not input_string:
            messagebox.showwarning("Warning", "Please enter a string.")
            return
        
        for i in range (len(input_string)):
            if ord(input_string[i].lower())<97 and ord(input_string[i].lower())>123:
     #           print("Invalid string. must contain only alphabets")
                messagebox.showwarning("Warning", "Invalid string. must contain only alphabets")
                return
        if operation == "count" and not hasattr(self, "target_char"):
            self.target_char = simpledialog.askstring("Input Character", "Enter a single character:")
            if self.target_char is None or len(self.target_char) != 1:
                messagebox.showwarning("Warning", "Please enter a single character.")
                return

        if operation == "substring" and not hasattr(self, "target_str"):
            self.target_str = simpledialog.askstring("Input string", "Enter a string:")
        
    #    if operation == "remove_duplicates":
    #        self.turing_machine = TuringMachine("_" + input_string + "_")
    #        updated_tape = self.turing_machine.remove_duplicates_gui()
     #       self.update_tape(updated_tape, self.turing_machine.head)
      #      return

        input_string = "_"+ input_string + "_"
        self.turing_machine = TuringMachine(input_string)

        updated_tape = self.turing_machine.tape
        head_position = self.turing_machine.head

        while self.turing_machine.check_state():
            if operation == "reverse":
                self.turing_machine.reverse_one_step()
            elif operation == "count":
                self.turing_machine.count_occurrence(self.target_char)
            elif operation == "case":
                self.turing_machine.change_case()
            elif operation == "substring":
                self.turing_machine.substring_match(self.target_str)
            elif operation == "remove_duplicates":
                self.turing_machine.remove_duplicates_gui()
            updated_tape = self.turing_machine.tape
            head_position = self.turing_machine.head
            self.update_tape(updated_tape, head_position)
            self.master.update_idletasks()  
            self.master.after(1000)

if __name__ == "__main__":
    root = tk.Tk()
    app = TMGUI(root)
    root.mainloop()