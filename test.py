import json

import tinder_api.session
import tinder_api.user as u

try:
    s = tinder_api.session.Session()  # inits the session
    print(s.get_id())
except:
    raise RuntimeError('Can\'t init session') from None


def test():
    try:
        profile = s.get_profile()
        save('profile.json', profile)

        likes = s.get_all_likes()
        save('likes.json', likes)

        matches = s.list_matches()
        save('matches.json', matches)

        matched_user = u.UserController(matches[0].get('_id')).get_data()
        save('matched_user.json', matched_user)

        print('PASS')
    except:
        print('FAIL')
        raise


def save(filename, data):
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data))
        f.close()


if __name__ == '__main__':
    test()
