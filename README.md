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

Recommend: Filmes recomendados de acordo com filtro colaborativo. Assim, caso o usuário avaliou positivamente os filmes A e B e outro usuário avaliou positivamente os filmes A, B e C, provavelmente o primeiro usuário irá gostar do filme C, assim C é recomendado para ele.
