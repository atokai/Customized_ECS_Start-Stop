# Customized ECS Start/Stop Python Script

Customized **ECS Start/Stop** Python script for **Open Telekom Cloud**.

Sometimes, we receive questions about how to update, simplify, or extend a given template to better serve customer needs. The **ECS-Start** and **ECS-Stop** **Function Graph** templates are useful, but they are quite basic and not very user-friendly. [In my previous article](https://community.open-telekom-cloud.com/community?id=community_blog&sys_id=f01ff5a46be46a10d15a9a74ab63fbdd), I explained how to work with environment variables, which many found confusing. To address these limitations, I’ve developed a new Start/Stop script.

## Features
- Uses **AK/SK authentication** to avoid issues caused by password expiration  
- Works on both **VMs and local PCs**  
- Supports both **frontend and backend server pools**  
- Waits for ECS **status changes** before proceeding 

## Requirements
- Python 3.9+  
- Open Telekom Cloud SDK 
- AK/SK credentials 

## Installation
```bash
git clone https://github.com/your-repo/ecs-start-stop.git
cd ecs-start-stop
pip install -r requirements.txt
```

## Usage
Run the script directly from your local machine:
```bash
python ECS_start_stop.py
```
You can also integrate it into **Function Graph** by copying the relevant function and main logic.

## That’s All Folks!