/* Same units and default TMP105 resolution as the documented QEMU/driver path.
 * References: content/flight-studio/infrastructure-evidence.json.
 * This module calculates an explanatory model; it never contacts an emulator. */
export function sampleTemperature({initial=23.5,amplitude=5,period=30,time=5,mode='sine'}={}) {
  return mode==='constant'?initial:initial+amplitude*Math.sin(2*Math.PI*time/period);
}
export function toMilliCelsius(celsius) {
  const scaled=celsius*1000,lower=Math.floor(scaled),fraction=scaled-lower;
  // Python round(), used by the actual sender, rounds halfway cases to even.
  return fraction<.5?lower:fraction>.5?lower+1:lower%2===0?lower:lower+1;
}
export function tmp105Reading(milliCelsius) {
  const fixed=Math.trunc(milliCelsius*256/1000);
  return Math.floor(fixed/128)*.5 || 0;
}
export function buildDeviceArguments({temperature=true,magnetometer=true,address='0x48'}={}) {
  if(!/^0x4[89ab]$/.test(address)) throw new RangeError('Unsupported example address');
  const args=['-M raspi4b'];
  if(temperature) args.push(`-device tmp105,id=tmp105,bus=i2c-bus.1,address=${address}`);
  if(magnetometer) args.push('-device lsm303dlhc_mag,id=lsm303dlhc_mag,bus=i2c-bus.1,address=0x1e');
  return args.join('\n');
}
