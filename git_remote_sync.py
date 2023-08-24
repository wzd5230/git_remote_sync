import os
import subprocess

# 该脚本中的命令都是在windows下执行的

# origin远程仓库的ssh地址
origin_url = "ssh://wangzhengdong@192.168.11.152:29418/rd2/xpositon/tag/UT241-G_v3_advanced.git"

# 新远程仓库gerrit服务器的ssh地址
gerrit_url = "ssh://wangzhengdong@192.168.11.222:29418/rd2/xpositon/tag/UT241-G_v3_advanced"

# 项目名称，也是clone到本地的文件夹名称
proj_name = None

# 从origin仓库克隆到本地
def clone_from_origin():
    global proj_name
    subprocess.run(["git", "clone", origin_url])
    proj_name = origin_url.split("/")[-1].replace(".git", "")
    print(f"已从 origin 仓库克隆到本地: {proj_name}")

# 进入项目文件夹
def enter_proj():
    os.chdir(proj_name)
    print(f"进入 {proj_name} 文件夹")

# 增加新的远程仓库，名称为gerrit，ssh地址为gerrit_url
def remote_add_gerrit():
    subprocess.run(["git", "remote", "add", "gerrit", gerrit_url])
    print(f"已将 gerrit 仓库添加为远程仓库")

# 将origin仓库的分支推送到gerrit仓库
def push_to_gerrit():
    # 获取origin远程的所有分支，并打印执行的命令
    origin_branches = subprocess.check_output("git branch -r", shell=True)
    print("git branch -r")
    
    # 对origin_branches进行处理，删除每个item前后的空格、tab
    origin_branches = origin_branches.decode("utf-8").split("\n")
    origin_branches = [x.strip() for x in origin_branches]
    origin_branches = [x.strip("\t") for x in origin_branches]
    origin_branches = [x for x in origin_branches if x != ""]

    # 删除以origin/HEAD开头的item
    origin_branches = [x for x in origin_branches if not x.startswith("origin/HEAD")]

    # 删除不是以origin/开头的item
    origin_branches = [x for x in origin_branches if x.startswith("origin/")]

    # 删除其他item中的origin/
    origin_branches = [x.replace("origin/", "") for x in origin_branches]

    # 打印分支数，并逐行打印origin_branches
    print(f"branches count: " + str(len(origin_branches)))
    for branch in origin_branches:
        print(branch)

    # 遍历origin_branches，在本地通过git checkout -b命令创建分支，并将分支推送到gerrit仓库
    for branch in origin_branches:
        # 打印在处理的分支名称
        print("branch: " + branch)

        # 使用git checkout -b "branch_name" "origin/branch_name"命令创建分支，在分支名称两边加上双引号，防止分支名称中有空格时出错
        subprocess.call("git checkout -b \"" + branch + "\" \"origin/" + branch + "\"", shell=True)
        print("git checkout -b \"" + branch + "\" \"origin/" + branch + "\"")

        # 使用git push gerrit branch_name命令推送分支
        subprocess.call("git push gerrit \"" + branch + "\"", shell=True)
        print("git push gerrit \"" + branch + "\"")
        
    # 从origin仓库拉取tags，并打印执行的命令
    subprocess.call("git fetch origin --tags", shell=True)
    print("git fetch origin --tags")

    # 将本地的tags推送到gerrit仓库，并打印执行的命令
    subprocess.call("git push gerrit --tags", shell=True)
    print("git push gerrit --tags")


# 退出当前工作目录
def exit_proj():
    os.chdir("..")
    print("已退出到上一级目录")

# 模块调用接口，2个参数分别赋值给origin_url、gerrit_url
def move_repo(in_origin_url, in_gerrit_url):
    global proj_name
    global origin_url
    global gerrit_url

    # 对in_origin_url、in_gerrit_url进行校验
    if in_origin_url == None or in_origin_url == "":
        print(f"{origin_url} 不能为空")
        return
    if in_gerrit_url == None or in_gerrit_url == "":
        print(f"{gerrit_url} 不能为空")
        return
    
    # 赋值给origin_url、gerrit_url
    origin_url = in_origin_url
    gerrit_url = in_gerrit_url

    # 执行迁移操作
    print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print(f"开始从 {origin_url} 仓库迁移到 {gerrit_url} 仓库")
    clone_from_origin()
    enter_proj()
    remote_add_gerrit()
    push_to_gerrit()
    exit_proj()
    print(f"已从 {origin_url} 仓库迁移到 {gerrit_url} 仓库")
    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# 直接运行该脚本时，执行该if语句块，使用变量定义的origin_url、gerrit_url
if __name__ == "__main__":
    clone_from_origin()
    enter_proj()
    remote_add_gerrit()
    push_to_gerrit()
    exit_proj()