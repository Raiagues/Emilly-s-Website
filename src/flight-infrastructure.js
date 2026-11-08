import {sampleTemperature,toMilliCelsius,tmp105Reading,buildDeviceArguments} from './flight-infrastructure-model.mjs';
const root=document.querySelector('.flight-infra');
if(root) {
 const config=JSON.parse(document.getElementById('engineering-data').textContent).infrastructure;
 const params={initial:23.5,amplitude:5,period:30,time:5,mode:'sine'};
 const inputs=[...root.querySelectorAll('[data-fs-param]')];
 const nodes=[...root.querySelectorAll('[data-fs-node]')];
 const explanations=[...root.querySelectorAll('[data-fs-explain]')];
 const route=root.querySelector('[data-fs-route]');
 const wires=root.querySelector('[data-fs-wires]');
 const pathsGroup=wires.querySelector('[data-fs-paths]');
 const traveller=wires.querySelector('[data-fs-traveller]');
 const follow=root.querySelector('[data-fs-follow]');
 const next=root.querySelector('[data-fs-next]');
 const temperatureSwitch=root.querySelector('[data-fs-device="tmp105"]');
 const magnetSwitch=root.querySelector('[data-fs-device="mag"]');
 const address=root.querySelector('[data-fs-address]');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 let stage=0,timeout=null,animation=null,paths=[];
 const svgNS='http://www.w3.org/2000/svg';
 const value=()=>sampleTemperature(params);
 const reading=()=>tmp105Reading(toMilliCelsius(value()));
 const point=(temperature,time)=>({x:45+time*8,y:165-temperature*3});
 function stop() {
   clearTimeout(timeout);timeout=null;cancelAnimationFrame(animation);animation=null;
   traveller.setAttribute('hidden','');
   follow.textContent='▶ '+follow.dataset.startLabel;follow.setAttribute('aria-pressed','false');
 }
 function choose(index) {
   stage=Math.max(0,Math.min(7,index));
   nodes.forEach((node,i)=>{node.setAttribute('aria-pressed',String(i===stage));node.classList.toggle('is-passed',i<stage);});
   explanations.forEach((panel,i)=>panel.hidden=i!==stage);
   paths.forEach((path,i)=>path.classList.toggle('is-passed',i<stage));
 }
 function geometry() {
   const box=route.getBoundingClientRect();
   wires.setAttribute('viewBox',`0 0 ${box.width} ${box.height}`);
   pathsGroup.replaceChildren();paths=[];
   for(let i=0;i<nodes.length-1;i++) {
     const a=nodes[i].getBoundingClientRect(),b=nodes[i+1].getBoundingClientRect();
     let x1,y1,x2,y2,pathData;
     const sameRow=Math.abs(a.top-b.top)<a.height*.65;
     if(sameRow && b.left>a.right) {
       x1=a.right-box.left;y1=a.top+a.height/2-box.top;x2=b.left-box.left;y2=b.top+b.height/2-box.top;
       const middle=(x1+x2)/2;pathData=`M${x1} ${y1} C${middle} ${y1} ${middle} ${y2} ${x2} ${y2}`;
     } else if(i===1 && innerWidth>760) {
       x1=a.right-box.left;y1=a.top+a.height/2-box.top;x2=b.left-box.left;y2=b.top+b.height/2-box.top;
       pathData=`M${x1} ${y1} C${x1+25} ${y1} ${x2-30} ${y2} ${x2} ${y2}`;
     } else if(i===6 && innerWidth>760) {
       x1=a.right-box.left;y1=a.top+a.height/2-box.top;x2=b.left-box.left;y2=b.top+b.height/2-box.top;
       pathData=`M${x1} ${y1} C${x1+25} ${y1} ${x2-25} ${y2} ${x2} ${y2}`;
     } else {
       x1=a.left+a.width/2-box.left;y1=a.bottom-box.top;x2=b.left+b.width/2-box.left;y2=b.top-box.top;
       const middle=(y1+y2)/2;pathData=`M${x1} ${y1} C${x1} ${middle} ${x2} ${middle} ${x2} ${y2}`;
     }
     const path=document.createElementNS(svgNS,'path');path.setAttribute('d',pathData);path.dataset.fsPath=String(i);pathsGroup.append(path);paths.push(path);
   }
   choose(stage);
 }
 function renderSignal() {
   const sample=value(),read=reading(),enabled=temperatureSwitch.checked;
   const points=[];
   for(let time=0;time<=60;time+=.25){const p=point(sampleTemperature({...params,time}),time);points.push(`${p.x.toFixed(2)},${p.y.toFixed(2)}`);}
   root.querySelector('[data-fs-wave]').setAttribute('points',points.join(' '));
   const p=point(sample,params.time);
   root.querySelector('[data-fs-wave-guide]').setAttribute('d',`M${p.x} 30V165`);
   root.querySelector('[data-fs-wave-dot]').setAttribute('cx',p.x);root.querySelector('[data-fs-wave-dot]').setAttribute('cy',p.y);
   root.querySelector('[data-fs-time]').textContent=params.time.toFixed(2)+' s';
   root.querySelector('[data-fs-source-value]').textContent=sample.toFixed(3)+' °C';
   root.querySelector('[data-fs-read-value]').textContent=enabled?read.toFixed(1)+' °C':'—';
   root.querySelector('[data-fs-driver-value]').textContent=enabled?read.toFixed(1)+' °C':'—';
   root.querySelectorAll('[data-fs-node-value]').forEach(output=>{
     output.textContent=output.dataset.fsNodeValue==='sample'?sample.toFixed(3)+' °C':enabled?read.toFixed(1)+' °C':'—';
   });
   root.querySelectorAll('[data-fs-readout]').forEach(output=>{const key=output.dataset.fsReadout;output.textContent=params[key]+(key==='period'?' s':' °C');});
   const code=root.querySelector('.fs-function code');
   code.textContent=params.mode==='constant'?'def sample(seconds, initial_c):\n    return initial_c':`def sample(seconds, initial_c):\n    return initial_c + ${params.amplitude} * sin(\n        2 * pi * seconds / ${params.period}\n    )`;
   inputs.filter(input=>['amplitude','period'].includes(input.dataset.fsParam)).forEach(input=>input.disabled=params.mode==='constant');
   root.querySelector('[data-fs-status]').textContent=enabled?`${config.status} ${params.time.toFixed(2)} s · ${sample.toFixed(3)} °C`:config.missing;
 }
 function renderBoard() {
   const enabled=temperatureSwitch.checked;
   follow.disabled=!enabled;next.disabled=!enabled;address.disabled=!enabled;
   root.querySelector('[data-fs-qemu-args]').textContent=buildDeviceArguments({temperature:enabled,magnetometer:magnetSwitch.checked,address:address.value});
   root.querySelector('[data-board-address]').textContent=address.value;
   root.querySelector('[data-board-devicegroup="sensor"]').classList.toggle('is-off',!enabled);
   root.querySelector('[data-fs-magnet]').hidden=!magnetSwitch.checked;
   nodes[2].querySelector('strong').textContent='TMP105 · I²C '+address.value;
   nodes[2].classList.toggle('is-disconnected',!enabled);
   renderSignal();
 }
 function advance() {
   if(stage===7){stop();return;}
   const path=paths[stage],destination=stage+1;
   if(reduced.matches||!path) {
     choose(destination);timeout=setTimeout(advance,1000);return;
   }
   const start=performance.now(),length=path.getTotalLength();
   traveller.removeAttribute('hidden');
   traveller.querySelector('text').textContent=(destination>=4?reading().toFixed(1):value().toFixed(3))+' °C';
   const move=now=>{
     const progress=Math.min(1,(now-start)/700),p=path.getPointAtLength(length*progress);
     traveller.setAttribute('transform',`translate(${p.x} ${p.y})`);
     const flip=p.x>route.clientWidth-100;
     traveller.querySelector('rect').setAttribute('x',flip?-95:10);
     traveller.querySelector('text').setAttribute('x',flip?-89:16);
     if(progress<1)animation=requestAnimationFrame(move);
     else {animation=null;traveller.setAttribute('hidden','');choose(destination);timeout=setTimeout(advance,600);}
   };
   animation=requestAnimationFrame(move);
 }
 nodes.forEach((node,i)=>{node.disabled=false;node.addEventListener('click',()=>{stop();choose(i);});});
 follow.addEventListener('click',()=>{
   if(timeout!==null||animation!==null){stop();return;}
   if(stage===7)choose(0);
   follow.textContent='Ⅱ '+follow.dataset.pauseLabel;follow.setAttribute('aria-pressed','true');
   timeout=setTimeout(advance,150);
 });
 next.addEventListener('click',()=>{stop();choose((stage+1)%8);});
 root.querySelector('[data-fs-reset]').addEventListener('click',()=>{stop();choose(0);});
 inputs.forEach(input=>input.addEventListener('input',()=>{
   const key=input.dataset.fsParam;params[key]=key==='mode'?input.value:Number(input.value);
   stop();choose(0);renderSignal();
 }));
 [temperatureSwitch,magnetSwitch,address].forEach(input=>input.addEventListener('change',()=>{stop();choose(0);renderBoard();}));
 function selection(buttonAttr,panelAttr,initial=0) {
   const buttons=[...root.querySelectorAll(`[${buttonAttr}]`)],panels=[...root.querySelectorAll(`[${panelAttr}]`)];
   const select=index=>{
     buttons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
     panels.forEach((panel,i)=>panel.hidden=i!==index);
     if(buttonAttr==='data-fs-part') root.querySelectorAll('[data-storage-region]').forEach(node=>node.classList.toggle('is-selected',Number(node.dataset.storageRegion)===index));
   };
   buttons.forEach((button,i)=>button.addEventListener('click',()=>select(i)));select(initial);
 }
 selection('data-fs-part','data-fs-part-detail',1);selection('data-fs-driver','data-fs-driver-detail');
 root.querySelectorAll('[data-fs-controls]').forEach(control=>control.hidden=false);
 renderBoard();choose(0);geometry();new ResizeObserver(geometry).observe(route);
 document.fonts.ready.then(geometry);
 document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
 reduced.addEventListener('change',stop);
 window.addEventListener('pagehide',stop);
}
