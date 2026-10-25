from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
old=root/'verification/original_autocorrect_data.h'
new=root/'keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair/autocorrect_data.h'
def rules(path):return re.findall(r'^//\s+(\S+)\s+->\s+(.+)$',path.read_text(),re.M)
assert rules(new)==[r for r in rules(old) if r!=('erested','arrested')]
def simulate(path,text):
 s=path.read_text();data=[int(x,16) for x in re.findall(r'0x([0-9a-fA-F]{2})',s.split('PROGMEM = {')[1])]
 buf=[];out=''
 for char in text:
  key=ord(char)-ord('a')+4 if char.isalpha() else 44
  buf=(buf+[key])[-19:];state=0;code=data[0];match=None
  if len(buf)>=5:
   for k in reversed(buf):
    if code&64:
     code&=63
     while code!=k:
      state+=3;code=data[state]
      if not code:break
     if not code:break
     state=data[state+1]|data[state+2]<<8
    elif code!=k:break
    else:
     state+=1
     if data[state]==0:state+=1
    code=data[state]
    if code&128:
     end=data.index(0,state+1)
     match=(code&63,bytes(data[state+1:end]).decode());break
  if match:
   n,change=match;out=(out[:-n] if n else out)+change
   buf=[44] if key==44 else []
   if key==44:out+=char
  else:out+=char
 return out
assert simulate(old,'interested ')=='intarrested '
for word in ['interested ','uninterested ','disinterested ']:assert simulate(new,word)==word,(word,simulate(new,word))
assert simulate(new,'intrest ')=='interest '
assert simulate(new,'abotu ')=='about '
print('PASS: reproduced interested -> intarrested in old serialized dictionary; corrected dictionary preserves interested/uninterested/disinterested and still corrects intrest/abotu.')
