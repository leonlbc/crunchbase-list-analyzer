from sentence_transformers import util
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parent_parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parent_parentdir)
from database.utils.hotTechCompanies.schema_create import Company, company_category, Category
from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

#Testar removendo nome e removendo stop-words
#continunar testando
#cruzar score de categoria + desc

desc = ["Inclined is a financial technology company that helps policyholders enhance the value of their life insurance policies.",
"HealthAssure is a healthtech startup that aggregates primary healthcare services and OPD insurance for corporates and individuals.",
"Farther Finance is a developer of an investment advisory platform used to provide modern technology with trusted advice."]

desc = ["financial technology company helps policyholders enhance value their life insurance policies.",
"healthtech startup aggregates primary healthcare services OPD insurance corporates individuals.",
"developer investment advisory platform used to provide modern technology with trusted advice."]

# desc = ["Astra is an automation platform for the movement of money.",
#         "TrovaTrip is an audience monetization platform via authentic experiences for topic influencers."]
# desc = ["automation platform movement money.",
#         "audience monetization platform via authentic experiences topic influencers."]

# Codifica as categorias pra gerar os embeddings correspondentes
embedding2 = model.encode(desc, convert_to_tensor=True)

stored_sentences = desc
stored_embeddings = embedding2
cosine_scores = util.pytorch_cos_sim(stored_embeddings, stored_embeddings)

for i in stored_sentences:
    for j in stored_sentences:
        idx_i = stored_sentences.index(i)
        idx_j = stored_sentences.index(j)
        sc = cosine_scores[idx_i][idx_j].item()
        print( str(i) + " + " + str(j) + ": " + str(sc))
