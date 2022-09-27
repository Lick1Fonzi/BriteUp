import os, os.path
from whoosh import index
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh import scoring
from extractor import extractor
from preprocessor import preprocess

INDEXPATH = os.path.abspath(os.path.pardir) + os.path.sep + "indexdir"
DOCPATH = os.path.abspath(os.path.pardir) + os.path.sep +"Docs"  
SCHEMA = Schema(event=TEXT(stored=True),content=TEXT(stored=True),url=TEXT(stored=True),path=TEXT(stored=True))

#funzione che legge un documento e lo aggiunge all'indice secondo lo schema
def add_doc(writer, path):
  doc = extractor(path)
  if("meetup" in doc.url):
    doc.url = "meetup"
  else:
    doc.url = "eventbrite"
  writer.add_document(event=preprocess(doc.event_name),content=preprocess(doc.content),url=doc.url,path=doc.path)

#creo directory degli indici, per ogni cartella in Docs creo un indice
def create_index():
  if not os.path.exists(INDEXPATH):
      os.mkdir(INDEXPATH)
  for dir in os.listdir(DOCPATH):
    ix = index.create_in(INDEXPATH, SCHEMA,indexname=dir)
    writer = ix.writer()
    for doc in os.listdir(os.path.join(DOCPATH,dir)):
      add_doc(writer,os.path.join(DOCPATH,dir,doc))
    writer.commit()

def search_index(indexname,keyword):
  ix = index.open_dir(INDEXPATH,indexname=indexname)
  q = MultifieldParser(['event', 'content','url'], schema=ix.schema)
  #keyquery = preprocess(keyword.lower())
  #query = q.parse(keyquery)
  query = q.parse(keyword)
  results = []
  with ix.searcher(weighting=scoring.BM25F(B=0.75, title_B=1.0, body_B=0.5, K1=2)) as searcher:   #scoring.TF_IDF()
        for r in searcher.search(query, limit=30):
          results.append({"file": r["path"], 'score': r.score})
  return results

def ranking_merged(query):
  results = []
  results.extend(search_index("www.meetup.com",query))
  results.extend(search_index("www.eventbrite.com",query))
  results = sorted(results,key = lambda x: x['score'] ,reverse=True)
  return results

    

