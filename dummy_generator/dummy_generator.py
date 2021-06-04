from data_dummy import *
import os
import json
import base64
import mimetypes
import requests
import time


list_file = os.listdir("./dummy_img")
url = "http://localhost:5001/tensile-ship-312415/us-central1/api/laporans"
access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFiMGNiMTk5Zjg3MGYyOGUyOTg5YWI0ODFjYzJlNDdlMGUyY2MxOWQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiS2lraSBIYXJhcGFuIEh1dGFwZWEiLCJyb2xlIjoiYWRtaW4iLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVuc2lsZS1zaGlwLTMxMjQxNSIsImF1ZCI6InRlbnNpbGUtc2hpcC0zMTI0MTUiLCJhdXRoX3RpbWUiOjE2MjI3ODU0OTMsInVzZXJfaWQiOiJXdEQ4ZTFXdkVHZ3liNGg2TUhmZ0VVY25yY3AxIiwic3ViIjoiV3REOGUxV3ZFR2d5YjRoNk1IZmdFVWNucmNwMSIsImlhdCI6MTYyMjc4NTQ5MywiZXhwIjoxNjIyNzg5MDkzLCJlbWFpbCI6Imtpa2kxOHRpQG1haGFzaXN3YS5wY3IuYWMuaWQiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsia2lraTE4dGlAbWFoYXNpc3dhLnBjci5hYy5pZCJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.Go6uRdTZPbSJp8_9gLoCbCnjB9CpxG4HDERGWTcoTI9XK0zDUvDdtelAsHf2cz0-HpOp0HOMeVcOa6Og3f-tNYAO-oD77ROn-G_f9Nozddoa_SPtS3CElnUjzp9vqYu73zFIDDhJdGKhix9KC58wLETvmqqJQufn4eq-3sB9D6wGTCyuj1Y7kI6hckFnECJepdtV4bRdPniRgU-O8IonDjh4Sl70QL-qzblZEkF5JTlCX-4QQ4XZx07hpf9_G0SjFkokzsu9p1OxBKxmzRS-1LCszvnfX8JIPCc7uftLBa3ZTaH84g1MIoqtT1iipxtiq5ZRQuNRCdzRHIq6bkEfbw"

headers = {
    "Authorization": "Bearer {}".format(access_token),
    "Accept": "application/json"
}
for d in range(len(data)):
    test_data = data[d]
    test_file = list_file[d]

    file_mime = mimetypes.MimeTypes().guess_type(test_file)[0]

    print(d, test_data, test_file, file_mime)


    with open ("./dummy_img/"+test_file, "rb") as f:
        im_b64 = base64.b64encode(f.read())

    test_data["foto"] = "data:{};base64,{}".format(file_mime,im_b64.decode("utf-8"))
    payload = test_data
    # print(payload[:500])
    x = requests.post(url, json=payload, headers=headers)
    print(x.text)
    time.sleep(60)
