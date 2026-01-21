import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import os
from llm_service import enviar_pergunta_chat

# Colors (matching homescreen.py style)
COLOR_BG = "#1e1e1e"
COLOR_FG = "#ffffff"
COLOR_ACCENT = "#007acc"
COLOR_ENTRY_BG = "#2d2d2d"

def read_report_context():
    try:
        with open("relatorio_viagem.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Nenhum relatório encontrado. Por favor, execute a simulação primeiro."

def send_message():
    user_question = entry_box.get()
    if not user_question.strip():
        return

    # Clear input
    entry_box.delete(0, tk.END)
    
    # Display User Message
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Você: {user_question}\n", "user")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

    # Disable input while processing
    send_button.config(state=tk.DISABLED)
    
    def process_ai():
        context = read_report_context()
        response = enviar_pergunta_chat(context, user_question)
        
        # Update GUI on main thread (Tkinter isn't thread-safe, but simple insert usually works or use after)
        root.after(0, lambda: display_ai_response(response))

    threading.Thread(target=process_ai, daemon=True).start()

def display_ai_response(response):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"IA: {response}\n\n", "ai")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)
    send_button.config(state=tk.NORMAL)

# GUI Setup
root = tk.Tk()
root.title("Chat com Especialista em Logística")
root.geometry("600x700")
root.configure(bg=COLOR_BG)

# Header
header_label = tk.Label(root, text="Assistente de Logística", font=("Segoe UI", 16, "bold"), bg=COLOR_BG, fg=COLOR_ACCENT)
header_label.pack(pady=10)

# Context Warning
context_label = tk.Label(root, text="Baseado no último relatório gerado.", font=("Segoe UI", 10, "italic"), bg=COLOR_BG, fg="#aaaaaa")
context_label.pack(pady=(0, 10))

# Chat Area
chat_frame = tk.Frame(root, bg=COLOR_BG)
chat_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_FG, insertbackground='white')
chat_display.pack(fill=tk.BOTH, expand=True)
chat_display.tag_config("user", foreground="#4ec9b0", font=("Segoe UI", 11, "bold"))
chat_display.tag_config("ai", foreground="#ce9178")
chat_display.config(state=tk.DISABLED) # Read-only

# Input Area
input_frame = tk.Frame(root, bg=COLOR_BG)
input_frame.pack(padx=20, pady=20, fill=tk.X)

entry_box = tk.Entry(input_frame, font=("Segoe UI", 12), bg=COLOR_ENTRY_BG, fg=COLOR_FG, insertbackground='white')
entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry_box.bind("<Return>", lambda event: send_message())

send_button = tk.Button(input_frame, text="Enviar", command=send_message, bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=20)
send_button.pack(side=tk.RIGHT)

if __name__ == "__main__":
    root.mainloop()
