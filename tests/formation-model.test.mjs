import {test} from 'node:test';
import assert from 'node:assert/strict';
import {FormationEngine} from '../src/formation-model.mjs';

test('formation analytic Jacobians agree with numerical derivatives away from the initial state',()=>{
  const e = new FormationEngine();
  for (const dyn of ['lin','nl']) {
    let x = e.setup(dyn).X0;
    for (let k=0;k<18;k++) x=e.rk4(dyn,x,5);
    const jac=e.jac(dyn,x);
    for(let j=0;j<x.length;j++) {
      const h=Math.max(Math.abs(x[j])*1e-5,j>=8?1e-9:1e-4);
      const a=x.slice(),b=x.slice();a[j]+=h;b[j]-=h;
      const fa=e.fdyn(dyn,a),fb=e.fdyn(dyn,b);
      for(let i=0;i<x.length;i++) {
        const numeric=(fa[i]-fb[i])/(2*h);
        assert.ok(Math.abs(numeric-jac[i][j])<1e-7+Math.abs(numeric)*2e-5,`${dyn} ${i},${j}: ${numeric} != ${jac[i][j]}`);
      }
    }
  }
});

test('orbital propagation conserves leader energy and exposes the original below-surface perigee',()=>{
  const e=new FormationEngine(), c=e.C(), initial=e.setup('nl').X0;
  const energy=x=>(x[7]**2+(x[6]*x[9])**2)/2-c.MU/x[6];
  const orbit=e.orbit('nl');
  for(const x of orbit.pts) assert.ok(Math.abs((energy(x)-energy(initial))/energy(initial))<2e-8);
  assert.ok(Math.abs(initial[6]-c.RE+97814)<1e-6);
  assert.ok(orbit.dmin>100000 && orbit.dmax>orbit.dmin);
});

test('seeded EKF is finite for all 24 noise/trust/model combinations and new noise preserves truth',()=>{
  const e=new FormationEngine();
  const truthByModel=new Map();
  for(const dyn of ['lin','nl']) for(const r of [5,10*Math.SQRT2,2000,20000]) for(const q of [.01,1,25]) {
    const out=e.ekf(dyn,r,q,1);
    if (!truthByModel.has(dyn)) truthByModel.set(dyn,out.tru);
    assert.deepEqual(out.tru,truthByModel.get(dyn),`${dyn}: noise and trust preserve the physical trajectory`);
    for(const key of ['rm','re','K','sig','inside'])assert.ok(Number.isFinite(out[key]),`${dyn}/${r}/${q}/${key}`);
    assert.ok(out.sg.every(v=>v>0));
    assert.ok(out.re<out.rm,`${dyn}/${r}/${q}: filter reduces truth-relative RMS`);
    assert.ok(out.inside>=0&&out.inside<=1);
  }
  const first=e.ekf('lin',10*Math.SQRT2,1,1),repeat=e.ekf('lin',10*Math.SQRT2,1,1),next=e.ekf('lin',10*Math.SQRT2,1,2);
  assert.deepEqual(first.mea,repeat.mea);assert.notDeepEqual(first.mea,next.mea);
  assert.deepEqual(first.tru,next.tru);assert.equal(first.t[0],0);assert.equal(first.t[1],5);
  assert.ok(Object.keys(e._runs).length<=6);
});

test('the separate course controller saturates at 50 N, accumulates windup and settles near one metre',()=>{
  const e=new FormationEngine(),ideal=e.servo(false),limited=e.servo(true);
  assert.ok(ideal.peak>66&&ideal.peak<68);
  assert.ok(limited.U.every(u=>Math.abs(u)<=50));
  assert.ok(limited.ask>ideal.ask);
  assert.ok(limited.zmax>ideal.zmax);
  assert.ok(Math.abs(limited.zend-1)<.002);
});
