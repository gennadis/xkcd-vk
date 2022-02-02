# Post random XKCD comics on VK group wall

This project is a simple command line tool for fetching [XKCD comics](https://xkcd.com/)  
and posting them to your [VK](https://vk.com/) community wall.

## Features
- Download random XKCD comics image and title
- Publish it as VK community wall post
- Comics picture will be deleted after posting.

## Setup
1. Clone project
```bash
git clone https://github.com/gennadis/xkcd-vk.git
cd xkcd-vk
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Rename `.env.example` to `.env` and place your secrets accordingly

5. Run
```bash
python main.py
```
