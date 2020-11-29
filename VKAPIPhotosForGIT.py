from urllib.parse import urljoin
import requests
import tqdm

class VK_user:
    API_BASE_URL = 'https://api.vk.com/method/'
    VK_TOKEN = 'INSERT  VK_TOKEN'
    V = '5.21'

    def get_max_photo(self, user_id):
        photos_list = list()
        get_photo_url = urljoin(self.API_BASE_URL, 'photos.get')
        get_likes_url = urljoin(self.API_BASE_URL, 'likes.getList')
        response = requests.get(get_photo_url, params={'access_token': self.VK_TOKEN, 'v': self.V, 'user_id': user_id, 'album_id': 'profile', 'photo_sizes': 1})
        photos = (response.json())['response']['items']

        for photo in photos:
            a = dict()
            a['type'] = 'a'
            item_id = photo['id']
            for params in (photo['sizes']):
                if params['type'] > a['type']:
                    a = params
                    a['item_id'] = str(item_id)
            photos_list.append(a)
        def sortbysize(inputdata):
            return str(inputdata['type'])

        photos_list.sort(key=sortbysize)

        for photos in photos_list:
            response1 = requests.get(get_likes_url, params={'access_token': self.VK_TOKEN, 'v': self.V, 'type': 'photo', 'owner_id': user_id, 'item_id': photos['item_id']})
            photos['file_name'] = (response1.json()['response']['count'])
        return photos_list

    def upload(self, YA_token, user_id: str, count: 5):
        HEADERS = {'Authorization': f'OAuth {YA_token}'}
        all_photos = self.get_max_photo(user_id)
        all_photos = all_photos[0:count]
        rep_new_folder = requests.get('https://cloud-api.yandex.net/v1/disk/resources?path=%2Fnew_folder', headers=HEADERS)
        put_path = rep_new_folder.json()['_embedded']['path']

        for photos in tqdm.tqdm(all_photos):
            file_name = photos['file_name']
            reponse = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', params={'path': f'{put_path}/{file_name}', 'overwrite': True}, headers=HEADERS)
            url = reponse.json()['href']
            file_path = str(photos['src'])
            img = requests.get(file_path).content
            requests.put(url, params={'path': put_path + '/'}, headers=HEADERS, files={"file": img})
        return

user1 = VK_user()
#user1.get_max_photo('552934290')
user1.upload('INSERT YANDEX_TOKEN', '552934290', 3)


