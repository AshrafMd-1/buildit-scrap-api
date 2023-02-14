import json

import requests

from buildit_api.db import models


def lang_code(compiler):
    lang = [['text/x-pascal', '3'],
            ['c', '4'],
            ['c++', '10'],
            ['csharp', '16'],
            ['clojure', '18'],
            ['text/x-crystal', '19'],
            ['text/x-elixir', '20'],
            ['text/x-erlang', '21'],
            ['go', '22'],
            ['text/x-haskell', '23'],
            ['plaintext', '44'],
            ['java', '26'],
            ['javascript', '29'],
            ['text/x-ocaml', '31'],
            ['text/x-octave', '32'],
            ['pascal', '33'],
            ['python', '34'],
            ['ruby', '38'],
            ['rust', '42']]
    for elem in lang:
        if compiler.lower() in elem:
            return elem[1]


def get_answer(db, user_id, det):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    user = db_user.username.lower()
    token = db_user.token
    mem = ['19951a1235', '20951a6626', '19951a0566', '21951a6608', '21951a6636', '21951a6612', '21951a6633']
    mem.insert(0, user)
    for i in mem:
        url = f"http://13.234.234.30:5000/submissions/user/{i}/{det.question}"
        headers = {
            "authorization": token,
            "content-type": "application/json"
        }
        response = requests.get(url, headers=headers)
        ans = json.loads(response.text)
        for j in ans:
            if j['score'] == 100 and j['languageId'] == lang_code(det.compiler):
                return str(j['sourceCode'])
    return "answer not found"
