from sentence_transformers import util
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from database.utils.hotTechCompanies.schema_create import Company, company_category, Category

#Carrega embeddings calculados no arquivo enconding_st
with open('semantic_similarity/embeddings.pkl', "rb") as fIn:
    stored_data = pickle.load(fIn)
    stored_sentences = stored_data['sentences']
    stored_embeddings = stored_data['embeddings']
# Computa o score de similaridade
cosine_scores = util.pytorch_cos_sim(stored_embeddings, stored_embeddings)

# TODO: Otimizar *muito*
# Gambiarra pq falhou o join do Sqlalchemy
# Monta dicionario das companies e suas categorias ('Join manual')
engine = create_engine('sqlite:///db.sqlite3', echo=False)
Session = sessionmaker(bind = engine)
session = Session()
comp_cat = session.query(company_category)
category = session.query(Category)
company = session.query(Company)
category_group_by_comp = {}
for cc in comp_cat:
    categ = None
    comp = None
    for ctg in category:
        if (ctg.id == cc.category_id):
            categ = ctg
    for cmp in company:
        if (cmp.uuid == cc.company_uuid):
            comp = cmp
    if category_group_by_comp.get(comp) == None:
        category_group_by_comp[comp] = [categ]
    else:
        category_group_by_comp[comp].append(categ)

# TODO: Otimizar + Experimentar outras metricas de relacionamento das categorias
# Ja tentei: media, media das maiores sims, score maximo gerals
def company_sim_score(cat_sim_matrix):
    len_cat = len(cat_sim_matrix)
    len_cat_2 = len(cat_sim_matrix[0])
    score = 0
    for i in cat_sim_matrix:
        for j in i:
            score = max(score, j)
    return score

# Calcula, para cada categoria da empresa 1..n
# um novo score relacionado aos scores de similaridade entre cada categoria
# de cada uma das outras empresas
comp_group_similar = {}
for comp in category_group_by_comp:
        comp_group_similar[comp] = []
        for comp_2 in category_group_by_comp:
            if comp_2 != comp:
                # Busca a matriz de score de similaridade entre as categorias das duas empresas
                cat_sim_matrix = []
                for idx1, cat in enumerate(category_group_by_comp[comp]):
                    cat_matrix_parcial = []
                    for idx2, cat_2 in enumerate(category_group_by_comp[comp_2]):
                        idx_cat = stored_sentences.index(cat.name.lower())
                        idx_cat2 = stored_sentences.index(cat_2.name.lower())
                        cat_matrix_parcial.append(cosine_scores[idx_cat][idx_cat2].item())
                    cat_sim_matrix.append(cat_matrix_parcial)
                # Calcula o score de similaridade entre as empresas
                score = company_sim_score(cat_sim_matrix)
                comp_group_similar[comp].append([comp_2, score])

#TODO: Otimizar
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
    comp_by_highest_score = list(filter(lambda x: x[1] > LIMITE_MAIOR, comp_by_highest_score))
    if (len(comp_by_highest_score) < 5):
        comp_by_highest_score = list(filter(lambda x: x[1] > LIMITE_MENOR, comp_categs))
        comp_by_highest_score = comp_categs[:5]
    comp_group_similar[i] = comp_by_highest_score


for i in comp_group_similar:
    print(str(i) + ": " + str(comp_group_similar[i]))
    print()
