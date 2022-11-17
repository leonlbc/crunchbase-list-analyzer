from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

# TODO: Parametrizar categorias
# TODO: Conectar com o script de scraping, para processar antes
# de armazenar na base de dados
# Esse processamento sera feito assim:
# 1) Codificar cada nova categoria com as categorias ja armazenadas
# 2) Gerar scores de similaridades novos
# 3) Atualizar scores das empresas ja armazenadas, se a similaridade com a
#  outra empresa for maior que a similaridade minima que ela possui

desc = []
with open('semantic_similarity/description/desc.txt', 'r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        desc.append(line.strip().lower())

# Codifica as categorias pra gerar os embeddings correspondentes
embedding2 = model.encode(desc, convert_to_tensor=True)

# Armazena em um arquivo pickle
with open('semantic_similarity/description/embeddings.pkl', "wb") as fOut:
    pickle.dump({'sentences': desc, 'embeddings': embedding2}, fOut, protocol=pickle.HIGHEST_PROTOCOL)
