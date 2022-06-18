import { DataLoader } from './modules/data-loader.js';
import { Instructions } from './modules/instruction.js';
import { AppState } from './modules/app-state.js';

const { state, subscribe } = AppState();
const data = await DataLoader("lego.json").load();
const instructions = Instructions(data);

const s = document.querySelector("#search");
const g = document.querySelector("#grid");

state.list = instructions.all();

s.addEventListener('query', (e) => {
  state.searchText = e.detail.query;
}, false);

subscribe('filtered', (e) => {
  g.list = e.detail.filtered;
})






