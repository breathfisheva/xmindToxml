import json
from zipfile import ZipFile

#unzip xmind file , get file_content
with ZipFile(r"test1.xmind") as xmind_file:
    for f in xmind_file.namelist():
        if f == "content.json":
            with xmind_file.open(f) as contentJsonFile:
                file_content = contentJsonFile.read().decode('utf-8')

#change file to json format
file_json_content = json.loads(file_content)

#get root_topic
root_topic = file_json_content[0]["rootTopic"] # file_json_content[0] 第一个sheet， file_json_content[1] 第二个sheet， 以此类推
cur_node = root_topic

root_topic_name = root_topic["title"]

#get roote topic notes
if "notes" in cur_node:
    note_content = cur_node["notes"]["plain"]["content"]

#get secondary node
children_node_list = root_topic["children"]["attached"]
for child in children_node_list:
    child_name = child["title"]