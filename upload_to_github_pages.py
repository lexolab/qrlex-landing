import os, json, base64, subprocess, sys

ROOT = '/home/ubuntu/.openclaw/workspace/qrlex-landing'
OWNER = 'lexolab'
REPO = 'qrlex-landing'

FILES = sorted([
    f for f in os.listdir(ROOT)
    if os.path.isfile(os.path.join(ROOT, f))
    and not f.startswith('.')
    and f not in {'upload_to_github_pages.py'}
])

TEXT_EXTS = {'.html', '.css', '.js', '.txt', '.md', '.json', '.svg', '.xml'}

for name in FILES:
    path = os.path.join(ROOT, name)
    ext = os.path.splitext(name)[1].lower()
    if ext in TEXT_EXTS:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        with open(path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('ascii')

    payload = {
        'owner': OWNER,
        'repo': REPO,
        'path': name,
        'message': f'Add {name}',
        'content': content,
        'branch': 'main',
    }
    payload_path = os.path.join(ROOT, f'.payload_{name}.json')
    with open(payload_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f)

    print(f'Uploading {name} ...')
    result = subprocess.run([
        'composio', 'execute', 'GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS',
        '-d', '@' + payload_path
    ], text=True, capture_output=True)
    print(result.stdout[-600:] if result.stdout else '')
    if result.returncode != 0:
        print('STDERR:', result.stderr[-300:], file=sys.stderr)
        sys.exit(result.returncode)

print('\n✅ All files uploaded.')
