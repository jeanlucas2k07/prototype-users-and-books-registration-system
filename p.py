import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO
from google_books_api import Livros
from bancoImagens import Images

class LivroFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, width=670, height=510, fg_color="transparent")
        self.grid(row=1, column=1, padx=20, pady=20, sticky="")
        # self.exibir_bestsallers()

    def exibir_bestsallers(self):
        best = Livros().buscarBestsellers()
        return self.exibir_livros(best)
    
    def exibir_livros(self, livros: list[dict[str, str]]):
        for livro in livros:
            # Criar um frame horizontal para cada livro
            livro_frame = ctk.CTkFrame(self, width=700)
            livro_frame.pack(fill="x", pady=10, padx=10)

            # Carregar e exibir a capa a partir da URL
            capa_url = livro['capa']
            if capa_url != "Sem capa":
                try:
                    response = requests.get(capa_url)
                    img_data = response.content
                    img = Image.open(BytesIO(img_data))

                    # Redimensionar a imagem para um tamanho fixo
                    img = img.resize((100, 150))  
                    img_ctk = ctk.CTkImage(light_image=img, size=(100, 150))  # Converter para CTkImage
                    label_capa = ctk.CTkLabel(livro_frame, image=img_ctk, text="")
                    label_capa.image = img_ctk  # Manter referência da imagem

                    label_capa.pack(side="left", padx=10)  # Posicionar à esquerda
                
                except Exception as e:
                    print(f"Erro ao carregar a capa: {e}")
                    label_capa = ctk.CTkLabel(livro_frame, text="Capa não disponível")
                    label_capa.pack(side="left", padx=10)
            else:
                if Images().checarImagem(isbn=livro["ISBN"]):
                    try:
                        img = Image.open(BytesIO(Images().checarImagem(livro["ISBN"])))
                        img = img.resize((100, 150))
                        img_ctk = ctk.CTkImage(light_image=img, size=(100, 150))
                        label_capa = ctk.CTkLabel(livro_frame, image=img_ctk, text="")
                        label_capa.image = img_ctk

                        label_capa.pack(side="left", padx=10)

                    except Exception as e:
                        print(f"Erro ao carregar a capa: {e}")
                        label_capa = ctk.CTkLabel(livro_frame, text="Capa não disponível")
                        label_capa.pack(side="left", padx=10)

            # Criar um frame para as informações do livro
            info_frame = ctk.CTkFrame(livro_frame, fg_color="transparent")  # Sem fundo visível
            info_frame.pack(side="left", fill="both", expand=True, padx=10)

            # Criar labels para exibir as informações
            label_titulo = ctk.CTkLabel(info_frame, text=f"Título: {livro['titulo']}", font=("Arial", 14, "bold"))
            label_titulo.pack(anchor="w")

            label_autores = ctk.CTkLabel(info_frame, text=f"Autor(es): {livro['autores']}", font=("Arial", 12))
            label_autores.pack(anchor="w")

            # Limitar a descrição a 100 caracteres para não ocupar muito espaço
            descricao = livro['descricao']
            if len(descricao) > 100:
                descricao = descricao[:100] + "\n"
            
            label_descricao = ctk.CTkLabel(info_frame, text=f"Descrição: {descricao}", font=("Arial", 11))
            label_descricao.pack(anchor="w")