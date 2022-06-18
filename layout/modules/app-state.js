import Fuse from 'https://cdn.jsdelivr.net/npm/fuse.js@6.6.2/dist/fuse.esm.js'
import { State } from './state.js';

export const AppState = () => {
  let client = new Fuse([], {
    includeScore: true,
    keys: ["code", "family", "name"],
  });

  const { state, subscribe } = State({
    loading: false,
    searchText: "",
    list: [],
    filtered: [],
  });

  subscribe("list", (e) => {
    const { list, state } = e.detail;
    client.setCollection(list);
    state.filtered = filter(client, state.searchText, list);
  });

  subscribe("searchText", (e) => {
    const { searchText, state } = e.detail;
    state.filtered = filter(client, searchText, state.list);
  });

  return { state, subscribe };
};

/**
 * Normalize search results 
 */
const filter = (client, search, full) => {
  const result = client.search(search).map(r => r.item);
  return !result || result.length == 0 ? full : result
}