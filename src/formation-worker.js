import {FormationEngine} from './formation-model.mjs';
const engine = new FormationEngine();
self.onmessage = ({data: {id, state}}) => {
  try {
    engine.state = state;
    self.postMessage({id, values: engine.renderVals()});
  } catch {
    self.postMessage({id, error: true});
  }
};
