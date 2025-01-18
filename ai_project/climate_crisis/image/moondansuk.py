import tkinter as tk
from tkinter import messagebox

class Keypad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("비밀번호 키패드")
        self.geometry("300x400")
        self.password = ""
        self.stored_password = "0000"  # 기본 비밀번호 설정
        self.is_setting_password = False
        self.is_changing_password = False
        self.create_widgets()
        self.reset_timer()

    def create_widgets(self):
        self.display = tk.Entry(self, font=("Arial", 18), show="*")
        self.display.grid(row=0, column=0, columnspan=3, ipadx=10, ipady=10)

        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            '*', '0', '#'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            action = lambda x=button: self.button_click(x)
            tk.Button(self, text=button, width=10, height=3, command=action).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 2:
                col_val = 0
                row_val += 1

    def button_click(self, value):
        self.reset_timer()
        if value == '*':
            self.confirm_action()
        elif value == '#':
            if self.stored_password in self.password and self.password.endswith(self.stored_password):
                self.is_changing_password = True
                messagebox.showinfo("안내", "새로운 비밀번호를 설정해주세요!")
                self.password = ""  # 비밀번호 변경 모드로 전환 시 입력 초기화
                self.display.delete(0, tk.END)
        else:
            self.password += value
            self.display.insert(tk.END, value)

    def confirm_action(self):
        if self.is_setting_password or self.is_changing_password:
            self.stored_password = self.password
            messagebox.showinfo("성공", "암호가 설정되었습니다!")
            self.is_setting_password = False
            self.is_changing_password = False
        else:
            if self.password.endswith(self.stored_password) and len(self.password) >= len(self.stored_password):
                messagebox.showinfo("성공", "문이 열렸습니다.")
            else:
                messagebox.showerror("오류", "비밀번호가 틀립니다.")
        self.password = ""
        self.display.delete(0, tk.END)

    def reset_timer(self):
        if hasattr(self, 'timer'):
            self.after_cancel(self.timer)
        self.timer = self.after(10000, self.clear_password)  # 10초 타이머

    def clear_password(self):
        self.password = ""
        self.display.delete(0, tk.END)
        messagebox.showinfo("안내", "입력 시간이 초과되었습니다. 비밀번호가 초기화되었습니다.")

if __name__ == "__main__":
    app = Keypad()
    app.mainloop()