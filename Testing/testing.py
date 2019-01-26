import json
ff = b'[{"faceRectangle":{"top":149,"left":190,"width":73,"height":73},"faceAttributes":{"emotion":{"anger":0.0,"contempt":0.003,"disgust":0.0,"fear":0.0,"happiness":0.0,"neutral":0.978,"sadness":0.019,"surprise":0.0}}}]'
ff = ff.decode()
gg = json.loads(ff)
final_data = gg[0]['faceAttributes']['emotion']
#sorted(ll, key=lambda dct: dct['name'])
print(final_data)
max_val = -1
max_index = ""
for list in final_data:
    if final_data[list] > max_val:
        max_val = final_data[list]
        max_index = list
print(max_index)

