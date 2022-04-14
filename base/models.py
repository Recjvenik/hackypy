from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey



class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    by = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256,)
    url = models.URLField(max_length=256,blank=True)
    description = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    type = models.CharField(max_length=256, null=True, blank=True, default='story')
    time = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    upVotes = models.ManyToManyField(User, related_name='story_upVotes')
    
    @property
    def getCommentCount(self):
        count = self.comment_set.all()
        return count.count()

    @property
    def getDateTime(self):
        if self.time is None:
            return self.created
        else:
            time = datetime.utcfromtimestamp(self.time)
            return time

    @property
    def getVoteCount(self):
        totalVotes = self.score + self.upVotes.count()
        return totalVotes


    def __str__(self):
        return self.title[0:50]

    class Meta:
        ordering = ['-time','-created']


class Comment(MPTTModel):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    by = models.CharField(max_length=256, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    identifier = models.IntegerField(default=0)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    comment_id = models.IntegerField(null=True, blank=True)
    time = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    

    @property
    def getDateTime(self):
        if self.time is None:
            return self.created
        else:
            time = datetime.utcfromtimestamp(self.time)
            return time
        

    # class MPTTModel:
    #     order_insertion_by = ['created']

    def __str__(self):
        return self.text[0:50]

    

