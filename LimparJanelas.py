class LimparJanelas:
    def limpa_janela_principal(self):
        self.frame.place_forget()
        self.barra_pesquisa.place_forget()
        self.botão_pesquisa.place_forget()
        self.bestsellers.grid_forget()
    
    def limpar_janela_pesquisa(self):
        self.frame.place_forget()
        self.botão_voltar.place_forget()
        self.label_image.place_forget()
        self.label.place_forget()
        self.janela_principal()

    def limpar_janela(self):
        self.frame_livro.place_forget()
        self.imagem.place_forget()
        self.botão_voltar.place_forget()
        self.label.place_forget()

        self.janela_principal()

    def limpar_janela_config(self):
        self.frame.place_forget()
        self.botão_voltar.place_forget()

        self.janela_principal()