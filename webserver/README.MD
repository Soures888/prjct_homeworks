# Nginx With the ability to purge images

## Installing:

`docker-compose up --build`

## Get the image/Purge it

http://localhost/duck.png - Got to this page in browser 2 times for caching the image

http://localhost/purge/duck.png - Purge Image

## Proofs

*Before Purging*:


![before purge](./proofs/before_purge.png)

*Purging Effect*:


![purge effect](./proofs/purge_effect.png)


*After Purge*:


![purge effect](./proofs/after_purge.png)
