import re

with open('padel-tracker.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find start of TACTICS BOARD JS section
start_marker = '// ═══════════════════════════════════════════════════════════════\n// TACTICS BOARD\n// ═══════════════════════════════════════════════════════════════'
end_marker = '</script>\n</body>\n</html>'

start_idx = content.find(start_marker)
end_idx = content.rfind(end_marker)

if start_idx < 0 or end_idx < 0:
    print(f'ERROR: start={start_idx}, end={end_idx}')
    exit(1)

new_js = r"""// ═══════════════════════════════════════════════════════════════
// TACTICS BOARD
// ═══════════════════════════════════════════════════════════════
const CW=320, CH=560, PX=30, PT=20, PB=20;
const IW=CW-PX*2, IH=CH-PT-PB;
const MID_Y=PT+IH/2;
const R=18, BR=10;

const formations={
  paralelas: {A1:[0.25,0.78],A2:[0.75,0.78],B1:[0.25,0.22],B2:[0.75,0.22],ball:[0.5,0.5]},
  diagonales:{A1:[0.15,0.82],A2:[0.82,0.68],B1:[0.82,0.18],B2:[0.15,0.32],ball:[0.5,0.5]},
  defensa:   {A1:[0.22,0.92],A2:[0.78,0.92],B1:[0.28,0.32],B2:[0.72,0.32],ball:[0.5,0.72]},
  ataque:    {A1:[0.28,0.58],A2:[0.72,0.58],B1:[0.28,0.12],B2:[0.72,0.12],ball:[0.5,0.35]},
  globo:     {A1:[0.22,0.88],A2:[0.78,0.88],B1:[0.28,0.55],B2:[0.72,0.55],ball:[0.35,0.75]},
  bandeja:   {A1:[0.3,0.62], A2:[0.7,0.62], B1:[0.25,0.15],B2:[0.75,0.15],ball:[0.4,0.42]},
  contrapie: {A1:[0.72,0.75],A2:[0.28,0.88],B1:[0.25,0.22],B2:[0.75,0.28],ball:[0.5,0.55]}
};

let pos={}, arrows=[], mode='move', arrowColor='#1d6fa4';
let dragging=null, dragOffX=0, dragOffY=0;
let arrowStart=null, previewEnd=null;

function px(rx){ return PX+rx*IW; }
function py(ry){ return PT+ry*IH; }
function rx(x){ return Math.max(0,Math.min(1,(x-PX)/IW)); }
function ry(y){ return Math.max(0,Math.min(1,(y-PT)/IH)); }

function setF(name){
  document.querySelectorAll('.tb').forEach(b=>{
    const map={paralelas:'Paralelas',diagonales:'Diagonales',defensa:'Defensa',ataque:'Ataque red',globo:'Globo',bandeja:'Bandeja',contrapie:'Contrapie'};
    b.classList.toggle('active', b.textContent===map[name]);
  });
  pos=JSON.parse(JSON.stringify(formations[name]));
  redraw();
}

function setMode(m){
  mode=m;
  ['move','arrow','erase'].forEach(id=>{
    document.getElementById('mode-'+id).classList.toggle('active',m===id);
  });
  const c=document.getElementById('mainCanvas');
  c.style.cursor=m==='erase'?'not-allowed':'crosshair';
}

function setArrowColor(c,btnId){
  arrowColor=c;
  document.querySelectorAll('.color-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(btnId).classList.add('active');
}

function clearArrows(){ arrows=[]; redraw(); }

function redraw(){
  const canvas=document.getElementById('mainCanvas');
  const ctx=canvas.getContext('2d');
  ctx.clearRect(0,0,CW,CH);
  drawCourt(ctx);
  arrows.forEach(a=>drawArrow(ctx,px(a.x1),py(a.y1),px(a.x2),py(a.y2),a.color,false));
  if(previewEnd&&arrowStart) drawArrow(ctx,arrowStart.x,arrowStart.y,previewEnd.x,previewEnd.y,arrowColor,true);
  drawBall(ctx);
  ['A1','A2'].forEach(id=>drawPlayer(ctx,id,'#1d6fa4'));
  ['B1','B2'].forEach(id=>drawPlayer(ctx,id,'#993c1d'));
}

function drawCourt(ctx){
  ctx.fillStyle='#2d5a3d';
  ctx.beginPath(); ctx.roundRect(PX,PT,IW,IH,4); ctx.fill();
  ctx.strokeStyle='rgba(255,255,255,0.22)'; ctx.lineWidth=1.5;
  ctx.strokeRect(PX,PT,IW,IH);
  ctx.fillStyle='rgba(0,0,0,0.18)';
  ctx.fillRect(PX,PT,IW,10);
  ctx.fillRect(PX,PT+IH-10,IW,10);
  ctx.fillRect(PX,PT+10,10,IH-20);
  ctx.fillRect(PX+IW-10,PT+10,10,IH-20);
  ctx.strokeStyle='rgba(255,255,255,0.18)'; ctx.lineWidth=1;
  const q=IH/4;
  [[PX,PT+q,PX+IW,PT+q],[PX,PT+q*3,PX+IW,PT+q*3]].forEach(([x1,y1,x2,y2])=>{
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
  });
  [IW/3,IW*2/3].forEach(dx=>{
    ctx.beginPath(); ctx.moveTo(PX+dx,PT+q); ctx.lineTo(PX+dx,PT+q*3); ctx.stroke();
  });
  ctx.setLineDash([5,5]);
  ctx.beginPath();
  ctx.moveTo(PX+IW/2,PT); ctx.lineTo(PX+IW/2,PT+q);
  ctx.moveTo(PX+IW/2,PT+q*3); ctx.lineTo(PX+IW/2,PT+IH);
  ctx.stroke(); ctx.setLineDash([]);
  ctx.strokeStyle='rgba(255,255,255,0.7)'; ctx.lineWidth=3;
  ctx.beginPath(); ctx.moveTo(PX,MID_Y); ctx.lineTo(PX+IW,MID_Y); ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,0.35)';
  ctx.font='bold 9px Arial'; ctx.textAlign='center';
  ctx.fillText('RED',PX+IW/2,MID_Y-5);
  ctx.fillStyle='rgba(255,255,255,0.12)';
  ctx.font='9px Arial';
  ctx.fillText('FONDO',PX+IW/2,PT+7);
  ctx.fillText('FONDO',PX+IW/2,PT+IH-3);
}

function drawPlayer(ctx,id,fill){
  const [ex,ey]=pos[id];
  const x=px(ex), y=py(ey);
  const names={A1:'nA1',A2:'nA2',B1:'nB1',B2:'nB2'};
  const name=(document.getElementById(names[id])?.value||id).substring(0,7);
  ctx.fillStyle=fill;
  ctx.beginPath(); ctx.arc(x,y,R,0,Math.PI*2); ctx.fill();
  ctx.strokeStyle='rgba(255,255,255,0.8)'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.arc(x,y,R,0,Math.PI*2); ctx.stroke();
  ctx.fillStyle='white'; ctx.font='bold 9px Arial';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText(name.substring(0,5),x,y);
  ctx.textBaseline='alphabetic';
  const tw=ctx.measureText(name).width+12;
  ctx.fillStyle='rgba(0,0,0,0.65)';
  ctx.beginPath(); ctx.roundRect(x-tw/2,y+R+2,tw,15,4); ctx.fill();
  ctx.fillStyle='rgba(255,255,255,0.9)'; ctx.font='9px Arial';
  ctx.fillText(name,x,y+R+13);
}

function drawBall(ctx){
  const [ex,ey]=pos.ball;
  const x=px(ex), y=py(ey);
  ctx.fillStyle='#f4a226';
  ctx.beginPath(); ctx.arc(x,y,BR,0,Math.PI*2); ctx.fill();
  ctx.strokeStyle='#7a4f0a'; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.arc(x,y,BR,0,Math.PI*2); ctx.stroke();
  ctx.strokeStyle='rgba(255,255,255,0.45)'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.arc(x-2,y-2,4,Math.PI*0.8,Math.PI*1.8); ctx.stroke();
}

function drawArrow(ctx,x1,y1,x2,y2,color,dashed){
  const dx=x2-x1, dy=y2-y1, len=Math.sqrt(dx*dx+dy*dy);
  if(len<6) return;
  const ux=dx/len, uy=dy/len;
  ctx.strokeStyle=color; ctx.lineWidth=2.5;
  if(dashed) ctx.setLineDash([5,4]); else ctx.setLineDash([]);
  ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2-ux*9,y2-uy*9); ctx.stroke();
  ctx.setLineDash([]);
  const angle=Math.atan2(dy,dx);
  ctx.fillStyle=color;
  ctx.beginPath();
  ctx.moveTo(x2,y2);
  ctx.lineTo(x2-13*Math.cos(angle-0.38),y2-13*Math.sin(angle-0.38));
  ctx.lineTo(x2-13*Math.cos(angle+0.38),y2-13*Math.sin(angle+0.38));
  ctx.closePath(); ctx.fill();
}

function hitTest(mx,my){
  for(const id of ['A1','A2','B1','B2']){
    const [ex,ey]=pos[id];
    const dx=mx-px(ex), dy=my-py(ey);
    if(dx*dx+dy*dy<=(R+5)*(R+5)) return id;
  }
  const [bx,by]=pos.ball;
  const dx=mx-px(bx), dy=my-py(by);
  if(dx*dx+dy*dy<=(BR+6)*(BR+6)) return 'ball';
  return null;
}

function eraseArrowAt(mx,my){
  arrows=arrows.filter(a=>{
    const x1=px(a.x1),y1=py(a.y1),x2=px(a.x2),y2=py(a.y2);
    const dx=x2-x1,dy=y2-y1,len=Math.sqrt(dx*dx+dy*dy);
    if(len<1) return true;
    const t=Math.max(0,Math.min(1,((mx-x1)*dx+(my-y1)*dy)/(len*len)));
    return Math.sqrt((mx-(x1+t*dx))*(mx-(x1+t*dx))+(my-(y1+t*dy))*(my-(y1+t*dy)))>12;
  });
  redraw();
}

const tacCanvas=document.getElementById('mainCanvas');

tacCanvas.addEventListener('mousedown',e=>{
  const r=tacCanvas.getBoundingClientRect();
  const mx=(e.clientX-r.left)*(CW/r.width);
  const my=(e.clientY-r.top)*(CH/r.height);
  if(mode==='erase'){eraseArrowAt(mx,my);return;}
  if(mode==='arrow'){arrowStart={x:mx,y:my};return;}
  const hit=hitTest(mx,my);
  if(hit){dragging=hit;const [ex,ey]=pos[hit];dragOffX=mx-px(ex);dragOffY=my-py(ey);}
});

tacCanvas.addEventListener('mousemove',e=>{
  const r=tacCanvas.getBoundingClientRect();
  const mx=(e.clientX-r.left)*(CW/r.width);
  const my=(e.clientY-r.top)*(CH/r.height);
  if(mode==='arrow'&&arrowStart){previewEnd={x:mx,y:my};redraw();return;}
  if(!dragging) return;
  pos[dragging]=[rx(mx-dragOffX),ry(my-dragOffY)];
  redraw();
});

tacCanvas.addEventListener('mouseup',e=>{
  const r=tacCanvas.getBoundingClientRect();
  const mx=(e.clientX-r.left)*(CW/r.width);
  const my=(e.clientY-r.top)*(CH/r.height);
  if(mode==='arrow'&&arrowStart){
    const dx=mx-arrowStart.x,dy=my-arrowStart.y;
    if(Math.sqrt(dx*dx+dy*dy)>10) arrows.push({x1:rx(arrowStart.x),y1:ry(arrowStart.y),x2:rx(mx),y2:ry(my),color:arrowColor});
    arrowStart=null; previewEnd=null; redraw(); return;
  }
  dragging=null;
});

tacCanvas.addEventListener('touchstart',e=>{
  e.preventDefault();
  const r=tacCanvas.getBoundingClientRect();
  const t=e.touches[0];
  const mx=(t.clientX-r.left)*(CW/r.width);
  const my=(t.clientY-r.top)*(CH/r.height);
  if(mode==='arrow'){arrowStart={x:mx,y:my};return;}
  if(mode==='erase'){eraseArrowAt(mx,my);return;}
  const hit=hitTest(mx,my);
  if(hit){dragging=hit;const[ex,ey]=pos[hit];dragOffX=mx-px(ex);dragOffY=my-py(ey);}
},{passive:false});

tacCanvas.addEventListener('touchmove',e=>{
  e.preventDefault();
  const r=tacCanvas.getBoundingClientRect();
  const t=e.touches[0];
  const mx=(t.clientX-r.left)*(CW/r.width);
  const my=(t.clientY-r.top)*(CH/r.height);
  if(mode==='arrow'&&arrowStart){previewEnd={x:mx,y:my};redraw();return;}
  if(!dragging) return;
  pos[dragging]=[rx(mx-dragOffX),ry(my-dragOffY)];
  redraw();
},{passive:false});

tacCanvas.addEventListener('touchend',e=>{
  const r=tacCanvas.getBoundingClientRect();
  const t=e.changedTouches[0];
  const mx=(t.clientX-r.left)*(CW/r.width);
  const my=(t.clientY-r.top)*(CH/r.height);
  if(mode==='arrow'&&arrowStart){
    const dx=mx-arrowStart.x,dy=my-arrowStart.y;
    if(Math.sqrt(dx*dx+dy*dy)>10) arrows.push({x1:rx(arrowStart.x),y1:ry(arrowStart.y),x2:rx(mx),y2:ry(my),color:arrowColor});
    arrowStart=null;previewEnd=null;redraw();return;
  }
  dragging=null;
});

function exportImg(){
  const src=document.getElementById('mainCanvas');
  const note=document.getElementById('tactNote').value.trim();
  const nH=note?70:0;
  const exp=document.createElement('canvas');
  exp.width=CW; exp.height=CH+nH+28;
  const ctx=exp.getContext('2d');
  ctx.fillStyle='#1b4332'; ctx.fillRect(0,0,exp.width,exp.height);
  ctx.font='bold 11px Arial';
  ctx.fillStyle='rgba(255,255,255,0.45)'; ctx.textAlign='center';
  ctx.fillText('TACTICA PADEL PRO',CW/2,14);
  ctx.drawImage(src,0,18);
  if(note){
    ctx.fillStyle='rgba(0,0,0,0.3)'; ctx.fillRect(0,CH+18,CW,nH+10);
    ctx.fillStyle='rgba(255,255,255,0.8)'; ctx.font='11px Arial'; ctx.textAlign='left';
    const words=note.split(' '); let line='', y=CH+34;
    words.forEach(w=>{
      const test=line+w+' ';
      if(ctx.measureText(test).width>CW-18&&line!==''){ctx.fillText(line,9,y);line=w+' ';y+=15;}
      else line=test;
    });
    ctx.fillText(line,9,y);
  }
  const a=document.createElement('a');
  a.download='tactica-padel.png';
  a.href=exp.toDataURL('image/png');
  a.click();
}

setF('paralelas');"""

new_content = content[:start_idx] + new_js + '\n' + end_marker
with open('padel-tracker.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('OK - file written successfully')
print(f'New size: {len(new_content)} chars')
