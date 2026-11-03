import os
import tkinter as tk
import unicodedata
from datetime import datetime
from tkinter import messagebox

# Dados da oficina (troque pelos dados reais)
OFICINA_NOME = "Nome da Oficina"
OFICINA_ENDERECO = "Endereço da Oficina"
OFICINA_TELEFONE = "(00) 0000-0000"

# Pasta onde os PDFs vão ser salvos
PASTA_SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orcamentos")

# Tamanho da folha A4 em pontos
LARGURA_PAGINA = 595
ALTURA_PAGINA = 842


def gerar_orcamento_pdf(cliente, itens, catalogo=None):
    # O catalogo vem do main.py, mas não é usado aqui
    total = 0
    for item in itens:
        total = total + item["valor"]

    janela = tk.Tk()
    janela.title("Orçamento - Estética Automotiva")
    janela.resizable(False, False)

    frame = tk.Frame(janela, padx=20, pady=20)
    frame.pack()

    tk.Label(frame, text=OFICINA_NOME, font=("Arial", 16, "bold")).pack(anchor="w")
    tk.Label(frame, text="Cliente: " + cliente.Nome).pack(anchor="w")
    tk.Label(frame, text="Telefone: " + cliente.Telefone).pack(anchor="w")
    tk.Label(frame, text="Veículo: " + cliente.Carro + " | Placa: " + cliente.Placa).pack(anchor="w", pady=(0, 10))

    lista = tk.Listbox(frame, width=60, height=10)
    for item in itens:
        lista.insert(tk.END, item["servico"] + " - R$ " + "%.2f" % item["valor"])
    lista.pack(fill="x")

    tk.Label(frame, text="TOTAL: R$ " + "%.2f" % total, font=("Arial", 12, "bold")).pack(anchor="e", pady=10)

    status = tk.Label(frame, text="", fg="green")
    status.pack()

    def clicou_em_gerar():
        try:
            caminho = criar_pdf(cliente, itens, total)
        except OSError as erro:
            messagebox.showerror("Erro", "Não foi possível salvar o PDF: " + str(erro), parent=janela)
            return
        status.config(text="PDF salvo em: " + caminho)

    botao = tk.Button(frame, text="Gerar PDF", command=clicou_em_gerar, width=20)
    botao.pack(pady=(10, 0))

    janela.mainloop()


def criar_pdf(cliente, itens, total):
    # Cria a pasta de saída se ela ainda não existir
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    # Monta o nome do arquivo usando só as letras e números da placa
    placa_limpa = ""
    for letra in cliente.Placa:
        if letra.isalnum():
            placa_limpa = placa_limpa + letra
    if placa_limpa == "":
        placa_limpa = "semplaca"

    agora = datetime.now()
    nome_arquivo = "orcamento_" + placa_limpa + "_" + agora.strftime("%Y%m%d_%H%M%S") + ".pdf"
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

    # Cada item da lista comandos é uma linha que vai dentro do PDF
    comandos = []

    # Fundo cinza claro, igual ao da janela do Tkinter
    comandos.append(retangulo_pdf(0, 0, LARGURA_PAGINA, ALTURA_PAGINA, "0.941 0.941 0.941"))

    # Nome e endereço da oficina, do lado esquerdo
    comandos.append(texto_pdf(30, 52, OFICINA_NOME, 16, negrito=True))
    comandos.append(texto_pdf(30, 72, OFICINA_ENDERECO, 11))
    comandos.append(texto_pdf(30, 90, "Tel: " + OFICINA_TELEFONE, 11))

    # Título e data, do lado direito
    comandos.append(texto_pdf(565, 52, "ORÇAMENTO", 14, negrito=True, alinhar_direita=True))
    comandos.append(texto_pdf(565, 72, "Data: " + agora.strftime("%d/%m/%Y"), 11, alinhar_direita=True))

    # Dados do cliente e do carro, uma linha cada
    comandos.append(texto_pdf(30, 125, "Cliente: " + cliente.Nome, 11))
    comandos.append(texto_pdf(30, 147, "Telefone: " + cliente.Telefone, 11))
    comandos.append(texto_pdf(30, 169, "Veículo: " + cliente.Carro + " | Placa: " + cliente.Placa, 11))

    # Caixa branca com borda cinza, como a Listbox da janela (sempre com pelo menos 10 linhas)
    linhas_caixa = max(len(itens), 10)
    altura_caixa = linhas_caixa * 18 + 8
    comandos.append(caixa_pdf(30, 190, 535, altura_caixa))

    topo = 194
    for item in itens:
        comandos.append(texto_pdf(36, topo + 13, item["servico"] + " - R$ " + "%.2f" % item["valor"], 11))
        topo = topo + 18

    # Total em negrito, alinhado à direita da caixa, como o label TOTAL da janela
    comandos.append(texto_pdf(565, 190 + altura_caixa + 30, "TOTAL: R$ " + "%.2f" % total, 12, negrito=True, alinhar_direita=True))

    conteudo = "\n".join(comandos)
    pdf = montar_pdf(conteudo)

    arquivo = open(caminho, "wb")
    arquivo.write(pdf.encode("cp1252", errors="replace"))
    arquivo.close()
    return caminho


# Largura de cada caractere da Helvetica, do espaço (32) até o til (126).
# Usada para alinhar os textos à direita.
LARGURAS_NORMAL = [
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
    556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
    1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
    333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
    556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584,
]

LARGURAS_NEGRITO = [
    278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278,
    556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611,
    975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556,
    333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611,
    611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584,
]


def largura_texto(texto, tamanho, negrito=False):
    tabela = LARGURAS_NORMAL
    if negrito:
        tabela = LARGURAS_NEGRITO

    largura = 0
    for letra in texto:
        # Letra com acento (ex.: Ç, ã) usa a largura da letra sem acento
        base = unicodedata.normalize("NFD", letra)[0]
        if 32 <= ord(base) <= 126:
            largura = largura + tabela[ord(base) - 32]
        else:
            largura = largura + 556
    return largura * tamanho / 1000


def texto_pdf(x, topo, texto, tamanho, negrito=False, cor="0 0 0", alinhar_direita=False):
    # O PDF conta a posição de baixo para cima, então a altura é ajustada aqui
    y = ALTURA_PAGINA - topo
    if alinhar_direita:
        x = x - largura_texto(texto, tamanho, negrito)

    if negrito:
        fonte = "F2"
    else:
        fonte = "F1"

    # Parênteses e barras precisam de \ na frente para não quebrar o PDF
    texto_seguro = texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    return cor + " rg\nBT /" + fonte + " " + str(tamanho) + " Tf " + str(x) + " " + str(y) + " Td (" + texto_seguro + ") Tj ET"


def retangulo_pdf(x, topo, largura, altura, cor):
    y = ALTURA_PAGINA - topo - altura
    return cor + " rg " + str(x) + " " + str(y) + " " + str(largura) + " " + str(altura) + " re f"


def caixa_pdf(x, topo, largura, altura):
    # Retângulo branco com borda cinza, como a área da lista na janela
    y = ALTURA_PAGINA - topo - altura
    return "1 1 1 rg 0.478 RG 0.75 w " + str(x) + " " + str(y) + " " + str(largura) + " " + str(altura) + " re B"


def montar_pdf(conteudo):
    # Cada objeto é uma parte do arquivo PDF
    objetos = []
    objetos.append("<< /Type /Catalog /Pages 2 0 R >>")
    objetos.append("<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objetos.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 " + str(LARGURA_PAGINA) + " " + str(ALTURA_PAGINA) + "] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>")
    objetos.append("<< /Length " + str(len(conteudo)) + " >>\nstream\n" + conteudo + "\nendstream")
    objetos.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    objetos.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

    pdf = "%PDF-1.4\n"

    # Guarda a posição de cada objeto para a tabela xref
    posicoes = []
    numero = 1
    for objeto in objetos:
        posicoes.append(len(pdf))
        pdf = pdf + str(numero) + " 0 obj\n" + objeto + "\nendobj\n"
        numero = numero + 1

    inicio_xref = len(pdf)
    pdf = pdf + "xref\n0 " + str(len(objetos) + 1) + "\n"
    pdf = pdf + "0000000000 65535 f \n"
    for posicao in posicoes:
        pdf = pdf + ("%010d" % posicao) + " 00000 n \n"
    pdf = pdf + "trailer\n<< /Size " + str(len(objetos) + 1) + " /Root 1 0 R >>\n"
    pdf = pdf + "startxref\n" + str(inicio_xref) + "\n%%EOF\n"
    return pdf
