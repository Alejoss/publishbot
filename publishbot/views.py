import tweepy
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from publishbot.connection_settings import twitter_connect
from publishbot.models import Tweet


def home(request):
    if request.method == 'POST':
        image = request.FILES['image']
        text = request.POST['text']
        date = request.POST['date']
        time = request.POST['time']
        print(f"date {date}")
        print(f"time {time}")
        datetime_obj = datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M')

        new_object = Tweet(image=image, text=text, tweet_time=datetime_obj)
        new_object.save()

        return render(request, 'home.html')
    else:
        return render(request, 'home.html')


def send_tweet(request):
    image_path = None
    api = twitter_connect()
    if not api:
        pass
        # return http error

    try:
        # Upload the image
        media = api.media_upload(image_path)

        # Post a tweet with the image
        tweet = "Check out this image!"
        post_result = api.update_status(status=tweet, media_ids=[media.media_id])

        # Print the tweet URL
        print(
            f"Tweet posted successfully! URL: https://twitter.com/{post_result.user.screen_name}/status/{post_result.id}")
    except tweepy.TweepError as e:
        print(f"Error posting tweet: {e}")

    response_data = {'message': 'Created successfully'}
    return JsonResponse(response_data, status=201)
