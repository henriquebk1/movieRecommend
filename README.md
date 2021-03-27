# Recomendação de Filmes

##### Requisitos

```
python 3.8

pip3

Django

pandas

numpy

scipy
```

##### Como rodar

```
python manage.py runserver
```

## Recomendações

Home: Filmes melhores avaliados, compensado de acordo com o número de avaliações. Assim um filme com 5 notas 9,1 não vai parecer mais recomendado do que um com 1000 notas e média 9. Baseado em: https://www.datacamp.com/community/tutorials/recommender-systems-python

Recommend (Collaborative): Filmes recomendados de acordo com filtro colaborativo. Assim, caso o usuário avaliou positivamente os filmes A e B e outro usuário avaliou positivamente os filmes A, B e C, provavelmente o primeiro usuário irá gostar do filme C, assim C é recomendado para ele. 
Ele busca as avaliações de filmes feitas pelo usuário logado, comparando com as avaliações feitas por outras usuários, de modo a encontrar usuários parecidos (isso é feito através de uma correlação). Com base nos usuários similares, é recomendado os filmes melhor avaliados por esses usuários similares, com um limite de até 50 filmes recomendados. Filmes já assistidos não são recomendados.

Recommend (Genre): Filmes melhores avaliados dos gêneros que o usuário logado avaliou positivamente. Exemplo: Se o usuário avaliou positivamente somente filmes de comédia, serão recomendados somente os melhores filmes do gênero comédia, com base nas avalições de todos usuários da plataforma (sendo limitado a 50 filmes recomendados). Isso é feito ao obter os gêneros dos filmes avaliados positivamente pelo usuário (são considerados os filmes cuja avaliação for superior à média das avaliações do usuário, sendo assim, se um usuário só deu notas 9 e 8, os filmes com notas 9 serão considerados como bem avaliados, se só deu notas 10 e 5, os filmes com notas 10 serão considerados como bem avaliados).

*Se o usuário não avaliou nenhum filme, não são geradas recomendações de forma colaborativa nem com base no conteúdo de suas avaliações (por gênero), sendo informado para o usuário que ele deve avaliar ao menos um filme primeiramente.
