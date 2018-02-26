1. 生成公钥上传到Github
	https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#platform-linux
	同时在网站创建一个仓库，flask-blog.git 	
2. 本地配置，已经配置过不需要
	git config --global user.email "your-email"
	git config --global user.name "your-name"

3. 	创建GitHub项目
	进入flask_microblog文件夹
	vim ./.gitignore
		/flask
		*.pyc
		*.db
	echo "开始搭建一个博客" >> README.md
	git init
	git add.
	git commit -m 'begin build blog'
	git remote add origin https://github.com/*yourname*/flask-blog.git
	git push -u origin master
	
	a. 如果git remote add 这一步因为各种原因出错
		可以先查看 git remote -v,查看你当前项目远程连接的是哪个仓库地址，看一下origin对应的库是不是正确
		git remote rm origin 删除，然后重新设置git remote add origin https://github.com/*yourname*/flask-blog.git
		如果删除不成功，打开gitconfig的文件，
		vim ~/.gitconfig  打开它把里面的[remote "origin"]那一行删掉
		
	b. 要移除跟踪但不删除文件,以便稍后在 .gitignore 文件中补上,git rm -r --cached tmp/
		git rm -r tmp/ 直接删除这个目录下的所有文件，可能需要加-f参数
		git rm -r -n --cached tmp/  查看会移除那些文件，并不会真的移除