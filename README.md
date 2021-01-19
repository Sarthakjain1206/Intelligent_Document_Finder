<p align="center">
  <img src="https://repository-images.githubusercontent.com/267515540/1d2d9000-a35e-11ea-8ee0-60ba580c3445" width=600 height=300>
</p>

<h1 align="center">Intelligent Document Finder 2.0</h1>

<br><br>
A tool which can find your any document using **semantic search**.
<br><br>
**This is an Improvised Version of Intelligent-Document-Finder**
<br>
List of New Features--
1. Implemented Document Similarity Script, which allows you to see related or most similar documents.
2. Revamped website UI.
3. Reduces time complexities of search functions.
# What is Intelligent Document Finder <img src="https://img.icons8.com/color/48/000000/learning.png"/> ?
How easy do you find it to remember the exact location of a document that you created last year? Not very easy, right? Big Organizations/people deal with hundreds of documents daily and forget about them, most of the time.
<br>
But what if we want that old documentation again for some work, but unfortunately you do not remember the name or the actual content of that document to retrieve it from the large storage of your computer.
<br>
In such cases, use of a __Intelligent document finder__ can really make a huge difference. As, it can Search for the document(```semantically```) of your need based on a query input. This will not only help in faster access to the document, but will also help in grouping similar documents together and in analysing them.
<br>

<a href="https://youtu.be/fn4A2P1qpWM">Watch Project Demo: </a>

[![Watch Demo](https://i9.ytimg.com/vi_webp/fn4A2P1qpWM/sddefault.webp?time=1611081000000&sqp=CKjKnIAG&rs=AOn4CLB-lc28zlEQXFLoJvb42qjBGUoWnQ)](https://youtu.be/fn4A2P1qpWM)


# Note <img src="https://img.icons8.com/ios-filled/30/000000/note.png"/> 
Currently this repositry is using predefined database of news articles gathered by web scraping. Due to the github restrictions on uploading the large files, we cannot upload it here. 
<br><br>
Soon, we will add the support of the dynamic databases, so that you can use this tool for your own databases to build your own custom search engine.
<br>
# Technologies Used <img src="https://img.icons8.com/nolan/48/computer.png"/>
**```Python3.6```**
__```JavaScript```__
__```jQuery```__
__```HTML & CSS```__
<br>
<h4>Database Used:</h4>
 SQlite
<br>
<h4>For implementing searching:</h4>
 Various NLP(Natural Language Processing) techniques is used.
<br>
<h4>For website:</h4>

- Python-based Web framework : Flask
- JavaScript
- jQuery

# Program Flow <img src="https://img.icons8.com/fluent/40/000000/iphone-spinner.png"/>
<img src="https://github.com/Sarthakjain1206/Intelligent-Document-Finder/blob/master/Flowchart.png" alt="Trulli" width="700" height="500">

# Compatibility
- Backend (AI part) is compatible on any machine that has python and required dependencies installed.
- Recommended browsers: Mozilla Firefox and Google Chrome.

# How to Install and Use <img src="https://img.icons8.com/color/40/000000/settings.png"/> ?

```> mkdir IntelligentDocumentFinder```
<br>
<br>
```> cd IntelligentDocumentFinder```
<br>
<br>
```> git clone https://github.com/Sarthakjain1206/Intelligent_Document_Finder_2.0.git```
<br>

Install Vitual Environment if not installed
<br>
- On Linux/MacOs
```> python3 -m pip install --user virtualenv```
- On windows
```> py -m pip install --user virtualenv```

Create Virtual Environment
- On macOS and Linux:
```> python3 -m venv env```
- On Windows:
```> py -m venv env```

Activate Environment:
- On macOS and Linux:
```> source env/bin/activate```
- On Windows:
```> .\env\Scripts\activate```

```> pip install -r requirements.txt```

__Download Glove Word Embeddings__ from this [link](https://www.kaggle.com/terenceliu4444/glove6b100dtxt), decompress it and copy the ```glove.6B.100d``` file in ```DataBase``` folder

then, 
run initial_file.py through this command
```> python initial_file.py```

Now you are good to go.. Just type this command everytime you want to access it, and open the website in chrome/firefox
<br>
```> python src/app.py```
<br><br>

<h1>Developers <img src="https://img.icons8.com/ultraviolet/24/000000/human-head.png"/></h1>

You can get in touch with us on linkedln profiles

<br>

__Sarthak Jain__ ```Machine Learning``` ```NLP``` ```Web Crawling```

[![Foo](https://img.icons8.com/cute-clipart/48/000000/linkedin.png)](https://www.linkedin.com/in/sarthak-jain-58b466170/)

You can also follow me on Github to stay updated about my latest projects
[![Foo](https://img.icons8.com/material-sharp/24/000000/github.png)](https://github.com/Sarthakjain1206)

__Rishabh Mishra__  ```Full Stack Web Developer```

[![Foo](https://img.icons8.com/cute-clipart/48/000000/linkedin.png)](https://www.linkedin.com/in/rishabh-mishra-3a6985167)

You can also follow me on Github to stay updated about my latest projects
[![Foo](https://img.icons8.com/material-sharp/24/000000/github.png)](https://github.com/rishabhm74)


If you liked this repository, then do support it by giving it a __star__
<img src="https://img.icons8.com/emoji/24/000000/star-emoji.png"/>

<h1>Contributions <img src="https://img.icons8.com/office/24/000000/community-grants.png"/> </h1>
 If you find any bug or have any suggestions to improve this project, then feel free to generate a pull request.
<br>

There are a lot of features that can be added to this tool. 

1. __Query Segmentation__
2. __Query Expansion__ (Mainly - __Pseudo Relevance Feedback technique__)
3. __Improvising Spell Checker__
4. __Collocations__ For example- Currently this project consider "New York" as ["New","York"] i.e two different words but it should be consider as a single entity like ["New_York"], this can definitely make a big difference in search results.
5. __Query Logs (Game changing technique for search engines)__
6. __Search result's segmentation__ [like- Luecene]

If you have any experience in implementing any of these features then, do __contribue__. 

# References
1. Awsome article of BM25 ranking algorithm on wikipedia -
[Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25)

2. Read this article on [Topic Modeling](https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24)

3. Completely followed this beautiful [article](https://medium.com/@acrosson/extract-subject-matter-of-documents-using-nlp-e284c1c61824) on SVOs tagging for generating tags for this project.

4. Used the BM25 ranking fuction implementation from this great [repositry](https://github.com/dorianbrown/rank_bm25) on github by ```dorianbrown```.
