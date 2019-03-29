import json
from zipfile import ZipFile
from xml.etree.ElementTree import Element, SubElement, ElementTree


#3.创建一个类TopicInfo，以类的方式获取xmind元素信息，比如 topic_name就能获取xmind里某一个node的title
class TopicInfo(object):
    def __init__(self, roottopic):
        self.roottopic = roottopic
        self.topic_name = ""
        self.topic_notes = ""
        self.topic_marker = ""
        self.detached_child_topic_list = []
        self.attached_childTopic_list = []
        self.sub_topics = []

        # get current node's topic name
        self.topic_name = self.roottopic['title']

        # get current node's notes
        if 'notes' in self.roottopic.keys():
            self.topic_notes = self.roottopic['notes']['plain']['content']

        #get current node's markers
        if 'markers' in self.roottopic.keys():
            if len(self.roottopic['markers']) > 0:
                self.topic_marker = self.roottopic['markers'][0]['markerId']

        #get child nodes info
        if 'children' in self.roottopic.keys():
            child_topic = self.roottopic['children']
            if 'attached' in child_topic:
                #get child node list
                self.attached_childTopic_list = child_topic['attached']
                for topic in self.attached_childTopic_list:
                    if 'title' in topic.keys():
                        #get child node name list
                        self.sub_topics.append(topic['title'])

#1.解压xmind文件
def unzipxmind(filepath):
    with ZipFile(filepath) as xmind_file:
        for f in xmind_file.namelist():
            if f == "content.json":
                with xmind_file.open(f) as contentJsonFile:
                    return contentJsonFile.read().decode('utf-8')
#2.把xmind文件的内容转换成json数据格式
def xmind2json(filepath):
    file_content = unzipxmind(filepath)
    return json.loads(file_content)

#5.保存xml文件，如果没有设定xml的名字则默认为default.xml
def save_xml(root, xmlfilename='default.xml'):
    tree = ElementTree(root)
    tree.write(xmlfilename, encoding="utf-8", xml_declaration=True)

#4.通过TopicInfo类读取json数据来创建xml
def json2xml(filepath, xmlfilename):
    file_json_content = xmind2json(filepath)
    sheet = file_json_content[0] #get the first sheet
    rootTopic = sheet['rootTopic']

    rt = TopicInfo(rootTopic)
    root = Element('testsuite', {'name': ''})

    #testsuite
    if len(rt.attached_childTopic_list) > 0:
        for childnode in rt.attached_childTopic_list:
            cd = TopicInfo(childnode)
            testsuite = SubElement(root, 'testsuite', {'name': cd.topic_name})
            #testcase
            if len(cd.attached_childTopic_list) > 0:
                for childnode in cd.attached_childTopic_list:
                    cd = TopicInfo(childnode)
                    testcase = SubElement(testsuite, 'testcase', {'name': cd.topic_name})
                    # print(cd.topic_name, cd.topic_marker, cd.topic_notes, cd.sub_topics)

                    #steps->step (actions/expected)
                    if len(cd.attached_childTopic_list) > 0:
                        #steps
                        steps = SubElement(testcase, 'steps')
                        #actions
                        for childnode in cd.attached_childTopic_list:
                            cd = TopicInfo(childnode)
                            step = SubElement(steps, "step")
                            actions = SubElement(step, "actions")
                            actions.text = cd.topic_name

                            #expected
                            if len(cd.attached_childTopic_list) > 0:
                                for childnode in cd.attached_childTopic_list:
                                    cd = TopicInfo(childnode)
                                    expected = SubElement(step, "expectedresults")
                                    expected.text = cd.topic_name

    save_xml(root, xmlfilename)


if __name__ == '__main__':
    json2xml(r"test1.xmind", 'test.xml') #如果没有设定xml的名字则默认为default.xml

