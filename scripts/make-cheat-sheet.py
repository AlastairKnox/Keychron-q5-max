from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from pypdf import PdfReader
out=Path(__file__).resolve().parents[1]/'docs';out.mkdir(exist_ok=True)
for name,file in [('Desk','DejaVuSans.ttf'),('DeskBold','DejaVuSans-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
W,H=210*mm,148*mm
c=canvas.Canvas(str(out/'cheat-sheet.pdf'),pagesize=(W,H))
c.setTitle('Keychron Q5 Max - Custom Linux desk card')
c.setAuthor('Alastair Knox')
ink=HexColor('#172c36');accent=HexColor('#176c6a');muted=HexColor('#46545c');rule=HexColor('#d3dcde')
def text(x,y,s,size=12,bold=False,color=ink):
 c.setFillColor(color);c.setFont('DeskBold' if bold else 'Desk',size);c.drawString(x,y,s)
text(20,H-32,'Q5 MAX',25,True)
text(157,H-31,'CUSTOM LINUX',14,True,accent)
text(20,H-54,'Fn + Space  enters / leaves Linux mode',15,True)
text(20,H-72,'Standard Mac / Windows layouts remain on the rear switch.',10.2,color=muted)
c.setStrokeColor(rule);c.line(20,H-85,W-20,H-85)
xs=[20,213,406];cw=169
for x,title in zip(xs,['TYPING MACROS','EDIT & KNOB','CLIPBOARD & APPS']):text(x,H-106,title,12,True,accent)
cols=[[
 ('Fn + L / Butterfly + L','ls -ltr + Enter'),
 ('Fn + P / Butterfly + P','ps auxw|more + Enter'),
 ('Fn + H / Butterfly + H','history + Enter'),
 ('Fn + D','Type ../'),
 ('Fn + M','Thanks, [new line] Alastair.'),
 ('Fn + R, then release','Start recording a macro'),
 ('Fn + S','Stop recording'),
 ('Fn + O, then release','Replay recorded macro'),
], [
 ('Tap left / right Shift','(  /  )   Hold for Shift'),
 ('Shift + Backspace','Forward Delete'),
 ('Fn + A','Autocorrect on / off'),
 ('Fn + C','Caps Word on / off'),
 ('Fn + PgUp / PgDn','Home / End'),
 ('Turn clockwise / back','Volume up / down'),
 ('Press knob','Mute / unmute'),
 ('Fn + turn knob','Scroll down / up'),
], [
 ('Triangle','Copy: Ctrl + Shift + C'),
 ('Square','Paste: Ctrl + Shift + V'),
 ('Butterfly + Triangle','Copy: Ctrl + C'),
 ('Butterfly + Square','Paste: Ctrl + V'),
 ('Circle','Open terminal'),
 ('Fn + Pad 0 / Butterfly + Pad 0','Open calculator'),
 ('Fn + Circle','Select word; +Shift: line'),
 ('Butterfly means LEFT','The key immediately before Space'),
]]
for x,rows in zip(xs,cols):
 for i,(key,action) in enumerate(rows):
  y=H-129-i*25
  keysize=11.4
  while pdfmetrics.stringWidth(key,'DeskBold',keysize)>cw:keysize-=.2
  text(x,y,key,keysize,True)
  size=10.5
  while pdfmetrics.stringWidth(action,'Desk',size)>cw:size-=.2
  text(x,y-14,action,size,color=muted)
for x in [201,394]:
 c.setStrokeColor(rule);c.line(x,H-100,x,66)
c.setStrokeColor(rule);c.line(20,61,W-20,61)
text(20,44,'ESC: green = autocorrect ON   |   amber = OFF   |   red = recording',10.5,True)
text(20,28,'Fn + F3: overview   F4: apps   F5/6: lights   F7-12: media & volume',10.5)
text(20,13,'Autocorrect starts ON. Period types normally. Print A5 landscape at 100% / actual size.',8.5,color=muted)
c.showPage();c.save()
p=PdfReader(out/'cheat-sheet.pdf')
assert len(p.pages)==1
assert abs(float(p.pages[0].mediabox.width)-W)<1
print('Created one-page A5 landscape desk card:',out/'cheat-sheet.pdf')
