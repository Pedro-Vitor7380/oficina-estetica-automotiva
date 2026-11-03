import os
from classes import GerenciadorCarrinho, dadosCadastro
from gerador_pdf import gerar_orcamento_pdf

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def aguardar_voltar():
    while True:
        voltar = input("\n[ Aperte 'G' para voltar ao menu ]: ").strip().upper()
        if voltar == 'G':
            break

def iniciar_sistema():
    limpar_tela()
    
    print("="*45)
    print("Bem vindo ao sistema de Estética Automotiva")
    print("="*45)
    
    print("\n--- Passo 1: Dados de Cadastro ---")
    nome = input("Nome do cliente: ")
    telefone = input("Telefone do cliente: ")
    carro = input("Qual é o modelo do carro? ")
    placa = input("Placa do carro: ")
    
    cliente = dadosCadastro(nome, telefone, carro, placa)
    carrinho = GerenciadorCarrinho()
    
    mostrar_catalogo = False
    mensagem_aviso = f"Cadastro de {cliente.Nome} realizado com sucesso!"
    
    while True:
        limpar_tela()
        
        if mostrar_catalogo:
            print("--- CATÁLOGO DE SERVIÇOS ---")
            for id_servico, info in carrinho.catalogo.items():
                print(f"[{id_servico}] {info['servico']} - R$ {info['valor']:.2f}")
            print("-" * 30)
        
        print("--- Menu Principal ---")
        print(" 1 - Ver catalogo de serviços")
        print(" 2 - Adicionar Serviço")
        print(" 3 - Ver Carrinho / Remover itens")
        print(" 4 - Finalizar Pedido e Sair")
        print("-" * 30)
        
        if mensagem_aviso:
            print(f">> AVISO: {mensagem_aviso}")
            mensagem_aviso = "" 
        
        opcao = input("Escolha uma opção (1 a 4): ").strip()
        
        match opcao:
            case '1':
                mostrar_catalogo = True
                
            case '2':
                try:
                    id_escolhido = int(input("Digite o numero [ID] do serviço solicitado: "))
                    if id_escolhido in carrinho.catalogo:
                        carrinho.adicionar_ao_carrinho(id_escolhido)
                        nome_servico = carrinho.catalogo[id_escolhido]['servico']
                        mensagem_aviso = f"Serviço '{nome_servico}' adicionado com sucesso!"
                    else:
                        mensagem_aviso = "ID Inválido! Verifique o catálogo e tente novamente."
                except ValueError:
                    mensagem_aviso = "Por favor, digite apenas números válidos."
                    
            case '3':
                mensagem_carrinho = ""
                while True:
                    limpar_tela()
                    print("--- SEU CARRINHO ---")
                    carrinho.mostrar_carrinho()
                    print("-" * 30)
                    
                    if mensagem_carrinho:
                        print(f">> AVISO: {mensagem_carrinho}")
                        mensagem_carrinho = ""
                        
                    print("Opções do Carrinho:")
                    print(" [ ID ] - Digite o ID do serviço para remover")
                    print(" [ G  ] - Aperte G para voltar ao menu")
                    
                    opc_car = input("\nEscolha (ID ou G): ").strip().upper()
                    
                    if opc_car == 'G':
                        break
                    else:
                        try:
                            id_remover = int(opc_car)
                            carrinho.remover_do_carrinho(id_remover)
                            mensagem_carrinho = f"Comando aceito! Se o ID {id_remover} estava no carrinho, foi removido."
                        except ValueError:
                            mensagem_carrinho = "Opção invalida. Digite o ID para remover ou 'G' para voltar."
                            
            case '4':
                limpar_tela()
                print("--- FINALIZAR PEDIDO ---")
                carrinho.mostrar_carrinho()
                print("-" * 30)
                
                confirmacao = input("\nDeseja realmente fechar o pedido? (S/N): ").strip().upper()
                
                if confirmacao == 'S':
                    limpar_tela()
                    print("="*45)
                    print(" RESUMO DO PEDIDO FINALIZADO")
                    print("-" * 45)
                    print(f"Cliente: {cliente.Nome} | Tel: {cliente.Telefone}")
                    print(f"Veículo: {cliente.Carro} | Placa: {cliente.Placa}")
                    print("-" * 45)
                    
                    carrinho.mostrar_carrinho()
                    
                    print("="*45)
                    print("Obrigado pela preferência e volte sempre!\n")
                    gerar_orcamento_pdf(cliente, carrinho.carrinho, carrinho.catalogo)
                else:
                    print("\nFinalização cancelada.")
                    aguardar_voltar() # Pede o 'G' para voltar ao menu
            
            case _:
                mensagem_aviso = "Opção Inválida! Escolha um número de 1 a 4."

if __name__ == "__main__":
    iniciar_sistema()