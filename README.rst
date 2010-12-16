
A python client for http://www.bugmenot.com/
=============================================

Usage
--------
::

	537 ~/git/py-bugmenot> ./bugmenot.py -h
	Usage: bugmenot.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -s SITE, --site=SITE  The target site
	  -t RET, --ret_type=RET
							The return type(text/json)

	538 ~/git/py-bugmenot> ./bugmenot.py -s www.douban.com
	Username                      	Password            
	8gmenot@gmail.com             	bugmenot            
	duzhengyu1986@126.com         	dhyqpzm7913         
	396351252@qq.com              	1990816             
	123098                        	123                 
	xiaobiao@bugmenot.com         	8229193             

	539 ~/git/py-bugmenot> ./bugmenot.py -s www.douban.com -t json
	[{"username": "8gmenot@gmail.com", "password": "bugmenot"}, {"username": "duzhengyu1986@126.com", "password": "dhyqpzm7913"}, {"username": "396351252@qq.com", "password": "1990816"}, {"username": "123098", "password": "123"}, {"username": "xiaobiao@bugmenot.com", "password": "8229193"}]



