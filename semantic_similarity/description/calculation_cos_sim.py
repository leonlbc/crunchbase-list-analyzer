from sentence_transformers import util
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parent_parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parent_parentdir)
from database.utils.hotTechCompanies.schema_create import Company, company_category, Category

#Carrega embeddings calculados no arquivo enconding_st
with open('semantic_similarity/description/embeddings.pkl', "rb") as fIn:
    stored_data = pickle.load(fIn)
    stored_sentences = stored_data['sentences']
    stored_embeddings = stored_data['embeddings']
# Computa o score de similaridade
cosine_scores = util.pytorch_cos_sim(stored_embeddings, stored_embeddings)

engine = create_engine('sqlite:///db.sqlite3', echo=False)
Session = sessionmaker(bind = engine)
session = Session()
company = session.query(Company).all()

def company_sim_score(cat_sim_matrix):
    score = 0
    for i in cat_sim_matrix:
        for j in i:
            score = max(score, j)
    return score

comp_group_similar = {}
for comp in company:
        comp_group_similar[comp] = []
        for comp_2 in company:
            if comp_2 != comp:
                idx = stored_sentences.index(comp.short_description.lower().strip())
                idx_2 = stored_sentences.index(comp_2.short_description.lower().strip())
                score = cosine_scores[idx][idx_2].item()
                comp_group_similar[comp].append([comp_2, score])

QTD_SIMILAR_COMPANIES = 10
LIMITE_MENOR = 0.3
LIMITE_MAIOR = 0.4
for i in comp_group_similar:
    # Ordena do maior ao menor os scores de similaridade
    comp_categs = list(reversed(sorted(comp_group_similar[i], key=lambda x: x[1])))
    # Pega uma certa quantidade de empresas similares 
    comp_by_highest_score = comp_categs[:QTD_SIMILAR_COMPANIES]
    # Separa apenas scores maiores que 0.4, a nao ser que a empresa tenha poucos (< 5) similares
    # e nesse caso seleciona os 5 maiores entre 0.3 e 0.4
    # comp_by_highest_score = list(filter(lambda x: x[1] > LIMITE_MAIOR, comp_by_highest_score))
    # if (len(comp_by_highest_score) < 5):
    #     comp_by_highest_score = list(filter(lambda x: x[1] > LIMITE_MENOR, comp_categs))
    #     comp_by_highest_score = comp_categs[:5]
    comp_group_similar[i] = comp_by_highest_score

for i in comp_group_similar:
    print(str(i) + ": " + str(comp_group_similar[i]))
    print()
