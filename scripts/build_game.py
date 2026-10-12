"""Run an original generator in an isolated directory and restore organized outputs."""
from pathlib import Path
import json, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]

def game_info(game_id):
    index=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
    entry=next((g for g in index['games'] if g['id']==game_id),None)
    if entry is None:raise SystemExit('Unknown game: '+game_id)
    game=ROOT/entry['path']
    return game,json.loads((game/'game.json').read_text(encoding='utf-8'))

def build(game_id):
    game,meta=game_info(game_id)
    config=meta.get('builder')
    if not config:raise SystemExit('No builder configured; see this game README.')
    with tempfile.TemporaryDirectory(prefix='children-game-') as temporary:
        work=Path(temporary)/config['working_directory_name'];work.mkdir()
        for filename in config['source_files']:shutil.copy2(game/'src'/filename,work/filename)
        for rel in meta.get('assets',[]):
            destination=work/rel;destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(game/rel,destination)
        shutil.copy2(game/'references/图画提示词.md',work/config['prompt_filename'])
        subprocess.run([sys.executable,str(work/config['entry'])],check=True,cwd=work)
        for original,relative in config['outputs'].items():
            # Generator copies of source and artwork are unchanged inputs.
            if relative.startswith(('src/','assets/','references/图画提示词')):continue
            output=work/original
            if not output.is_file():raise SystemExit('Missing generated output: '+original)
            destination=game/relative;destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(output,destination)
    print('Generated:',game_id)
    print('Render and inspect both PDFs before updating the ZIP.')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python scripts/build_game.py GAME_ID')
    build(sys.argv[1])
