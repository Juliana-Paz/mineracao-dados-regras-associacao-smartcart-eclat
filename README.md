# 🛒 SmartCart — Sistema de Recomendação por Regras de Associação

> Aplicação de mineração de dados utilizando o algoritmo **ECLAT** sobre o **Groceries Dataset**, com sistema de recomendação de produtos baseado em regras de associação, containerizado com Docker.

---

## 📌 Sobre o Projeto

Este projeto foi desenvolvido como atividade da disciplina de **Mineração de Dados** do curso de Sistemas de Informação — UNITINS (2026).

O objetivo é descobrir padrões de coocorrência entre produtos comprados por clientes de supermercado e disponibilizar um sistema de recomendação via aplicação web: o usuário seleciona produtos no carrinho e o sistema sugere outros produtos frequentemente comprados em conjunto.

---

## 📦 Dataset

**Groceries Dataset** — publicado por Heeral Dedhia no Kaggle (GPL 2)

| Atributo | Descrição |
|---|---|
| `Member_number` | Identificador único do cliente |
| `Date` | Data da compra |
| `itemDescription` | Nome do produto comprado |

- 📊 **38.765** registros
- 👤 **3.898** clientes únicos (transações)
- 🏷️ **167** itens distintos
- 🛍️ Média de **8,92** itens por transação

🔗 https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset

---

## ⚙️ Algoritmo — ECLAT

O **ECLAT (Equivalence Class Clustering and bottom-up Lattice Traversal)** utiliza representação vertical dos dados (TID-lists), sendo mais eficiente que o Apriori por evitar múltiplas varreduras do banco de dados.

**Limiares utilizados:**
- Suporte mínimo: **2%**
- Confiança mínima: **20%**
- Lift mínimo: **> 1,0**

**Resultados:**
- 894 itemsets frequentes
- 1.397 regras de associação geradas

---

## 📐 Métricas

| Métrica | Descrição |
|---|---|
| **Suporte** | Proporção de transações com X e Y juntos |
| **Confiança** | P(Y\|X) — probabilidade de Y dado X |
| **Lift** | Força da associação relativa ao acaso (> 1 = positiva) |
| **Leverage** | Diferença entre frequência observada e esperada |
| **Conviction** | Medida de implicação direcional |

---

## 🗂️ Estrutura do Projeto

```
├── app/
│   ├── app.py                  # Backend Flask
│   ├── requirements.txt        # Dependências Python
│   ├── Dockerfile              # Container Docker
│   ├── rules.csv               # Regras mineradas (gerado pelo notebook)
│   ├── items_list.csv          # Lista de itens (gerado pelo notebook)
│   └── templates/
│       └── index.html          # Frontend da aplicação
├── notebook_final.ipynb        # Pipeline completo no Google Colab
└── README.md
```

---

## 🚀 Como Executar

### Opção 1 — Docker (recomendado)

```bash
# Baixar a imagem do Docker Hub
docker pull jucrsp/smartcart-eclat:latest

# Rodar o container
docker run -p 5000:5000 jucrsp/smartcart-eclat:latest
```

Acesse: http://localhost:5000

### Opção 2 — Local (Python)

```bash
cd app
pip install -r requirements.txt
python app.py
```

Acesse: http://localhost:5000

---

## 🔄 Reproduzindo o Pipeline

1. Baixe o dataset: https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset
2. Abra o `notebook_final.ipynb` no Google Colab
3. Faça upload do arquivo `Groceries_dataset.csv`
4. Execute todas as células
5. Baixe os arquivos `rules.csv` e `items_list.csv` gerados
6. Coloque-os na pasta `app/` e execute a aplicação

---

## 🐳 Docker Hub

A imagem está disponível publicamente:

🔗 https://hub.docker.com/r/jucrsp/smartcart-eclat

```bash
docker pull jucrsp/smartcart-eclat:latest
```

---

## 🧪 Exemplos de Recomendação

| Carrinho | Recomendações |
|---|---|
| `whole milk` + `yogurt` + `rolls/buns` | sausage, other vegetables, soda |
| `sausage` + `soda` + `whole milk` | rolls/buns, yogurt, other vegetables |
| `other vegetables` + `whole milk` | yogurt (conf. 37,5%, lift 1,33x), rolls/buns (conf. 42,9%) |

---

## 🛠️ Tecnologias

- Python 3.11
- Flask 3.0.3
- mlxtend 0.25.0
- pandas
- Docker

---

## 📚 Referências

- Dedhia, H. (2020). Groceries Dataset. Kaggle. https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset
- Zaki, M. J. (2000). Scalable algorithms for association mining. IEEE Transactions on Knowledge and Data Engineering.
- Raschka, S. mlxtend documentation. http://rasbt.github.io/mlxtend/
