# This is NETWORK - OS PBL
## Description
This project aims to build a Web Server to manage and control Raspberry remotely. With this system, users can perform the following functions:
- Managing resources: view CPU parameters, disk space, network traffic and RAM/SWAP performance realtime.
- Managing files: view files and folders, add new file/folder, rename and delete file/folder.
- Managing applications: view application list and uninstall applications.
- Managing users: view user list, add new user, update and delete user.
- Remote controlling via Terminal: execute the commands via terminal.
- Tracking resource, users log: view history of CPU performance, network traffic and user actions.
## How to run (Raspbian OS)
- Edit some config in .env_example, then rename to .env
- Install python and run `pip install -r requirements.txt`
- Create database: `python database.py`
- Run server: `python main.py`

## Result 
- [Demo video](https://youtu.be/rsIklOp8tVY)
- [Report](https://github.com/huytuong010101/PBL4-Raspberry-Server-ControlAndTracking/blob/main/PBL4-Report.pdf)

## Member
- Nguyen Huy Tuong
- [Le Hoang Ngoc Han](https://github.com/hanahh080601)
