import json


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

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
                          )



print(data['duration'])