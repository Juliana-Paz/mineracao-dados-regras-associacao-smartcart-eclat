from flask import Flask, request, jsonify, render_template
import pandas as pd
import ast

app = Flask(__name__)

# Carregar regras e itens
rules_df = pd.read_csv('rules.csv')
items_df = pd.read_csv('items_list.csv')

# Converter antecedentes e consequentes de string para lista
rules_df['antecedents'] = rules_df['antecedents'].apply(lambda x: set(x.split('|')))
rules_df['consequents'] = rules_df['consequents'].apply(lambda x: set(x.split('|')))

ALL_ITEMS = sorted(items_df['item'].tolist())


def recomendar(carrinho):
    """
    Dado um carrinho (lista de itens), retorna recomendações
    baseadas nas regras de associação mineradas pelo ECLAT.
    """
    carrinho_set = set(carrinho)
    recomendacoes = {}

    for _, row in rules_df.iterrows():
        # Verifica se o antecedente é subconjunto do carrinho
        if row['antecedents'].issubset(carrinho_set):
            for item in row['consequents']:
                # Não recomenda itens que já estão no carrinho
                if item not in carrinho_set:
                    if item not in recomendacoes:
                        recomendacoes[item] = {
                            'item': item,
                            'confianca': round(float(row['confidence']), 4),
                            'lift': round(float(row['lift']), 4),
                            'suporte': round(float(row['support']), 4)
                        }
                    else:
                        # Mantém a regra com maior lift
                        if row['lift'] > recomendacoes[item]['lift']:
                            recomendacoes[item] = {
                                'item': item,
                                'confianca': round(float(row['confidence']), 4),
                                'lift': round(float(row['lift']), 4),
                                'suporte': round(float(row['support']), 4)
                            }

    # Ordenar por lift decrescente e retornar top 8
    resultado = sorted(recomendacoes.values(), key=lambda x: x['lift'], reverse=True)
    return resultado[:8]


@app.route('/')
def index():
    return render_template('index.html', items=ALL_ITEMS)


@app.route('/recomendar', methods=['POST'])
def recomendar_endpoint():
    data = request.get_json()
    carrinho = data.get('carrinho', [])

    if not carrinho:
        return jsonify({'recomendacoes': [], 'mensagem': 'Carrinho vazio.'})

    recomendacoes = recomendar(carrinho)

    if not recomendacoes:
        return jsonify({
            'recomendacoes': [],
            'mensagem': 'Nenhuma recomendação encontrada para essa combinação de itens.'
        })

    return jsonify({
        'recomendacoes': recomendacoes,
        'mensagem': f'{len(recomendacoes)} recomendação(ões) encontrada(s).'
    })


@app.route('/itens', methods=['GET'])
def listar_itens():
    return jsonify({'itens': ALL_ITEMS})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
