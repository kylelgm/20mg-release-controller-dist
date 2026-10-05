#!/usr/bin/env python3
"""Owner-side assembly; never executes or extracts archive-provided code."""
import gzip
import hashlib
import io
import json
import pathlib
import sys
import tarfile
import zipfile

FULL = 'c99e36c06609f8157fb9a360ae4ec19e0f09aef836518c920e8705fb35c17eaa'
OP = '74277219e8da60958c00f9aee9d2023225e98fdda8bfd2156a5d9e85e0edaab3'
RAW = 'd858c5cc2b5632d0db8f6a4d5730060336202dbfba77fa8ed27938f5f27add9d'
CAPSULE = 'de3640b29e7a529720db777563da8d71add362b2fcbf039ddbc8aa6fb07784eb'

def require(condition):
    if not condition:
        raise SystemExit('Installer assembly verification failed; nothing installed')

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

require(len(sys.argv) == 4)
capsule, op_zip, output = map(pathlib.Path, sys.argv[1:])
require(not output.exists() and digest(capsule) == CAPSULE and digest(op_zip) == OP)
with tarfile.open(capsule, 'r:gz') as archive:
    members = archive.getmembers()
    require(len(members) == 2 and {m.name for m in members} == {'base.tar', 'recipe.json'})
    require(all(m.isfile() and not m.issym() and not m.islnk() for m in members))
    require(archive.getmember('recipe.json').size <= 4096)
    require(archive.getmember('base.tar').size <= 300 * 1024 * 1024)
    recipe = json.loads(archive.extractfile('recipe.json').read())
    base = archive.extractfile('base.tar').read()
require(recipe['schema'] == 1 and recipe['originalTarSha256'] == RAW and recipe['originalGzipSha256'] == FULL)
require(recipe['baseBytes'] == len(base) and recipe['originalTarBytes'] <= 350 * 1024 * 1024)
require([s['name'] for s in recipe['spans']] == ['op', 'op.sig'])
pieces = []
previous = 0
with zipfile.ZipFile(op_zip) as archive:
    for span in recipe['spans']:
        offset, length = span['baseOffset'], span['length']
        require(isinstance(offset, int) and previous <= offset <= len(base))
        require(isinstance(length, int) and 0 < length <= 50 * 1024 * 1024)
        info = archive.getinfo(span['name'])
        require(info.file_size == length and not info.is_dir())
        pieces.extend([base[previous:offset], archive.read(info)])
        previous = offset
pieces.append(base[previous:])
original = b''.join(pieces)
require(len(original) == recipe['originalTarBytes'] and hashlib.sha256(original).hexdigest() == RAW)
# Gzip metadata and compression settings reproduce the already-reviewed bundle.
# Any platform-dependent compression difference fails the full bundle digest.
with output.open('xb') as f, gzip.GzipFile(filename='', mode='wb', fileobj=f, mtime=0) as compressed:
    compressed.write(original)
if digest(output) != FULL:
    output.unlink()
    raise SystemExit('Exact reviewed bundle could not be reconstructed; nothing installed')
print('Exact reviewed enrollment-only bundle verified')
