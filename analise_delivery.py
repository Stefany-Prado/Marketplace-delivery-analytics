import os
import pandas as pd
import numpy as np

NOME_ARQUIVO = "pedidos_delivery.csv"

def carregar_ou_criar_dados():
    """Carrega a base existente ou cria uma nova base com dados sintéticos caso não exista."""
    if os.path.exists(NOME_ARQUIVO):
        print(f"-> Base de dados '{NOME_ARQUIVO}' carregada com sucesso!")
        return pd.read_csv(NOME_ARQUIVO)
    
    print("-> Criando base de dados inicial com 1000 pedidos...")
    np.random.seed(42)
    n_pedidos = 1000

    dados = {
        "id_pedido": range(1001, 1001 + n_pedidos),
        "id_cliente": np.random.randint(1, 200, n_pedidos),
        "id_restaurante": np.random.randint(1, 30, n_pedidos),
        "id_entregador": np.random.randint(1, 50, n_pedidos),
        "distancia_km": np.round(np.random.uniform(1.0, 15.0, n_pedidos), 2),
        "valor_pedido": np.round(np.random.uniform(20.0, 200.0, n_pedidos), 2),
        "clima": np.random.choice(["Ensolarado", "Nublado", "Chuvoso"], n_pedidos, p=[0.6, 0.25, 0.15]),
        "horario_pico": np.random.choice([0, 1], n_pedidos, p=[0.6, 0.4]),
    }

    df = pd.DataFrame(dados)

    # Regras operacionais
    tempo_transito_base = 15 + (df["distancia_km"] * 3)
    tempo_preparo_restaurante = np.random.randint(10, 30, n_pedidos)
    adicional_clima = np.where(df["clima"] == "Chuvoso", 15, np.where(df["clima"] == "Nublado", 5, 0))
    adicional_pico = np.where(df["horario_pico"] == 1, 12, 0)

    df["tempo_entrega_min"] = (tempo_transito_base + tempo_preparo_restaurante + adicional_clima + adicional_pico + np.random.normal(0, 4, n_pedidos)).astype(int)
    df["tempo_prometido_min"] = (tempo_transito_base + 20).astype(int)
    df["atrasado"] = (df["tempo_entrega_min"] > df["tempo_prometido_min"]).astype(int)
    df["minutos_atraso"] = np.maximum(0, df["tempo_entrega_min"] - df["tempo_prometido_min"])
    df["avaliacao"] = np.clip(np.round(5.0 - (df["minutos_atraso"] * 0.12) - np.random.uniform(0, 0.4, n_pedidos), 1), 1.0, 5.0)

    df.to_csv(NOME_ARQUIVO, index=False, encoding="utf-8-sig")
    return df


def adicionar_novo_pedido(df):
    """Permite ao usuário digitar manualmente as informações de um novo pedido."""
    print("\n--- ➕ ADICIONAR NOVO PEDIDO ---")
    try:
        novo_id = df["id_pedido"].max() + 1 if not df.empty else 1001
        cliente = int(input("ID do Cliente (ex: 15): "))
        restaurante = int(input("ID do Restaurante (ex: 3): "))
        entregador = int(input("ID do Entregador (ex: 8): "))
        distancia = float(input("Distância em km (ex: 4.5): "))
        valor = float(input("Valor do pedido em R$ (ex: 65.90): "))
        
        print("\nCondições climáticas: 1 - Ensolarado | 2 - Nublado | 3 - Chuvoso")
        op_clima = input("Escolha a opção (1/2/3): ")
        clima_map = {"1": "Ensolarado", "2": "Nublado", "3": "Chuvoso"}
        clima = clima_map.get(op_clima, "Ensolarado")

        pico = int(input("É horário de pico? (1 para Sim / 0 para Não): "))
        tempo_prometido = int(input("Tempo prometido em minutos (ex: 40): "))
        tempo_real = int(input("Tempo real gasto na entrega em minutos (ex: 48): "))
        avaliacao = float(input("Nota da avaliação (1.0 a 5.0): "))

        # Cálculo das métricas derivadas
        atrasado = 1 if tempo_real > tempo_prometido else 0
        minutos_atraso = max(0, tempo_real - tempo_prometido)

        novo_registro = {
            "id_pedido": novo_id,
            "id_cliente": cliente,
            "id_restaurante": restaurante,
            "id_entregador": entregador,
            "distancia_km": distancia,
            "valor_pedido": valor,
            "clima": clima,
            "horario_pico": pico,
            "tempo_entrega_min": tempo_real,
            "tempo_prometido_min": tempo_prometido,
            "atrasado": atrasado,
            "minutos_atraso": minutos_atraso,
            "avaliacao": avaliacao
        }

        # Concatena o novo pedido no DataFrame
        df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
        df.to_csv(NOME_ARQUIVO, index=False, encoding="utf-8-sig")
        print(f"\n✅ Pedido #{novo_id} adicionado e salvo com sucesso em '{NOME_ARQUIVO}'!")

    except ValueError:
        print("\n❌ Erro: Por favor, digite valores numéricos válidos nos campos correspondentes.")

    return df


def analisar_fatores_atraso(df):
    """Realiza a análise exploratória e exibe as estatísticas gerais."""
    if df.empty:
        print("\nNenhum dado disponível para análise.")
        return

    print("\n==================================================")
    print(" 🚚 RELATÓRIO DE DESEMPENHO OPERACIONAL & ATRASOS ")
    print("==================================================\n")

    print(f"Total de Pedidos Analisados: {len(df)}")
    print(f"Ticket Médio: R$ {df['valor_pedido'].mean():.2f}")
    print(f"Tempo Médio de Entrega: {df['tempo_entrega_min'].mean():.1f} min")
    print(f"Taxa Geral de Atraso: {(df['atrasado'].mean() * 100):.1f}%\n")

    print("--- IMPACTO DO CLIMA ---")
    print(df.groupby("clima").agg(
        qtd=("id_pedido", "count"),
        taxa_atraso=("atrasado", lambda x: f"{x.mean()*100:.1f}%"),
        tempo_medio=("tempo_entrega_min", "mean"),
        avaliacao=("avaliacao", "mean")
    ))

    print("\n--- IMPACTO DO HORÁRIO DE PICO (0 = Não, 1 = Sim) ---")
    print(df.groupby("horario_pico").agg(
        qtd=("id_pedido", "count"),
        taxa_atraso=("atrasado", lambda x: f"{x.mean()*100:.1f}%"),
        tempo_medio=("tempo_entrega_min", "mean"),
        avaliacao=("avaliacao", "mean")
    ))
    print("\n==================================================")


def menu_principal():
    df = carregar_ou_criar_dados()

    while True:
        print("\n--- MENU DE OPÇÕES ---")
        print("1. Visualizar Relatório de Atrasos")
        print("2. Adicionar Novo Pedido")
        print("3. Sair")
        
        opcao = input("Escolha uma opção (1-3): ").strip()

        if opcao == "1":
            analisar_fatores_atraso(df)
        elif opcao == "2":
            df = adicionar_novo_pedido(df)
        elif opcao == "3":
            print("\nSaindo... Bons estudos!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu_principal()