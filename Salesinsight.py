import re
import csv
import random
from datetime import datetime, timedelta

def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    #Gera um dataset sintetico de vendas com dados sujos e grava em CSV

    random.seed(seed)

    produtos = [
        "Notebook",
        "Smartphone",
        "Tablet",
        "Monitor",
        "Teclado",
        "Mouse",
        "Headset"
    ]

    categorias = {
        "Notebook": "Computadores",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Computadores",
        "Teclado": "Perifericos",
        "Mouse": "Perifericos",
        "Headset": "Perifericos"
    }

    precos = {
        "Notebook": 3500,
        "Smartphone": 2200,
        "Tablet": 1800,
        "Monitor": 1200,
        "Teclado": 250,
        "Mouse": 120,
        "Headset": 350
    }

    regioes = [
        "Sudeste",
        "Sul",
        "Nordeste",
        "Centro-Oeste",
        "Norte"
    ]

    data_inicio = datetime(2025, 1, 1)

    colunas = [
        "id_venda",
        "data_venda",
        "cliente",
        "produto",
        "categoria",
        "regiao",
        "quantidade",
        "preco_unitario"
    ]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas
        )

        escritor.writeheader()

        for i in range(n_registros):

            produto = random.choice(produtos)
            categoria = categorias[produto]

            quantidade = random.randint(1, 10)

            preco = round(
                precos[produto] * random.uniform(0.85, 1.15),
                2
            )

            data = data_inicio + timedelta(
                days=random.randint(0, 364)
            )

            data_txt = data.strftime("%Y-%m-%d")

            cliente = f"Cliente_{random.randint(1, 50):03d}"

            # Sujeira proposital para a etapa de limpeza

            if random.random() < 0.05:
                quantidade = ""

            if random.random() < 0.04:
                preco = ""

            if random.random() < 0.06:
                produto = " " + produto + " "

            if random.random() < 0.03:
                data_txt = "DATA INVALIDA"

            if random.random() < 0.10:
                cliente = random.choice([
                    cliente.upper().replace("_", "-"),
                    cliente + "!!",
                    " " + cliente,
                    cliente.replace("Cliente_", "cliente#")
                ])

            escritor.writerow({
                "id_venda": i + 1,
                "data_venda": data_txt,
                "cliente": cliente,
                "produto": produto,
                "categoria": categoria,
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco
            })

    print(f"Dataset gerado com {n_registros} registros em {caminho_csv}.")

gerar_dataset_vendas()

def carregar_dataset(caminho_csv):
    #Carrega o dataset CSV e retorna uma lista de dicionários

    registros = []

    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            registros.append(linha)

    return registros

registros = carregar_dataset("vendas.csv")

def inspecionar_dados(registros):
    #Exibe informações iniciais sobre o dataset

    print(f"\n=== INSPECAO INICIAL DO DATASET ===")

    print(f"\nTotal de registros: {len(registros)}")

    if registros:
        print("\nColunas:")
        print(list(registros[0].keys()))

    print("\nValores ausentes:")

    colunas = registros[0].keys()

    for coluna in colunas:
        ausentes = 0

        for registro in registros:
            if registro[coluna] == "":
                ausentes += 1

        print(f"{coluna}: {ausentes}")

    print("\nPrimeiros registros:")

    for registro in registros[:5]:
        print(registro)

inspecionar_dados(registros)
PADRAO_CLIENTE = re.compile(r"[^A-Za-z0-9_-]")

def limpar_dados(registros):
    #Limpa os registros e remove dados inválidos

    registros_limpos = []

    removidos_data = 0
    removidos_nulos = 0

    for registro in registros:

        # Limpeza dos textos
        cliente = registro["cliente"].strip()
        cliente = re.sub(PADRAO_CLIENTE, "", cliente)

        produto = registro["produto"].strip()

        # Verificação da data
        try:
            data = datetime.strptime(
                registro["data_venda"],
                "%Y-%m-%d"
            )
        except ValueError:
            removidos_data += 1
            continue

        # Verificação de valores ausentes
        if (
            registro["quantidade"] == ""
            or registro["preco_unitario"] == ""
        ):
            removidos_nulos += 1
            continue

        # Conversão dos tipos
        quantidade = int(registro["quantidade"])
        preco_unitario = float(registro["preco_unitario"])

        # Atualização do registro
        registro["cliente"] = cliente
        registro["produto"] = produto
        registro["data_venda"] = data.strftime("%Y-%m-%d")
        registro["quantidade"] = quantidade
        registro["preco_unitario"] = preco_unitario

        registros_limpos.append(registro)

    relatorio = {
        "iniciais": len(registros),
        "removidos_data": removidos_data,
        "removidos_nulos": removidos_nulos,
        "finais": len(registros_limpos)
    }

    return registros_limpos, relatorio

# Relatorio de limpeza
registros_limpos, relatorio = limpar_dados(registros)

print("\n=== RELATORIO DE LIMPEZA ===")

print(f"Registros iniciais: {relatorio['iniciais']}")
print(
    f"Removidos por data invalida: "
    f"{relatorio['removidos_data']}"
)
print(
    f"Removidos por valores nulos: "
    f"{relatorio['removidos_nulos']}"
)
print(f"Registros finais: {relatorio['finais']}")

def criar_colunas_derivadas(registros):
    # Cria novas informações a partir dos dados limpos

    meses = [
        "Janeiro",
        "Fevereiro",
        "Marco",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    for registro in registros:

        data = datetime.strptime(
            registro["data_venda"],
            "%Y-%m-%d"
        )

        receita = (
            registro["quantidade"]
            * registro["preco_unitario"]
        )

        registro["receita_total"] = round(receita, 2)

        registro["mes"] = data.month

        registro["mes_nome"] = meses[data.month - 1]

        registro["trimestre"] = f"Q{((data.month - 1) // 3) + 1}"

        registro["ano"] = data.year

        if receita < 1000:
            registro["faixa_receita_item"] = "Baixo Valor"
        elif receita <= 5000:
            registro["faixa_receita_item"] = "Medio Valor"
        else:
            registro["faixa_receita_item"] = "Alto Valor"

    return registros

registros_limpos = criar_colunas_derivadas(registros_limpos)

print("\n=== DADOS APOS TRANSFORMACAO ===")

for registro in registros_limpos[:3]:
    print(
        f"ID: {registro['id_venda']} | "
        f"Data: {registro['data_venda']} | "
        f"Cliente: {registro['cliente']} | "
        f"Produto: {registro['produto']} | "
        f"Categoria: {registro['categoria']} | "
        f"Região: {registro['regiao']} | "
        f"Quantidade: {registro['quantidade']} | "
        f"Preço: R$ {registro['preco_unitario']:.2f} | "
        f"Receita: R$ {registro['receita_total']:.2f} | "
        f"Mês: {registro['mes_nome']} | "
        f"Trimestre: {registro['trimestre']} | "
        f"Ano: {registro['ano']} | "
        f"Faixa: {registro['faixa_receita_item']}"
    )

def calcular_metricas(registros):
    #Calcula métricas agregadas por mês, produto, categoria e região

    por_mes = {}
    por_produto = {}
    por_categoria = {}
    por_regiao = {}

    for registro in registros:

        # -------------------------
        # POR MÊS
        # -------------------------
        mes = registro["mes"]

        if mes not in por_mes:
            por_mes[mes] = {
                "mes": mes,
                "receita_total": 0,
                "quantidade": 0,
                "n_vendas": 0
            }

        por_mes[mes]["receita_total"] += registro["receita_total"]
        por_mes[mes]["quantidade"] += registro["quantidade"]
        por_mes[mes]["n_vendas"] += 1

        # -------------------------
        # POR PRODUTO
        # -------------------------
        produto = registro["produto"]

        if produto not in por_produto:
            por_produto[produto] = 0

        por_produto[produto] += registro["receita_total"]

        # -------------------------
        # POR CATEGORIA
        # -------------------------
        categoria = registro["categoria"]

        if categoria not in por_categoria:
            por_categoria[categoria] = 0

        por_categoria[categoria] += registro["receita_total"]

        # -------------------------
        # POR REGIÃO
        # -------------------------
        regiao = registro["regiao"]

        if regiao not in por_regiao:
            por_regiao[regiao] = {
                "regiao": regiao,
                "receita_total": 0,
                "n_vendas": 0
            }

        por_regiao[regiao]["receita_total"] += registro["receita_total"]
        por_regiao[regiao]["n_vendas"] += 1

    # Transformar os dicionários em listas

    lista_mes = list(por_mes.values())

    for item in lista_mes:
        item["receita_total"] = round(item["receita_total"], 2)

    lista_produtos = []

    for produto, receita in por_produto.items():
        lista_produtos.append({
            "produto": produto,
            "receita_total": round(receita, 2)
        })

    lista_produtos.sort(
        key=lambda item: item["receita_total"],
        reverse=True
    )

    top_produtos = lista_produtos[:5]

    lista_categorias = []

    for categoria, receita in por_categoria.items():
        lista_categorias.append({
            "categoria": categoria,
            "receita_total": round(receita, 2)
        })

    lista_categorias.sort(
        key=lambda item: item["receita_total"],
        reverse=True
    )

    lista_regioes = []

    for regiao, dados in por_regiao.items():

        ticket_medio = (
            dados["receita_total"] / dados["n_vendas"]
        )

        lista_regioes.append({
            "regiao": regiao,
            "receita_total": round(dados["receita_total"], 2),
            "ticket_medio": round(ticket_medio, 2)
        })

    lista_regioes.sort(
        key=lambda item: item["receita_total"],
        reverse=True
    )

    metricas = {
        "por_mes": lista_mes,
        "top_produtos": top_produtos,
        "por_categoria": lista_categorias,
        "por_regiao": lista_regioes
    }

    return metricas

def exibir_metricas(metricas):
    #Exibe as métricas agregadas no terminal

    print("\n=== POR MES ===")

    for item in metricas["por_mes"]:
        print(
            f"Mês: {item['mes']} | "
            f"Receita: R$ {item['receita_total']:.2f} | "
            f"Quantidade: {item['quantidade']} | "
            f"Vendas: {item['n_vendas']}"
        )

    print("\n=== TOP 5 PRODUTOS ===")

    for item in metricas["top_produtos"]:
        print(
            f"{item['produto']} | "
            f"Receita: R$ {item['receita_total']:.2f}"
        )

    print("\n=== POR CATEGORIA ===")

    for item in metricas["por_categoria"]:
        print(
            f"{item['categoria']} | "
            f"Receita: R$ {item['receita_total']:.2f}"
        )

    print("\n=== POR REGIAO ===")

    for item in metricas["por_regiao"]:
        print(
            f"{item['regiao']} | "
            f"Receita: R$ {item['receita_total']:.2f} | "
            f"Ticket médio: R$ {item['ticket_medio']:.2f}"
        )

def segmentar_clientes(registros):
    #Agrupa clientes, calcula gasto e classifica em Bronze, Prata ou Ouro

    classificar = lambda total: (
        "Ouro"
        if total > 15000
        else "Prata"
        if total >= 5000
        else "Bronze"
    )

    total_por_cliente = {}

    for registro in registros:

        cliente = registro["cliente"]

        if cliente not in total_por_cliente:
            total_por_cliente[cliente] = 0

        total_por_cliente[cliente] += registro["receita_total"]

    clientes = []

    for nome, total in total_por_cliente.items():

        clientes.append({
            "cliente": nome,
            "total_gasto": round(total, 2),
            "segmento": classificar(total)
        })

    clientes.sort(
        key=lambda cliente: cliente["total_gasto"],
        reverse=True
    )

    return clientes

def exibir_segmentacao(clientes):
    #Exibe os 10 maiores clientes e a distribuição dos segmentos
    print("ENTREI NA FUNÇÃO EXIBIR_SEGMENTACAO")
    print("\n=== TOP 10 CLIENTES ===")

    for cliente in clientes[:10]:
        print(
            f"{cliente['cliente']} | "
            f"Gasto: R$ {cliente['total_gasto']:.2f} | "
            f"Segmento: {cliente['segmento']}"
        )

    distribuicao = {
        "Bronze": 0,
        "Prata": 0,
        "Ouro": 0
    }

    for cliente in clientes:
        distribuicao[cliente["segmento"]] += 1

    print("\n=== DISTRIBUICAO DOS CLIENTES ===")

    for segmento, quantidade in distribuicao.items():
        print(f"{segmento}: {quantidade}")
