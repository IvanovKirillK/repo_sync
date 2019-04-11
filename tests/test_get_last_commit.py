from tasks import get_last_commit
import logging
import pytest
from flask import Flask
import json
from multiprocessing import Process

logger = logging.getLogger('testlog')


@pytest.fixture()
def main_branch():
    response = '{\
    "values": [\
        {\
            "id": "a228ada353f3778710f4a76e043aaa5d963f4086",\
            "displayId": "a228ada353f",\
            "author": {\
                "name": "ivanov_ma",\
                "emailAddress": "ivanov_ma@rtsoft.msk.ru",\
                "id": 159,\
                "displayName": "Иванов Михаил Александрович",\
                "active": true,\
                "slug": "ivanov_ma",\
                "type": "NORMAL",\
                "links": {\
                    "self": [\
                        {\
                            "href": "http://192.168.10.208:7990/users/ivanov_ma"\
                        }\
                    ]\
                }\
            },\
            "authorTimestamp": 1554828372000,\
            "committer": {\
                "name": "ivanov_ma",\
                "emailAddress": "ivanov_ma@rtsoft.msk.ru",\
                "id": 159,\
                "displayName": "Иванов Михаил Александрович",\
                "active": true,\
                "slug": "ivanov_ma",\
                "type": "NORMAL",\
                "links": {\
                    "self": [\
                        {\
                            "href": "http://192.168.10.208:7990/users/ivanov_ma"\
                        }\
                    ]\
                }\
            },\
            "committerTimestamp": 1554828372000,\
            "message": "Merge pull request #188 in PFP/asm from hotfix/ASM-195-migrations to develop\n\n* commit :\n  hotfix/ASM-195 delete local import and move it upward\n  Moving includes up\n  Moving signal function to signals.py\n  Move update_breakers_history on post_migrate signal",\
            "parents": [\
                {\
                    "id": "637e9c7b4e601a3359475ccdb97783784932600a",\
                    "displayId": "637e9c7b4e6"\
                },\
                {\
                    "id": "90849ac8fa07b28125464b815a31c21ea63d6fc7",\
                    "displayId": "90849ac8fa0"\
                }\
            ],\
            "properties": {\
                "jira-key": [\
                    "ASM-195"\
                ]\
            }\
        }\
    ],\
    "size": 1,\
    "isLastPage": false,\
    "start": 0,\
    "limit": 1,\
    "nextPageStart": 1\
    }'

    app = Flask(__name__)

    @app.route('/rest/api/latest/projects/PFP/repos/asm/commits?until=develop&limit=0&start=0')
    def hello():
        return response

    if __name__ == "__main__":
        app.run()
    # server = Process(target=app.run)
    # server.start()

    yield

    # server.terminate()
    # server.join()


def test_get_last_commit_failed_case(main_branch):
    branch = json.dumps({'vcs': 'bitbucket', 'url': 'http://127.0.0.1:5000/rest/api/latest/projects/PFP/repos/asm/commits', 'params': {'until': 'develop', 'limit': 0, 'start': 0}, 'auth': {'type': 'basic', 'login': 'ivanov_kk', 'password': 'ckfhjlfrn'}})
    print(branch)
    assert get_last_commit(branch, logger) is False
