import requests
from django.test import TestCase

base_url = 'http://localhost:8000/'
# Create your tests here.

'''
1. To get user data - /api/users/?username=<username>
2. To get all posts of a user - /api/posts/?username=<username>
3. To view a post = /api/view_post/?post_id=<id>
'''
user_data = 'api/users/?username=Rambabu'
user_posts = 'api/posts/?username=Chinku'
view_post = 'api/view_post/?post_id=5'


def test(url):
    resp = requests.get(url)
    print(f"\n{'*'*65}")
    print(f'Test URL: {url}')
    print(f"{'*'*65}")
    if resp.status_code == 404:
        return 'No URL path defined'
    elif resp.status_code == 200:
        if resp.json() == []:
            return 'Not Found'
        else:
            return 'Success!'

print(test(base_url + user_data))
print(test(base_url + user_posts))
print(test(base_url + view_post))