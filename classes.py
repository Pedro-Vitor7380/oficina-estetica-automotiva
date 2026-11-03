class GerenciadorCarrinho:
    def __init__(self):
        self.catalogo = {
            1: {"servico": "Lavagem Simples", "valor": 70.00},
            2: {"servico": "Lavagem Detalhada", "valor": 150.00},
            3: {"servico": "Lavagem de Chassis", "valor": 90.00},
            4: {"servico": "Lavagem de Motor a Seco", "valor": 120.00},
            5: {"servico": "Descontaminação de Pintura", "valor": 100.00},
            6: {"servico": "Limpeza Detalhada de Rodas e Caixas de Roda", "valor": 180.00},
            7: {"servico": "Enceramento Técnico", "valor": 120.00},
            8: {"servico": "Selante de Pintura", "valor": 250.00},
            9: {"servico": "Polimento Comercial", "valor": 350.00},
            10: {"servico": "Polimento Técnico - 1 Etapa", "valor": 500.00},
            11: {"servico": "Polimento Técnico - 2 Etapas", "valor": 800.00},
            12: {"servico": "Polimento Técnico - 3 Etapas", "valor": 1100.00},
            13: {"servico": "Cristalização de Pintura", "valor": 600.00},
            14: {"servico": "Vitrificação de Pintura (1 Ano)", "valor": 1200.00},
            15: {"servico": "Vitrificação de Pintura (3 Anos)", "valor": 1800.00},
            16: {"servico": "Higienização Interna Completa", "valor": 400.00},
            17: {"servico": "Higienização de Bancos de Tecido", "valor": 200.00},
            18: {"servico": "Limpeza e Hidratação de Bancos de Couro", "valor": 250.00},
            19: {"servico": "Impermeabilização de Tecidos", "valor": 300.00},
            20: {"servico": "Higienização de Teto", "valor": 150.00},
            21: {"servico": "Oxi-sanitização (Remoção de Odores)", "valor": 120.00},
            22: {"servico": "Cristalização de Vidros", "valor": 100.00},
            23: {"servico": "Remoção de Chuva Ácida dos Vidros", "valor": 150.00},
            24: {"servico": "Polimento de Faróis", "valor": 150.00},
            25: {"servico": "Vitrificação de Faróis", "valor": 250.00},
            26: {"servico": "Revitalização de Plásticos Externos", "valor": 120.00},
            27: {"servico": "Vitrificação de Plásticos", "valor": 300.00}
        }
        self.carrinho = []

    def adicionar_ao_carrinho(self, id_produto):
        item = self.catalogo[id_produto]
        self.carrinho.append({
            "id": id_produto,
            "servico": item["servico"],
            "valor": item["valor"]
        })
        print(f"Adicionado: {item['servico']} - R$ {item['valor']:.2f}")

    def mostrar_carrinho(self):
        print("\n--- SEU CARRINHO ---")
        total = 0
        for item in self.carrinho:
            print(f"[{item['id']}] {item['servico']}: R$ {item['valor']:.2f}")
            total += item['valor']
            
        print("-" * 20)
        print(f"TOTAL: R$ {total:.2f}")

    # Método movido para DENTRO da classe GerenciadorCarrinho
    def remover_do_carrinho(self, id_servico):
        for item in self.carrinho:
            if item['id'] == id_servico:
                self.carrinho.remove(item)
                break


class dadosCadastro:
    def __init__(self, nome, telefone, carro, placa):
        self.Nome = nome
        self.Telefone = telefone
        self.Carro = carro
        self.Placa = placa