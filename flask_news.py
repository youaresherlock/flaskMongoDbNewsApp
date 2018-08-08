# -*- coding: utf-8 -*-
# @Author: Clarence
# @Date:   2018-08-06 22:36:44
# @Last Modified by:   Clarence
# @Last Modified time: 2018-08-08 21:52:37

from datetime import datetime
from forms import NewsForm
from flask import Flask, render_template, flash, redirect, url_for, abort, request
from flask_mongoengine import MongoEngine

app = Flask(__name__)

# 设置主机名和端口号以及要连接的数据库
app.config['MONGODB_SETTINGS'] = {
	'db' : 'flask_news',
	'host' : '127.0.0.1',
	'port' : 27017	
}
app.config['SECRET_KEY'] = 'my name is Clarence'


db = MongoEngine(app)

NEWS_TYPES = (('推荐', '推荐'), 
	('百家', '百家'), 
	('本地', '本地'),
	('图片', '图片')
)

class News(db.Document):
	""" 新闻模型 """
	title = db.StringField(required = True, max_length = 200)
	content = db.StringField(required = True)
	news_type = db.StringField(required = True, choices = NEWS_TYPES)
	img_url = db.StringField()
	is_valid = db.BooleanField(default = True)
	created_at = db.DateTimeField(default = datetime.now())
	updated_at = db.DateTimeField(default = datetime.now())

	# eg: 进行标题过滤 https://mongoengine-odm.readthedocs.io/guide/document-instances.html#pre-save-data-validation-and-cleaning
	def clean(self):
		if '黄' in self.title:
			raise db.ValidationError('不能有黄字')

	# 指定连接数据库集合和排序规则
	meta = {
	'collection' : 'mongo_news',
	'ordering' : ['-created_at']
	}

# 设置根目录的路由
@app.route('/')
def index():
	''' 新闻首页 '''
	news_list = News.objects.filter(is_valid = True)
	return render_template('index.html', news_list = news_list)

# 内容页
@app.route('/cat/<name>')
def cat(name):
	''' 新闻类别页 '''
	news_list = News.objects.filter(is_valid = True, news_type = name)
	return render_template('cat.html', news_list = news_list)

# 详情页 无需声明类型，我们是以ObjectId为主键
@app.route('/detail/<pk>')
def detail(pk):
	''' 新闻详情页 '''
	#new_obj = News.objects.filter(pk = pk).first()
	#first_or_404()在mongengine对这个QuerySet进行了封装
	new_obj = News.objects.filter(pk = pk).first_or_404()
	# if not new_obj:
	# 	abort(404)
	return render_template('detail.html', new_obj = new_obj)

# 后台
@app.route('/admin')
@app.route('/admin/<int:page>')
def admin(page = None):
	''' 后台首页 '''
	if page is None:
		page = 1
	page_data = News.objects.paginate(page = page, per_page = 5)
	return render_template('admin/index.html',
	 page_data = page_data,
	 page = page)

@app.route('/admin/add', methods = ['POST', 'GET'])
def add():
	''' 新增新闻数据 '''
	form = NewsForm()
	if form.validate_on_submit():
		# 从前台表单中获取表单值组成的对象
		new_obj = News(
			title = form.title.data,
			content = form.content.data,
			news_type = form.news_type.data,
			img_url = form.image.data,)
		new_obj.save()
		flash('新增新闻成功')
		return redirect(url_for('admin'))
	return  render_template('admin/add.html', form = form)

# 需要get来获取表单信息
@app.route('/admin/update/<pk>', methods = ['POST', 'GET'])
def update(pk):
	''' 修改新闻数据 也可通过update进行逻辑删除，更改对象的is_valid属性 '''
	new_obj = News.objects.get_or_404(pk=pk)
	form = NewsForm(obj = new_obj)
	if form.validate_on_submit():
		new_obj.title = form.title.data
		new_obj.content = form.content.data
		new_obj.news_type = form.news_type.data
		new_obj.img_url = form.image.data
		new_obj.save()
		flash('修改新闻成功')
		return  redirect(url_for('admin'))
	#返回修改html,获取用户输入的表单信息
	return render_template('admin/update.html', form = form)

@app.route('/admin/delete/<pk>', methods = ['POST'])
def delete(pk):
	''' 删除新闻信息 '''
	new_obj = News.objects.filter(pk = pk).first()
	if not new_obj:
		return 'no'
	# 逻辑删除
	# new_obj.is_valid = False 
	# new_obj.save()
	# return 'yes'

	# 物理删除 
	new_obj.delete()
	return 'yes'

if __name__ == '__main__':
	app.run(debug = True)