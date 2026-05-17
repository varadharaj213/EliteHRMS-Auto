from flask import Flask
import requests
import base64
from datetime import datetime

app = Flask(__name__)

USERNAME="YOUR_USERNAME"
PASSWORD="YOUR_PASSWORD"

@app.route("/punch/<ptype>")
def punch(ptype):

    encoded_user=base64.b64encode(USERNAME.encode()).decode()
    encoded_pass=base64.b64encode(PASSWORD.encode()).decode()

    login=requests.post(
        "https://transapi.elitehrms.com/api/admin/getsignin",
        json={
            "loginName":encoded_user,
            "loginpassword":encoded_pass,
            "IPAddress":""
        }
    )

    token=login.json()["Token"]["Token"]

    response=requests.post(
        "https://transapi.elitehrms.com/api/Attendance/PostEmployeeInOut",
        headers={
            "Authorization":token
        },
        json={
            "PunchType":ptype,
            "PunchTime":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
    )

    return response.text

if __name__=="__main__":
    app.run()