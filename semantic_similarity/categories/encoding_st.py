from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

# TODO: Importar categorias da base de dados
# TODO: Conectar com o script de scraping, para processar antes
# de armazenar na base de dados
# Esse processamento sera feito assim:
# 1) Codificar cada nova categoria com as categorias ja armazenadas
# 2) Gerar scores de similaridades novos
# 3) Atualizar scores das empresas ja armazenadas, se a similaridade com a
#  outra empresa for maior que a similaridade minima que ela possui

categories_2 = []
with open('semantic_similarity/categories/categories.txt', 'r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        categories_2.append(line.strip().lower())

# Codifica as categorias pra gerar os embeddings correspondentes
embedding2 = model.encode(categories_2, convert_to_tensor=True)

# Armazena em um arquivo pickle
with open('semantic_similarity/categories/embeddings.pkl', "wb") as fOut:
    pickle.dump({'sentences': categories_2, 'embeddings': embedding2}, fOut, protocol=pickle.HIGHEST_PROTOCOL)
