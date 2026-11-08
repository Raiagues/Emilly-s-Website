import {test} from 'node:test';
import assert from 'node:assert/strict';
import {sampleTemperature,toMilliCelsius,tmp105Reading,buildDeviceArguments} from '../src/flight-infrastructure-model.mjs';
test('synthetic waveform reproduces the source and exposes amplitude, baseline, period and constant mode',()=>{
 assert.equal(sampleTemperature({time:0}),23.5);
 assert.equal(sampleTemperature({time:7.5}),28.5);
 assert.equal(sampleTemperature({time:22.5}),18.5);
 assert.equal(toMilliCelsius(sampleTemperature({time:5})),27830);
 assert.equal(sampleTemperature({initial:24,amplitude:8,period:60,time:15}),32);
 assert.equal(sampleTemperature({initial:19,mode:'constant',time:16}),19);
});
test('temperature conversion preserves Python rounding and the actual TMP105 default resolution',()=>{
 for(const [c,milli] of [[.0005,0],[.0015,2],[.0025,2],[-.0005,0],[-.0015,-2]])assert.equal(toMilliCelsius(c),milli);
 for(const [milli,c] of [[27830,27.5],[28500,28.5],[0,0],[-1,0],[-4,-.5],[-501,-.5],[-504,-1]])assert.equal(tmp105Reading(milli),c);
});
test('board topology generates only enabled devices with the chosen address',()=>{
 assert.equal(buildDeviceArguments({temperature:false,magnetometer:false}),'-M raspi4b');
 assert.match(buildDeviceArguments({address:'0x49',magnetometer:false}),/tmp105,id=tmp105,bus=i2c-bus\.1,address=0x49$/);
 assert.doesNotMatch(buildDeviceArguments({magnetometer:false}),/lsm303/);
 assert.throws(()=>buildDeviceArguments({address:'unexpected'}),RangeError);
});
