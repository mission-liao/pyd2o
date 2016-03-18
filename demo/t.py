import six
import model
from model import User

if __name__ == '__main__':
    u1 = model.User(dict(
        email='missionaryliao@gmail.com',
        preference=dict(
            color='red',
            size='xxxxxl',
        )
    ))
    print u1
    print u1.email
    print u1.preference.color
    print u1.preference.size

    u2 = model.User(dict(
        email='kkk@gmail.com',
        pps=[
            dict(color='red', size='m'),
            dict(color='yellow', size='s'),
        ]
    ))
    for v in u2.pps:
        print v.color, v.size

    u3 = model.User(dict(
        email='xxx@gmail.com',
        xxx=dict(
            a=[
                dict(color='red1', size='m1'),
                dict(color='yellow1', size='s1'),
            ],
            b=[
                dict(color='red2', size='m2'),
                dict(color='yellow2', size='s2'),
            ],
        )
    ))
    for k in u3.xxx:
        print k
        for v in u3.xxx[k]:
            print v.color, v.size


