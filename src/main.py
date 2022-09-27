import shutil
from preprocessor import preprocess_query
from indexing_whoosh import ranking_merged
import os
from webcrawler import WebCrawler
from extractor import extractor
from indexing_whoosh import create_index

FILES_PATH = '../Docs/'

#ripulisce cartella dei documenti
def clean_docs():
    for dir in os.listdir(FILES_PATH):
        shutil.rmtree(os.path.join(FILES_PATH,dir), ignore_errors=True)

#inizia il crawling popolando la cartella dei documenti
def start_crawling(limit=20):
    clean_docs()
    wc = WebCrawler(limit=limit)

    # Si può passare un url iniziale alle funzioni di run
    wc.start_crawling("https://www.meetup.com/find/?source=EVENTS")
    wc.start_crawling("https://www.eventbrite.com/d/ny--new-york/events/")
    #wc.remove_double_files()

    create_index()

#stampa i risultati di una query sottoposta al motore
def submit_query(query):
    results = ranking_merged(query)
    if results == []:
        print("La query non ha dato risultati utili, provare a riformulare \n")
        return
    count = 0
    print("Documents found: "+ str(len(results)))
    for x in results:
        print(f"\n\n\t Result {count+1}: \n")
        print(extractor(x['file']))
        print(f" \n score:{x['score']}")
        count += 1
        if count == 10:
            if (input("show more results? (y/n) \n") == "n"):
                return
            count = 0

def benchmark():
    NQueries_benchmark = 10
    precision_at_10thres = [1,0.948,1,0.975,0.218,1,1,1,1,1]
    MAP = sum(precision_at_10thres)/NQueries_benchmark
    natural_queries = []
    queries = []
    results = []
    with open('query_natural_leng.txt','r') as f:
        for line in f:
            natural_queries.append(line[:-1])
    with open('query_benchmark.txt','r') as f:
        for line in f:
            queries.append(line[:-1])
    for query in queries:
        results.append(ranking_merged(query)[:11])
    for result in results:
        print(f'{natural_queries.pop(0)}')
        print(f'Eseguendo query: {queries.pop(0)}')
        print('numero di risultati ottenuto: ' + str(len(result)))
        print(f'Average Precision per primi 10 risultati: {precision_at_10thres.pop(0)} \n\n')
    print(f'\nMean Average Precision: {MAP} \n')


def menu():
    c = input("""
    1) WebCrawling (Scarica i dati dalle due sorgenti)
    2) Esegui una query
    3) Cronologia delle ultime query
    4) Benchmark
    5) Exit
    """)
    try:

        x = int(c)
        if x==1:
            limit = input("Insert the limit of the search (integer number):")
            start_crawling(limit=int(limit))
        elif x==2:
            submit_query(input("insert query \n"))
        elif x==3:
            pass
        elif x==4:
            input('Prima di procedere con il benchmark, cancellare la cartella Docs e rinominare Docs_Benchmark in Docs.\nEnter per continure\n')
            benchmark()
        elif x==5:
            exit()

    except ValueError:
        print("Insert only valid numbers in the menu please.")
        menu()

#Main
while True:
    menu()








