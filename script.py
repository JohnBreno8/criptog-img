from cryptography.fernet import Fernet
from PIL import Image
import numpy as np

def gerar_chave():
    return Fernet.generate_key()

def criptografar_imagem(imagem_path, chave):
    with open(imagem_path, "rb") as file:
        imagem_bytes = file.read()
    fernet = Fernet(chave)
    return fernet.encrypt(imagem_bytes)

def esconder_imagem(imagem_disfarce_path, imagem_oculta_criptografada, saida_path):
    imagem_disfarce = Image.open(imagem_disfarce_path)
    matriz_disfarce = np.array(imagem_disfarce)
    
    # Certifique-se de que a imagem criptografada cabe no espaço disponível
    tamanho = len(imagem_oculta_criptografada)
    if tamanho > matriz_disfarce.size:
        raise ValueError("A imagem oculta é muito grande para a imagem disfarce.")
    
    # Embutir os dados na imagem disfarce (nos últimos bits)
    matriz_disfarce = matriz_disfarce.flatten()
    for i in range(tamanho):
        matriz_disfarce[i] = (matriz_disfarce[i] & ~1) | (imagem_oculta_criptografada[i] % 2)
    matriz_disfarce = matriz_disfarce.reshape(np.array(imagem_disfarce).shape)
    
    imagem_embutida = Image.fromarray(matriz_disfarce)
    imagem_embutida.save(saida_path)

# Exemplo de uso
chave = gerar_chave()
imagem_oculta_criptografada = criptografar_imagem("imagem_oculta.jpg", chave)
esconder_imagem("imagem_disfarce.jpg", imagem_oculta_criptografada, "imagem_embutida.png")
print("Imagem embutida salva em 'imagem_embutida.png'. Chave:", chave.decode())
