# title 
oss-project1-cau

# original source code
https://github.com/Axel-Erfurt/QFilemanager

# How to install
**[OS]** Ubuntu 22.04.2
**[Requirements]** Python3, PyQt5, PyQtWebEngine, send2trash

sudo apt install python3-pip  
pip3 install PyQt5  
pip3 install PyQtWebEngine  
pip3 install send2trash  
sudo apt-get install --reinstall libxcb-xinerama0 

**Ubuntu 언어 English**

sudo apt install git
cd oss-project1-cau
cd QFilemanager

# 기능
**1. [toolbar] git init & git commit button**
- git init 버튼: git이 관리하고 있지 않은 폴더에서 누르면 git이 관리하기 시작한다.
![git init button](./QFilemanager/icons8-git-48.png)
- git commit 버튼: 버튼을 누르면 commit할 git stage에 대한 정보가 출력되고 OK를 누르고 commit 메시지를 작성하면 commit이 된다.
![git commit button](./QFilemanager/icons8-commit-git-64.png)

**2. git status icon**
각 파일 왼쪽에서 git status를 나타내준다.
- commited ![committed icon](./QFilemanager/icon/comitted.png)
- modified ![modified icon](./QFilemanager/icon/modified.png)
- staged ![staged icon](./QFilemanager/icon/staged.png)
- untracked ![untracked icon](./QFilemanager/icon/untracked.png)
- staged_modified ![staged_modified icon](./QFilemanager/icon/staged_modified.png)
- staged_untracked ![staged_untracked icon](./QFilemanager/icon/staged_untracked.png)

**3. context menu**
각 파일에서 마우스 오른쪽 버튼을 클릭하면 각 git status에 맞는 메뉴가 나온다.
- for untracked files:
    git add
- for modified files: 
    git add
    git restore
- for staged files:
    git restore --staged
- for committed or unmodified files:
    git rm --cached
    git rm
    git mv

# 커밋 컨벤션
메시지 형식: [커밋 종류] [메시지] [#이슈]

### 커밋 종류:
- feat
- debug
- refactor
- chore
- build
- docs
