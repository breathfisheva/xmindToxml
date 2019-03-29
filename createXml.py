from xml.etree.ElementTree import Element, SubElement, ElementTree

#首先创建根节点
root = Element('lab')

#添加子节点SubElement(父节点Element对象， Tag字符串格式， Attribute字典格式)
person1 = SubElement(root, 'person', {'name':'Blue'})

#添加子节点
age1 = SubElement(person1, 'age')
#添加text，即22，字符串格式
age1.text = '22'
gender1 = SubElement(person1, 'gender')
gender1.text = 'male'

person2 = SubElement(root, 'person', {'name':'Yellow'})
age2 = SubElement(person2, 'age')
age2.text = '20'
gender2 = SubElement(person2, 'gender')
gender2.text = 'female'

#将根目录转化为xml树状结构(即ElementTree对象)
tree = ElementTree(root)
#写入xml文件
tree.write('sample.xml', encoding="utf-8", xml_declaration=True)