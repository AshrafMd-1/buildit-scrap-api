import json
from timeit import default_timer as timer

import requests

from buildit_api.mod.answer import lang_code
from buildit_api.mod.update import update_session


def submit_code(db, user_id, det):
    cookies = update_session(db, user_id)
    validate_url = 'http://13.234.234.30:5000/validateSubmission'
    validate_headers = {
        'authorization': cookies['token'],
    }
    validate_payload = {
        "source_code": det.code,
        "language_id": lang_code(det.compiler),
        "stdin": "",
        "contestId": "",
        "courseId": det.course,
        "user": cookies['user'],
        "questionId": det.question, }
    start = timer()
    res = requests.post(validate_url, data=validate_payload, headers=validate_headers, cookies=cookies)
    result = json.loads(res.content)
    end = timer()
    try:
        return {
            "result": result["result"],
            "time taken": end - start,
            "score": result["score"],

        }
    except:
        return {
            "result": result["message"],
            "time taken": end - start,
            "score": result["score"],
        }
