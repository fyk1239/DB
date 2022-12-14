# DB 更改代码后，将更改应用到数据库的操作说明
若模型有变动：

	python manage.py makemigrations
	python manage.py migrate

若初始数据有变化：

	python manage.py loaddata init_data.json

