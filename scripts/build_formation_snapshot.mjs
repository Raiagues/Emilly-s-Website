// Maintenance helper only. The normal Python build uses the committed snapshot.
import {writeFileSync} from 'node:fs';
import {FormationEngine} from '../src/formation-model.mjs';
writeFileSync(new URL('../content/ita-formation/default.json',import.meta.url),JSON.stringify(new FormationEngine().renderVals())+'\n');
