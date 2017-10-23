from django.shortcuts import render
from django.http import HttpResponse

import time
import json

from elasticsearch.elasticsearch_wrapper import ElasticsearchWrapper
from twitter.tweet_streamer import TweetStreamer
from twitter.tweet_handler import TweetHandler
import threading

es = ElasticsearchWrapper()

def start_streaming():
    es = ElasticsearchWrapper()
    streamer = TweetStreamer()
    streamer.set_handler(TweetHandler(es, collect_freq=5))
    streamer.start_stream()
    
t = threading.Thread(target=start_streaming)
t.setDaemon(True)
t.start()


def index(request):

    return render(request, 'googlemap/index.html')

def first_fetch(request):

    print ('ajax request: first_fetch')
    response = es.fetch_latest(1000)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')


def update_tweets(request):

    print ('ajax request: update_tweets')
    response = es.fetch_latest(10)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')

def stop_tweets(request):

    print ('ajax request: stop_tweets')
    return HttpResponse()

def search(request):

    print ('ajax request: search request')
    keyword = request.POST['keyword']
    response = es.search(keyword)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')

def geosearch(request):

    print ('ajax request: geosearch')
    location = request.POST.get('location')
    distance = request.POST.get('distance')
    print ('location: %s, radius: %s' % (location, distance))

    response = es.geosearch(location, distance, 2000)# search at most 2000 tweets
    print ('geosearch response: %s' % response)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')



