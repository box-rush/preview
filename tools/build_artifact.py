"""Build Artifact fragments from repo prototypes (repo files are the single source).
usage: python3 build.py <repo-file> <out-file> [rel=url ...]"""
import re,sys
src,out,*maps=sys.argv[1:]
s=open(src).read()
head=re.search(r'<head>(.*?)</head>',s,re.S).group(1)
body=re.search(r'<body>(.*)</body>',s,re.S).group(1)
head=re.sub(r'<meta[^>]*>\s*','',head)
head=re.sub(r'<!--.*?-->\s*','',head,flags=re.S)
frag=head.strip()+"\n"+body.strip()+"\n"
for m in maps:
    rel,url=m.split('=',1); frag=frag.replace(rel,url)
open(out,'w').write(frag)
print(out,len(frag))
