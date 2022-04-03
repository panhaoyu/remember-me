from pathlib import Path

import phy_django.runs
import requests

phy_django.runs.init_run('remember_me')

from word.models import WordModel

target_dir = Path(__file__).parent / 'voices'
target_dir.mkdir(parents=True, exist_ok=True)

for o in WordModel.objects.all():
    data = requests.get(f'http://dict.youdao.com/dictvoice?type=0&audio={o.word}').content
    with open(target_dir / f'{o.id}.mp3', 'wb') as f:
        f.write(data)
