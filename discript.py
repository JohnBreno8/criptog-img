def extrair_imagem(imagem_embutida_path, chave, tamanho_original, saida_path):
    imagem_embutida = Image.open(imagem_embutida_path)
    matriz_embutida = np.array(imagem_embutida).flatten()
    
    # Extrair os bits ocultos
    dados_ocultos = bytearray()
    for i in range(tamanho_original):
        dados_ocultos.append(matriz_embutida[i] & 1)
    
    fernet = Fernet(chave)
    imagem_original = fernet.decrypt(bytes(dados_ocultos))
    
    with open(saida_path, "wb") as file:
        file.write(imagem_original)
    print("Imagem original salva em", saida_path)

# Exemplo de uso
extrair_imagem("imagem_embutida.png", chave, len(imagem_oculta_criptografada), "imagem_revelada.jpg")
