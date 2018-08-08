# -*- coding: utf-8 -*-
# @Author: Clarence
# @Date:   2018-06-24 11:06:27
# @Last Modified by:   Clarence
# @Last Modified time: 2018-06-25 17:06:00
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

class  TestMongo(object):

	def __init__(self):
		self.client = MongoClient()
		# 获取到数据库students
		self.db = self.client['blog']

	def add_one(self):
		'''新增一条数据'''
		post = {
		'title' : '标题',
		'content' : '内容',
		'created_at' : datetime.now()
		}
		# self.db.students用来获取students集合 
		# 数据库名为blog, 集合名字为blog.posts
		rest = self.db.blog.posts.insert_one(post)
		return rest

	def  add_many(self, data):
		'''新增多条数据'''
		rest = self.db.students.insert_many(data)
		return rest


	def get_count(self):
		print('数据集合blog.posts中共有: %s 条数据' %self.db.blog.posts.count())

	def get_one(self):
		'''从集合blog.posts中查询一条数据'''
		return self.db.blog.posts.find_one()

	def get_more(self):
		'''查询多条数据'''
		return self.db.blog.posts.find()

	def get_from_oid(self, oid):
		'''根据记录的ID来获取数据'''
		return self.db.blog.posts.find_one({'_id' : ObjectId(oid)})

	def update(self):
		'''修改数据'''
		# 修改一条数据 将x加10
		# rest = self.db.blog.posts.update_one({'x' : 11}, {'$inc' : {'x' :10}})
		# return rest
		# 修复多条数据,将所有数据x增加10
		return self.db.blog.posts.update_many({}, {'$inc' : {'x' : 10}})

	def delete(self):
		'''删除数据'''
		# 删除一条数据
		#return self.db.blog.posts.delete_one({'x' : 31})
		# 删除多条数据
		return self.db.blog.posts.delete_many({'x' : 10})




data = [
      { 'name': "bob",'age': 16, 'sex': "male", 'grade': 95},
      { 'name': "ahn", 'age': 18, 'sex': "female", 'grade': 45},
      { 'name': "xi", 'age': 15, 'sex': "male", 'grade': 75},
   ]

def main():
	obj = TestMongo()
	#添加一条数据
	# rest = obj.add_one()
	# print(rest.inserted_id)
	# '''获取集合中的文档数量'''
	# obj.get_count()

	# 添加多条数据
	# rest = obj.add_many(data)
	# print(rest.inserted_ids)

	# 获取一条数据
	# rest = obj.get_one()
	# print(rest['_id'])

	# 获取多条数据
	# rest = obj.get_more()
	# print(type(rest)) #类型是pymongo.cursor.Cursor对象
	# for each in rest:
	# 	print(each)

	# rest = obj.get_from_oid("5b3062d6ded7e73a149d368b")
	# print(rest['_id'])
	# 删除数据
	# result = obj.update()
	# print(result.matched_count)
	# print(result.modified_count)
	rest = obj.delete()
	# 打印删除的文档数量
	print(rest.deleted_count)



if __name__ == '__main__':
	main()
