远程仓库同步
# 开发背景
在公司开发团队中，使用git进行代码的管理，之前使用的可能是某一个git服务器，后来需要更换其他的git服务器，就需要将原来的git服务器上所有的仓库的的分支、tag、commit等信息迁移到新的git服务器上，这个时候就需要使用到git-remote-sync这个工具了。

# 基本原理
git-remote-sync的基本原理是：
- 从源git服务器上clone所有的仓库到本地
- 获取远程仓库的所有分支
- 在本地通过checkout -b [branch] [remote]/[branch]创建所有的分支，并且将分支推送到新的git服务器上
- 获取远程仓库的所有tag，并且将tag推送到新的git服务器上

# 使用方式
该工具工作在windows环境下，依赖python 3环境，使用方式如下：

1. 创建一个空文件夹，并将git_remote_sync.py文件拷贝到该文件夹下。
2. 使用IDE打开git_remote_sync.py文件，修改其中的origin_url和target_url，分别为源git服务器和目标git服务器的地址。
```
# origin远程仓库的ssh地址
origin_url = "ssh://wangzhengdong@192.168.11.152:29418/rd2/xpositon/tag/UT241-G_v3_advanced.git"

# 新远程仓库gerrit服务器的ssh地址
gerrit_url = "ssh://wangzhengdong@192.168.11.222:29418/rd2/xpositon/tag/UT241-G_v3_advanced"
```
3. 在命令行中进入到该文件夹下，执行python git_remote_sync.py命令，即可开始同步。
```
python git_remote_sync.py
```