"""Validate catalog links, PDFs, card IDs, packages and optional file hashes."""
from pathlib import Path
from zipfile import ZipFile
import json,re,hashlib,sys
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]

def require(condition,message):
    if not condition:raise SystemExit(message)

def inside(relative):
    path=(ROOT/relative).resolve()
    require(path.is_relative_to(ROOT),'Path outside repository: '+str(relative))
    return path

def check():
    index=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
    seen=set();total_pages=0;total_cards=0
    for entry in index['games']:
        gid=entry['id'];require(gid not in seen,'Duplicate game ID: '+gid);seen.add(gid)
        require(re.fullmatch(r'\d{3}-[a-z0-9-]+',gid) is not None,'Invalid game ID: '+gid)
        game=inside(entry['path']);require((game/'README.md').is_file(),'Missing game README')
        meta=json.loads((game/'game.json').read_text(encoding='utf-8'))
        require(meta['id']==gid and meta['version']==entry['version'],'Catalog metadata mismatch: '+gid)
        for key,relative in meta['files'].items():
            path=(game/relative).resolve();require(path.is_relative_to(game),'Invalid file path')
            require(path.is_file(),'Missing '+key+': '+str(path))
        for kind in ['rulebook','materials']:
            pages=PdfReader(game/meta['files'][kind]).pages
            require(len(pages)==meta['pdf_pages'][kind],'PDF page mismatch: '+gid+' '+kind)
            require(all(p.extract_text() for p in pages),'PDF lacks expected text: '+gid)
            total_pages+=len(pages)
        require(all(1<=p<=meta['pdf_pages']['materials'] for p in meta['first_session_material_pages']),'Invalid first print pages')
        cards=json.loads((game/meta['files']['cards_data']).read_text(encoding='utf-8'))
        require(len(cards)==len({c['id'] for c in cards}),'Duplicate card IDs: '+gid);total_cards+=len(cards)
        for asset in meta.get('assets',[]):require((game/asset).is_file(),'Missing asset: '+asset)
        archive=inside(entry['download']);require(archive.is_file(),'Missing ZIP: '+gid)
        with ZipFile(archive) as z:
            require(z.testzip() is None,'Corrupt ZIP: '+gid)
            if meta.get('builder'):
                config=meta['builder'];folder=config['working_directory_name']
                for original,relative in config['outputs'].items():
                    # Markdown line endings in old download kits may be CRLF.
                    bundled=z.read(folder+'/'+original);local=(game/relative).read_bytes()
                    if Path(relative).suffix in {'.md','.py','.json'}:
                        bundled=bundled.replace(b'\r\n',b'\n');local=local.replace(b'\r\n',b'\n')
                    require(bundled==local,'Stale ZIP content: '+gid+' '+original)
    directory_ids={p.name for p in (ROOT/'games').iterdir() if p.is_dir()}
    require(directory_ids==seen,'Unregistered game directory')
    print(f'Validated {len(seen)} games, {total_pages} PDF pages, {total_cards} unique cards and matching ZIPs')

def hashes(write=False):
    files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.name!='SHA256SUMS.txt']
    content='\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix() for p in files)+'\n'
    path=ROOT/'SHA256SUMS.txt'
    if write:path.write_text(content,encoding='utf-8',newline='\n');print('Updated SHA256SUMS.txt')
    elif path.exists():require(path.read_text(encoding='utf-8')==content,'File hashes changed; run check_library.py --write-hashes')

if __name__=='__main__':
    check();hashes('--write-hashes' in sys.argv)
