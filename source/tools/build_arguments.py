"""Lossless, hash-bound JSON argv transport for long native command lines."""
import json
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash

def validate(value):
    if type(value) is not dict or set(value)!={'schema','args'} or type(value['schema']) is not int or value['schema']!=1 or type(value['args']) is not list or any(type(s) is not str or '\0' in s for s in value['args']):raise ValueError('Build argument manifest schema')
    return value['args']

def save(path,args):
    value=dict(schema=1,args=args);validate(value)
    data=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.read_bytes()!=data:raise ValueError('Preserve frozen build arguments')
    if not path.exists():path.write_bytes(data)
    return sha(data)

def expand(argv):
    if not argv or argv[0]!='--argument-file':return argv,None
    if len(argv)!=4 or argv[2]!='--argument-file-sha256':raise ValueError('Exclusive hash-bound argument-file invocation')
    path=ROOT/argv[1];require_hash(path,argv[3]);data=path.read_bytes();args=validate(json.loads(data.decode('utf8')))
    if '--argument-file' in args:raise ValueError('Nested build argument files forbidden')
    return args,dict(path=str(path.resolve().relative_to(ROOT)),sha256=sha(data))
