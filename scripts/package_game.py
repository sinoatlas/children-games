"""Update the complete download kit without mixing games."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,sys

ROOT=Path(__file__).resolve().parents[1]

def package(game_id):
    index=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
    entry=next((g for g in index['games'] if g['id']==game_id),None)
    if entry is None:raise SystemExit('Unknown game: '+game_id)
    game=ROOT/entry['path'];meta=json.loads((game/'game.json').read_text(encoding='utf-8'))
    archive=ROOT/entry['download'];archive.parent.mkdir(parents=True,exist_ok=True)
    config=meta.get('builder')
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        if config:
            folder=config['working_directory_name']
            for original,relative in config['outputs'].items():z.write(game/relative,folder+'/'+original)
        else:
            for file in sorted(game.rglob('*')):
                if file.is_file() and '__pycache__' not in file.parts:
                    z.write(file,game_id+'/'+file.relative_to(game).as_posix())
    with ZipFile(archive) as z:
        if z.testzip():raise SystemExit('Corrupt download archive')
    print('Packaged:',entry['download'])

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python scripts/package_game.py GAME_ID')
    package(sys.argv[1])
