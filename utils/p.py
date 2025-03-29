import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO
from apis.google_books_api import Livros
from database.bancoImagens import Images
from gui.AdicionarLista import LivrosSalvos

l = {'titulo': 'É assim que acaba', 'autores': 'Colleen Hoover', 'descricao': 'Da autora das séries Slammed e Hopeless. Um romance sobre as escolhas corretas nas situações mais difíceis. As coisas não foram sempre fáceis para Lily, mas isso nunca a impediu de conquistar a vida tão sonhada. Ela percorreu um longo caminho desde a infância, em uma cidadezinha no Maine: se formou em marketing, mudou para Boston e abriu a própria loja. Então, quando se sente atraída por um lindo neurocirurgião chamado Ryle Kincaid, tudo parece perfeito demais para ser verdade. Ryle é confiante, teimoso, talvez até um pouco arrogante e se sente atraído por Lily. Porém, sua grande aversão a relacionamentos é perturbadora. Além de estar sobrecarregada com as questões sobre seu novo relacionamento, Lily não consegue tirar Atlas Corrigan da cabeça — seu primeiro amor e a ligação com o passado que ela deixou para trás. Ele era seu protetor, alguém com quem tinha grande afinidade. Quando Atlas reaparece de repente, tudo que Lily construiu com Ryle fica em risco. Com um livro ousado e extremamente pessoal, Colleen Hoover conta uma história arrasadora, mas também inovadora, que não tem medo de discutir temas como abuso e violência doméstica. Uma narrativa inesquecível sobre um amor que custa caro demais.', 'capa': 'http://books.google.com/books/content?id=AKJGDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 'ISBN': '8501113492'}

class LivroInfo(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, width = 950, fg_color = "transparent")
        self.grid(row=1, column=1, padx=20, pady=20, sticky="")
    
    def livroInfo(self, livro):
        livro_frame = ctk.CTkFrame(self, width=475)
        livro_frame.pack(fill="x", padx=10, pady=10)
    

class LivroFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, id = None):
        super().__init__(parent, width=670, height=510, fg_color="transparent")
        self.grid(row=1, column=1, padx=20, pady=20, sticky="")
        self._paret = parent
        self.id_user = id

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
                # Checa se a tem uma capa referente ao livro, no banco de dados local
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
                descricao = descricao[:100] + '...'
            
            label_descricao = ctk.CTkLabel(info_frame, text=f"Descrição: {descricao}", font=("archivo.ttf", 11))
            label_descricao.pack(anchor="w")

            btns_frame = ctk.CTkFrame(info_frame)
            btns_frame.pack(anchor="w")

            btn = ctk.CTkButton(
                btns_frame, 
                corner_radius=15, 
                height=40, 
                text="Ver Mais...", 
                border_width=0, 
                command=lambda l=livro: LivroInfo(self._paret).livroInfo(l)
            )
            btn.pack(side="left", padx=5)  # Alinha os botões lado a lado

            # Botão "Adicionar à Lista"
            AdicionarLista = ctk.CTkButton(
                btns_frame, 
                corner_radius=15, 
                height=40, 
                text="Adicionar à Lista", 
                border_width=0, 
                command=lambda l=livro: LivrosSalvos(self.id_user).AdicionarLivros(l), 
                fg_color="green",
                hover_color="dark green"
            )
            AdicionarLista.pack(side="left", padx=5)