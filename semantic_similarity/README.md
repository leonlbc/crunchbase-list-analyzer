# Calculo da semelhanca entre as empresas por meio da similaridade semantica de suas categorias utilizando o SentenceTransformer (Sentence-Bert)

Irei calcular e armazenar os scores de similaridade entre as empresas similares utilizando a relacao entre os scores de 
similaridade das categorias delas a fim de utilizarmos essas informacoes no WebApp Crunchbase List 
Analyzer.

Utilizarei o transformer SentenceTransformer, com o modelo multi-qa-mpnet-base-dot-v1, ajustado para 
pesquisas semanticas (modelo pre-treinado mais performatico para esse objetivo, feito pelo time da 
SBert - 'https://www.sbert.net/docs/pretrained_models.html'), para gerar os embeddings das 
categorias. A partir desses dados, aplicarei uma funcao de similaridade por cosseno, que computa um 
score de 0-1, sendo 1 total relacao e 0 nehuma relacao entre as categorias. A partir desse score,
cruzarei todas as categorias de uma empresa com todas de cada uma das outras empresas,
a fim de computar um novo score, agora nao mais entre as categorias, mas sim entre as empresas. Com base nesse 
calculo, ligarei as 'k' empresas mais similares e armazenarei essa ligação com uma nova join table denominada "Similarity".

# Resultados

Utilizar as categorias das empresas para estabelecer o quao similares elas são não gerou resultados 
tão satisfatórios em alguns casos. Isso aconteceu por alguns motivos, sendo os principais: 
categorias mal selecionadas para uma certa empresa (não representam bem a atividade fim da empresa);
empresas com muitas categorias, cuja atividade fim não se destaca. Nesse último caso, as empresas obtiveram 
um score maior com uma maior quantidade de empresas, sem que a atividade fim tivesse relação.

Tentarei utilizar os embeddings das descricoes das empresas para melhorar esse score.

# Resultados - 2

Os embeddings das descricoes precisaram de tratamento: remoção de nome da empresa do texto, remoção de 
stop-words. Enquanto eu testava novos scores de similaridades, voltei para as categorias e testei mais 
maneiras de calcular os scores baseados nelas. Apenas mantive as empresas com relação alta ( > 0.5), e atribuí um 
peso maior para as empresas com relação de similaridade > 0.8 (extremamente similar). Os resultados foram mais 
satisfatórios, e por enquanto bastaram para o protótipo.
