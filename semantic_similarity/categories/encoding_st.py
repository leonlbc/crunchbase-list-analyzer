from sentence_transformers import SentenceTransformer
import pickle


####################
# Sqlalchemy
import os, sys, json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentdir)
from database.utils.hotTechCompanies.schema_create import Company, company_category, Category
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

with open("config.json", 'r') as f:
    config = json.load(f)

# Seleciona todas as categorias
engine = create_engine(config["db_path"], echo=False)
Session = sessionmaker(bind = engine)
session = Session()
category = session.query(Category.name).all()
categories = []
for i in category:
    categories.append(i[0].strip().lower())
####################

# TODO: Importar categorias da base de dados - FEITO
# TODO: Conectar com o script de scraping, para processar antes
# de armazenar na base de dados
# Esse processamento sera feito assim:
# 1) Codificar cada nova categoria com as categorias ja armazenadas
# 2) Gerar scores de similaridades novos
# 3) Atualizar scores das empresas ja armazenadas, se a similaridade com a
#  outra empresa for maior que a similaridade minima que ela possui

# Modelo selecionado com melhores resultados p/ similaridade semantica
model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
# Codifica as categorias pra gerar os embeddings correspondentes
embedding2 = model.encode(categories, convert_to_tensor=True)

# Armazena em um arquivo pickle
with open('semantic_similarity/categories/embeddings.pkl', "wb") as fOut:
    pickle.dump({'sentences': categories, 'embeddings': embedding2}, fOut, protocol=pickle.HIGHEST_PROTOCOL)
