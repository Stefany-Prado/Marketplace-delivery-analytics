# 📦 Marketplace Delivery Analytics

Projeto de análise de dados desenvolvido para investigar o comportamento dos pedidos, avaliar o desempenho operacional da logística de entrega e mensurar o impacto na experiência do cliente em um marketplace de delivery.

---

## 🎯 Objetivos do Projeto

- **Comportamento de Pedidos:** Identificar padrões de consumo, horários de pico e variação de ticket médio.
- **Desempenho Operacional:** Mapear gargalos logísticos, fatores de atraso (clima, distância, tempo de preparo) e eficiência das entregas.
- **Experiência do Cliente:** Analisar a relação entre o tempo total de entrega, atrasos e as notas de avaliação (NPS/Reviews).

---

## 📊 Estrutura dos Dados

A base contempla dados que simulam a operação do marketplace:

- **Pedidos & Clientes:** Identificadores únicos (`id_pedido`, `id_cliente`, `id_restaurante`, `id_entregador`).
- **Métricas Operacionais:** `distancia_km`, `tempo_entrega_min`, `tempo_prometido_min`, `valor_pedido`.
- **Fatores de Contexto:** `clima` (Ensolarado, Nublado, Chuvoso), `horario_pico` (Sim/Não).
- **Satisfação:** `atrasado` (Flag booleana), `minutos_atraso`, `avaliacao` (1 a 5 estrelas).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Pandas** & **NumPy** (Manipulação, limpeza e geração de dados)



=======
>>>>>>> d587ff3eae0c9afb60ec7c7b30fb47f9ef3d6178
