import customtkinter as ctk

# Criar a janela principal
ctk.set_appearance_mode("dark")  # Opcional: modo escuro
janela = ctk.CTk()
janela.geometry("400x400")
janela.title("Frame Scrollável")

# Criar um frame scrollável
scrollable_frame = ctk.CTkScrollableFrame(janela, width=300, height=300)
scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Adicionar widgets dentro do frame scrollável
for i in range(20):
    label = ctk.CTkLabel(scrollable_frame, text=f"Item {i+1}")
    label.pack(pady=5, padx=10)

# Iniciar o loop da interface gráfica
janela.mainloop()
