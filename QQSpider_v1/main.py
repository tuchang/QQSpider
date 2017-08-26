#-*- coding:utf-8 -*-

import codecs, time, random, os
from login import login
from util import util
from friends import get_friends
from blogs import get_blogs
from messages import get_messages
from moods import get_moods
from db import db
from status import status

qq_num = '123456'
qq_pwd = 'password'

def get_friends_info():
	friends = get_friends.Get_friends()
	friends.get_friends(lg.qq, util.get_cookie(), db)

def get_blogs_info():
	blogs = get_blogs.Get_blogs()
	blogs_info = blogs.get_blogs(lg.qq, util.get_cookie())

def get_messages_info(target_qq):
	messages = get_messages.Get_messages()
	messages.get_messages(lg.qq, target_qq, util.get_cookie(), db)

def get_moods_info(target_qq):
	moods = get_moods.Get_moods()

	try:
		moods.moodstatus = status.load_mood_status(db, 'mood_status', target_qq)
	except:
		status.save_mood_status(db, 'mood_status', target_qq, moods.moodstatus)

	if moods.moodstatus != {}:
		moods.get_moods(lg.qq, target_qq, util.get_cookie(), db)


if __name__ == '__main__':
	lg = login.Login(qq_num, qq_pwd)
	db = db.DB()
	if not os.path.isfile('friends.txt'):
		if lg.login_test():
			print u"getting all friends..."
			db.Create_db('db' + qq_num)
			get_friends_info()

	status = status.Status()
	friendsqq = codecs.open('friends.txt', 'r', 'utf-8')

	if lg.login_test():
		for target_qq in friendsqq:
			target_qq = target_qq.strip('\n').strip('\r')
			dict = []
			sql = 'SELECT SCHEMA_NAME FROM information_schema.SCHEMATA;'
			for i in db.Query_data('information_schema', sql):
				dict.append(i[0])
			if target_qq not in dict:
				print 'current qq: %s' % target_qq
				db.Create_db('db' + target_qq)
				try:
					#get_moods_info(target_qq)
					get_messages_info(target_qq)
				except Exception, e:
					print e
					break
	else:
		print 'login error, exit.'
