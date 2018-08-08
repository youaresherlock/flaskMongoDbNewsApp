# -*- coding: utf-8 -*-
# @Author: Clarence
# @Date:   2018-06-25 19:54:22
# @Last Modified by:   Clarence
# @Last Modified time: 2018-06-29 20:54:40

from datetime import datetime
from mongoengine import connect, Document, StringField, \
IntField, FloatField,EmbeddedDocument,ListField,DateTimeField,EmbeddedDocumentField

# 连接到本地students数据库
# connect('students')
# connect('students', host = '192/168.1.35', port = 27017)
connect('students', host='mongodb://localhost/students')

SEX_CHOICE = (
	('male', '男'),
	('female', '女'),
)

'''MongoDB has the ablility to embed documents within other documents.Schemata may be defined for these embedded 
documents, just as they may be for regular documents. To create an embedded document, just define a document as usual
, but inherit form EmbeddedDocument rather than Document'''
class Grade(EmbeddedDocument):
	'''科目成绩'''
	name = StringField(required = True)
	score = FloatField(required = True)

'''To define a shema for a document , create a class that inherits from Document.Fields are specified by 
adding field objects as clas attributes to the document class
As BSON(the binary format for storing data in mongodb) is order dependent, documents are serialized based 
on their field order'''
# 默认情况下required属性是False
class Student(Document):
	# MongoDB默认ID作为主键
	name = StringField(max_length = 32, required = True)
	age = IntField(required = True)
	address = StringField()
	sex = StringField(choices = SEX_CHOICE, required = True)
	grades = ListField(EmbeddedDocumentField(Grade)) #不同学生有多个课程和成绩
	school = StringField()
	created_at = DateTimeField(default = datetime.now())

	# 配置元数据
	meta = {
	    # 指定数据集合为students
		'collection' : 'students',
		# 可以通过meta元数据加入指定的排序方式 以年纪的大小倒序排序
		'''Adefault ordering can be specified for your QuerySet using the ordering attribute of meta.
		Ordering will be applied when the QuerySet is created, and can be overridden by subsequent calls to order_by() '''
		'ordering' : ['-age']
	}

class TestMongoEngine(object):

	def add_one(self):
		'''新增数据'''
		yuwen = Grade(
			name = '语文',
			score = 95
			)
		english = Grade(
			name = '英语',
			score = 89
			)
		# required = True都要输入
		stu_obj = Student(
			name = '张三',
			age = 21,
			sex = 'male',
			grades = [yuwen, english]
			)
		stu_obj.save()
		return stu_obj

	def get_one(self):
		''' 查询一条数据 '''
		return Student.objects.first()

	def get_more(self):
		''' 查询多条数据 '''
		return Student.objects.all()

	def get_from_oid(self, oid):
		''' 根据ID来获取数据 '''
		# 主键pk=oid的数据集合 Student.objects.filter(pk=oid)查询结果返回的是QuerySet对象
		return Student.objects.filter(pk=oid).first()
		# 查询的是一个QuerySet集合 也就是set数据结构，里面是查询到的Student对象
		# for each in Student.objects.filter(pk ="5b34e6702ad33bb76f592ae7"):
		# 	print(each.name) 

	def update(self):
		''' 修改数据 '''
		# 修改所有的男生年龄，增加是1岁
		Student.objects.filter(sex = 'male').update(inc__age = 2)
		# 更新性别是男生，年龄大于16岁的文档
		# Student.objects.filter(sex = 'male', age__gt = 16).update()

		# 修改一条数据 查询到的QuerySet中第一个数据减少一百岁
		return Student.objects.filter(sex = 'male').update_one(dec__age = 100)

	def delete(self):
		''' 删除数据 '''
		# 删除单条数据
		# return Student.objects.filter(sex = 'male').first().delete()

		# 删除多条数据
		return Student.objects.filter(sex = 'male').delete()



# 如果get_from_age获取指定年龄的学生，通过Student.objects.get()方式获得多条会产生异常MultipleObjectsReturned

def main():
	obj = TestMongoEngine()

	# 添加数据
	# rest = obj.add_one() #返回的是加入的Student对象
	# print(rest.id)
	# for each in Student.objects:
	# 	print(each.name)

	# 查找第一条数据 由于是以年纪倒序进行排序，所以第一个数据年龄最大
	# result = obj.get_one()
	# print(result.id,result.name)

	# 查找所有的数据
	# rows = obj.get_more()
	# for row in rows:
	# 	print(row.id, row.name)

	# 根据ID查询指定的数据 如果查找不到返回NoneType
	# result = obj.get_from_oid("5b34e82bded7e722208f18b8")
	# if result:
	# 	print(result.id, result.name)

	# 更新数据 返回的是NoneType类型
	# obj.update()

	# 删除数据
	result = obj.delete()
	print(result)


if __name__ == '__main__':
	main()