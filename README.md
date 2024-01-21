# Instructiuni de rulare:

## Setup:
+ Pentru rularea aplicatiei este nevoie de instalarea unui IDE pentru rularea python, in acest proiect, noi am folosit `PyCharm`
+ Este nevoie de instalarea librariilor aferente, respectiv `whoosh`, `nltk` si `openai`.

## Construirea index-ului:
  Pentru construirea index-ului este necesara adaugarea folderului cu documentele **Wikipedia** fie in directorul in care este proiectul,
  sub numele implicit `"wiki-subset-20140602.tar"`, fie schimbarea valorii variabilei `documentsPath` in valoarea aferenta locatiei directorului cu documentele **Wikipedia**

  ## Cautarea in index:
  Pentru a cauta in index este necesara setarea variabilei `createIndex` la `false`, iar pentru folosirea sau nu a categoriei, schimbarea argumentului trimis functiei `search_index` in `True` pentru folosirea
  categoriei sau `False` pentru a nu folosi.

## Folosirea ChatGPT:

  Pentru a folosi ChatGPT in evaluarea intrebarilor, este necesar un `api_key` care se poate procura din contul personal `OpenAI` si decomentarea codului 111-114 inclusiv si linia 117 pentru afisare.
