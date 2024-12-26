1. Conceito do Sistema

O sistema combina criptografia (para proteger os dados da imagem escondida) e esteganografia (para ocultar esses dados em outra imagem). Isso garante que, mesmo se alguém acessar a imagem "disfarce", não será capaz de recuperar a imagem original sem a senha correta.

Partes do Sistema

Imagem Oculta: A imagem que você deseja esconder.

Imagem Disfarce: A imagem visível que será usada para ocultar a imagem original.

Senha (Chave Criptográfica): Uma chave única para criptografar e descriptografar a imagem oculta.

Imagem Embutida: O resultado da fusão entre a imagem disfarce e os dados da imagem oculta.



---

2. Fluxo do Processo

Fase 1: Esconder a Imagem

1. Gerar uma Chave Criptográfica:

A chave é gerada usando um algoritmo de criptografia simétrica (por exemplo, Fernet da biblioteca cryptography).



2. Criptografar a Imagem Oculta:

A imagem é lida em formato binário.

A chave criptográfica é usada para transformar os dados da imagem em um formato protegido e ilegível.



3. Embutir os Dados Criptografados na Imagem Disfarce:

Os dados criptografados da imagem oculta são transformados em bits.

Esses bits são embutidos nos últimos bits dos pixels da imagem disfarce. Isso é feito porque alterar os últimos bits de um pixel tem um impacto visual imperceptível.



4. Salvar a Imagem Embutida:

A nova imagem (que contém os dados criptografados) é salva.





---

Fase 2: Revelar a Imagem

1. Extrair os Bits Ocultos da Imagem Embutida:

Os bits dos dados ocultos são extraídos dos últimos bits de cada pixel da imagem embutida.



2. Descriptografar os Dados:

Usando a mesma chave que foi utilizada para criptografar, os dados são descriptografados para recuperar os bytes da imagem original.



3. Salvar a Imagem Revelada:

Os dados da imagem original são escritos em um arquivo, restaurando a imagem escondida.





---

3. Implementação Técnica

Aqui está uma explicação detalhada do código apresentado anteriormente:

Função: Gerar Chave

def gerar_chave():
    return Fernet.generate_key()

Gera uma chave criptográfica aleatória.

Essa chave é essencial para proteger e recuperar a imagem oculta.



---

Função: Criptografar Imagem

def criptografar_imagem(imagem_path, chave):
    with open(imagem_path, "rb") as file:
        imagem_bytes = file.read()
    fernet = Fernet(chave)
    return fernet.encrypt(imagem_bytes)

Abre a imagem oculta em modo binário (rb).

Criptografa os dados binários usando a chave gerada.

Retorna os dados criptografados.



---

Função: Esconder Imagem

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

Etapas:

1. Carrega a imagem disfarce e converte seus pixels em uma matriz NumPy.


2. Verifica se a imagem disfarce tem espaço suficiente para armazenar os dados da imagem oculta.


3. Modifica os últimos bits de cada pixel para embutir os dados da imagem oculta criptografada.


4. Salva a nova imagem.





---

Função: Extrair e Descriptografar Imagem

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

Etapas:

1. Carrega a imagem embutida e lê os últimos bits de cada pixel.


2. Recupera os dados da imagem oculta no formato criptografado.


3. Usa a chave para descriptografar os dados, restaurando a imagem original.


4. Salva a imagem restaurada.





---

4. Considerações de Segurança

Proteção da Chave:

A chave criptográfica deve ser mantida em sigilo. Se for perdida, a imagem oculta não poderá ser recuperada.


Compressão de Dados:

Se a imagem oculta for grande, comprimi-la antes de criptografá-la pode ajudar.



5. Possíveis Melhorias

Suporte para Senhas:

Permitir que o usuário digite uma senha que será convertida em uma chave criptográfica.


Interface Gráfica:

Criar um programa com interface gráfica para simplificar o uso.


Formatos Avançados:

Adicionar suporte para outros formatos de imagem (como PNG, BMP).
