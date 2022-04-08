import requests
from .models import Post, Comment
from celery import shared_task


@shared_task
def newsData1():

    urlNewStories = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"

    newStoryIds = requests.get(urlNewStories).json()

    for id in range(0, 5):
        url = f"https://hacker-news.firebaseio.com/v0/item/{newStoryIds[id]}.json?print=pretty"
        response = requests.get(url)
        data = response.json()

        if 'deleted' in data:
            continue
        if 'dead' in data:
            continue
        if not 'url' in data:
            continue

        if not Post.objects.filter(title = data['title']).exists():
            post = Post(
                by = data['by'],
                title = data['title'],
                url = data['url'],
                score = data['score'],
                type = data['type'],
                time = data['time']
            )
            post.save()
        else:
            post = Post.objects.get(title = data['title'])
            post.votes = data['score']
            post.comments = data['descendants']
            post.save()

        if 'kids' in data:
            for id in data['kids']:
                url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty"
                response = requests.get(url)
                c_data = response.json()
               
                if 'deleted' in c_data:
                    continue

                if 'dead' in c_data:
                    continue
              
                if Comment.objects.filter(text = c_data['text']).exists():
                    comment = Comment.objects.get(text = c_data['text'])
                else:
                    comment = Comment(
                        by = c_data['by'],
                        text = c_data['text'],
                        time = c_data['time'],
                        post = post,
                    )
                    comment.save()
                    

                if 'kids' in c_data:
                    walk(c_data, post, comment)

    return 'done'


def walk(dict, post, parent):
    for id in dict['kids']:
        url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty"
        response = requests.get(url)
        c2_data = response.json()

        if 'deleted' in c2_data:
            continue
        if 'dead' in c2_data:
            continue
        if not 'kids' in c2_data:
            if not Comment.objects.filter(text = c2_data['text']).exists():
                co2 = Comment(
                    by = c2_data['by'],
                    text = c2_data['text'],
                    time = c2_data['time'],
                    parent = parent, 
                    post = post,
                )
                co2.save()
        else:
            if not Comment.objects.filter(text = c2_data['text']).exists():
                co2 = Comment(
                    by = c2_data['by'],
                    text = c2_data['text'],
                    time = c2_data['time'],
                    parent = parent, 
                    post = post,
                )
                co2.save()
            
                if 'kids' in c2_data:
                    walk(c2_data, post, co2)






    
         
            

    
   
   
    