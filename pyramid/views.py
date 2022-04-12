import json
from datetime import time, datetime
from html import escape
from pprint import pprint

import requests
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config

clientid = "lT2lQFLTRfLRznkI1zQwg"
clientsecret = "suFBsWDcvjVnEpyovU0LTDCPVfmWywp9"


def base64_encoding(base64_string):
    import base64
    base64_bytes = base64_string.encode ("ascii")

    sample_string_bytes = base64.b64encode (base64_bytes)
    sample_string = sample_string_bytes.decode ("ascii")

    return sample_string


def myconverter(o):
    if isinstance (o, datetime.datetime):
        return o.__str__ ()


@view_config (route_name='refreshaccess')
def refreshaccess(request):
    global user_detail
    # access token expires in one hour so refresh that
    data = requests.post (
        f"https://zoom.us/oauth/token?refresh_token={user_detail['refresh_token']}&grant_type=refresh_token",
        headers={
            "Authorization": "Basic " + base64_encoding (clientid + ":" + clientsecret),
            "Content-Type": "application/x-www-form-urlencoded"
        })
    return Response (data.text)


@view_config (route_name='redirect')
def redirect_view(request):
    # creating a access token
    global user_detail

    code = request.GET["code"]
    data = requests.post (
        f"https://zoom.us/oauth/token?code={code}&grant_type=authorization_code&redirect_uri=http://localhost:6543/goto",
        headers={
            "Authorization": "Basic " + base64_encoding (clientid + ":" + clientsecret),
            "Content-Type": "application/x-www-form-urlencoded",
        })

    user_detail = {
        "access_token": data.json ()["access_token"],
        "token_type": data.json ()["token_type"],
        "refresh_token": data.json ()["refresh_token"],
        "expires_in": data.json ()["expires_in"],
        "scope": data.json ()["scope"],
    }

    print ("access_token" + user_detail["access_token"])
    print ("token_type" + user_detail["token_type"])
    print ("refresh_token" + user_detail["refresh_token"])
    print ("expires_in" + str (user_detail["expires_in"]))
    print ("scope" + user_detail["scope"])
    # getting data from zoom server using access token
    print (datetime.now ())
    return Response (data.text)


@view_config (route_name='createmeeting')
def create(request):
    global user_detail
    data = requests.post ("https://api.zoom.us/v2/users/me/meetings",
                          headers={
                              "Authorization": f"Bearer {user_detail['access_token']}",
                              'content-type': "application/json",
                          },
                          data=json.dumps ({
                              "topic": "test",
                              "type": 2,
                              "duration": "30",
                              "settings": {
                                  "host_video": "true",
                                  "participant_video": "true",
                                  "join_before_host": "true",
                                  "mute_upon_entry": "true",
                                  "watermark": "true",
                                  "audio": "voip",
                                  "auto_recording": "cloud"
                              }

                          }
                          ))

    return Response (data.text)


@view_config (route_name='listmeeting')
def listmeeting(request):
    global user_detail
    data = requests.get("https://api.zoom.us/v2/users/me/meetings",
                          headers={
                              "Authorization": f"Bearer {user_detail['access_token']}",
                              'content-type': "application/json",
                          },
                          data=json.dumps ({
                              "next_page_token": "Tva2CuIdTgsv8wAnhyAdU3m06Y2HuLQtlh3",
                              "page_count": 1,
                              "page_number": 1,
                              "page_size": 30,
                              "total_records": 1,
                              "meetings": [
                                  {
                                      "agenda": "My Meeting",
                                      "created_at": "2022-03-23T05:31:16Z",
                                      "duration": 60,
                                      "host_id": "30R7kT7bTIKSNUFEuH_Qlg",
                                      "id": 97763643886,
                                      "join_url": "https://example.com/j/11111",
                                      "pmi": "97891943927",
                                      "start_time": "2022-03-23T06:00:00Z",
                                      "timezone": "America/Los_Angeles",
                                      "topic": "My Meeting",
                                      "type": 2,
                                      "uuid": "aDYlohsHRtCd4ii1uC2+hA=="
                                  }
                              ]
                          }
                          ))

    return Response (data.text)

@view_config(route_name='delete')
def delete(request):
    data = requests.delete("https://api.zoom.us/v2/meetings/84353893081",
                           headers={
                               "Authorization": f"Bearer {user_detail['access_token']}",
                               'content-type': "application/json",
                           }
                           )
    print(data.text)
    return Response(data.text)

@view_config(route_name='recording')
def record(request):
    global user_detail
    data = requests.get("https://api.zoom.us/v2/meetings/82886187376/recordings",
                        headers={
                            "Authorization": f"Bearer {user_detail['access_token']}",
                            'content-type': "application/json",
                        }
                        )
    return Response(data.text)


@view_config (route_name='revoke')
def revoke(request):
    # revoking a access token
    data = requests.post (f"https://zoom.us/oauth/revoke?token={user_detail['access_token']}",
                          headers={
                              "Authorization": "Basic " + base64_encoding (clientid + ":" + clientsecret),
                              "Content-Type": "application/x-www-form-urlencoded"
                          })
    return Response (data.text)
