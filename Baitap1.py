import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máy tính và Giải phương trình")
        
        # Tạo tabs
        self.tab_control = ttk.Notebook(root)
        
        # Tab 1: Giải phương trình
        self.equation_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.equation_tab, text='Giải phương trình')
        
        # Tab 2: Máy tính
        self.calculator_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.calculator_tab, text='Máy tính')
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Thiết lập giao diện cho từng tab
        self.setup_equation_tab()
        self.setup_calculator_tab()
        
        # Style cho các widgets
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)
        style.configure('TEntry', padding=5)
        
    def setup_equation_tab(self):
        # Frame cho phương trình bậc 1
        linear_frame = ttk.LabelFrame(self.equation_tab, text="Phương trình bậc 1 (ax + b = 0)", padding=10)
        linear_frame.pack(padx=10, pady=5, fill="x")
        
        # Các widgets cho phương trình bậc 1
        ttk.Label(linear_frame, text="a = ").grid(row=0, column=0)
        self.a1_entry = ttk.Entry(linear_frame, width=10)
        self.a1_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(linear_frame, text="b = ").grid(row=0, column=2)
        self.b1_entry = ttk.Entry(linear_frame, width=10)
        self.b1_entry.grid(row=0, column=3, padx=5)
        
        ttk.Button(linear_frame, text="Giải", command=self.solve_linear).grid(row=0, column=4, padx=5)
        
        # Frame cho phương trình bậc 2
        quadratic_frame = ttk.LabelFrame(self.equation_tab, text="Phương trình bậc 2 (ax² + bx + c = 0)", padding=10)
        quadratic_frame.pack(padx=10, pady=5, fill="x")
        
        # Các widgets cho phương trình bậc 2
        ttk.Label(quadratic_frame, text="a = ").grid(row=0, column=0)
        self.a2_entry = ttk.Entry(quadratic_frame, width=10)
        self.a2_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(quadratic_frame, text="b = ").grid(row=0, column=2)
        self.b2_entry = ttk.Entry(quadratic_frame, width=10)
        self.b2_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(quadratic_frame, text="c = ").grid(row=0, column=4)
        self.c2_entry = ttk.Entry(quadratic_frame, width=10)
        self.c2_entry.grid(row=0, column=5, padx=5)
        
        ttk.Button(quadratic_frame, text="Giải", command=self.solve_quadratic).grid(row=0, column=6, padx=5)
        
        # Label kết quả
        self.equation_result = ttk.Label(self.equation_tab, text="Kết quả sẽ hiển thị ở đây", wraplength=400)
        self.equation_result.pack(pady=20)
        
    def setup_calculator_tab(self):
        calc_frame = ttk.LabelFrame(self.calculator_tab, text="Máy tính cơ bản", padding=10)
        calc_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Widgets cho máy tính
        ttk.Label(calc_frame, text="Số thứ nhất:").grid(row=0, column=0, padx=5, pady=5)
        self.num1_entry = ttk.Entry(calc_frame, width=15)
        self.num1_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(calc_frame, text="Số thứ hai:").grid(row=1, column=0, padx=5, pady=5)
        self.num2_entry = ttk.Entry(calc_frame, width=15)
        self.num2_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame cho các nút phép tính
        button_frame = ttk.Frame(calc_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        operations = [('+', self.add), ('-', self.subtract), 
                     ('×', self.multiply), ('÷', self.divide)]
        
        for i, (symbol, command) in enumerate(operations):
            ttk.Button(button_frame, text=symbol, command=command).grid(row=0, column=i, padx=5)
        
        # Label kết quả
        self.calc_result = ttk.Label(calc_frame, text="Kết quả sẽ hiển thị ở đây")
        self.calc_result.grid(row=3, column=0, columnspan=2, pady=10)
    
    # Các hàm xử lý phương trình
    def solve_linear(self):
        try:
            a = float(self.a1_entry.get())
            b = float(self.b1_entry.get())
            
            if a == 0:
                if b == 0:
                    result = "Phương trình có vô số nghiệm"
                else:
                    result = "Phương trình vô nghiệm"
            else:
                x = -b / a
                result = f"Nghiệm x = {x:.2f}"
            
            self.equation_result.config(text=result)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
    
    def solve_quadratic(self):
        try:
            a = float(self.a2_entry.get())
            b = float(self.b2_entry.get())
            c = float(self.c2_entry.get())
            
            if a == 0:
                if b == 0:
                    if c == 0:
                        result = "Phương trình có vô số nghiệm"
                    else:
                        result = "Phương trình vô nghiệm"
                else:
                    x = -c / b
                    result = f"Phương trình trở thành bậc 1 với nghiệm x = {x:.2f}"
            else:
                delta = b**2 - 4*a*c
                if delta < 0:
                    result = "Phương trình vô nghiệm"
                elif delta == 0:
                    x = -b / (2*a)
                    result = f"Phương trình có nghiệm kép x = {x:.2f}"
                else:
                    x1 = (-b + math.sqrt(delta)) / (2*a)
                    x2 = (-b - math.sqrt(delta)) / (2*a)
                    result = f"Phương trình có hai nghiệm:\nx₁ = {x1:.2f}\nx₂ = {x2:.2f}"
            
            self.equation_result.config(text=result)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
    
    # Các hàm tính toán cơ bản
    def get_numbers(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            return num1, num2
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
            return None, None
    
    def add(self):
        num1, num2 = self.get_numbers()
        if num1 is not None:
            result = num1 + num2
            self.calc_result.config(text=f"Kết quả: {result:.2f}")
    
    def subtract(self):
        num1, num2 = self.get_numbers()
        if num1 is not None:
            result = num1 - num2
            self.calc_result.config(text=f"Kết quả: {result:.2f}")
    
    def multiply(self):
        num1, num2 = self.get_numbers()
        if num1 is not None:
            result = num1 * num2
            self.calc_result.config(text=f"Kết quả: {result:.2f}")
    
    def divide(self):
        num1, num2 = self.get_numbers()
        if num1 is not None:
            if num2 == 0:
                messagebox.showerror("Lỗi", "Không thể chia cho 0")
                return
            result = num1 / num2
            self.calc_result.config(text=f"Kết quả: {result:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()