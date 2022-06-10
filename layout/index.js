import { DataLoader } from './modules/data-loader.js';
import { Store } from './modules/instruction.js';

const data = await DataLoader("lego.json").load();
const store = Store(data);


const s = document.querySelector("#search");
const g = document.querySelector("#grid");

g.list = store.all();

s.addEventListener('search', (e) => {console.log(e.detail)}, false);

