/**
 * Data fetcher 
 */
export const DataLoader = (path) => {
  let loading = false, 
    error = false,
    data = [];

  return {
    async load() {
      if (!path) {
        return [];
      }
      
      try {
        loading = true;
        data = await (await fetch(path)).json();
      } catch (e) {
        error = true;
      }

      loading = false;
      return Array.isArray(data) ? data : []; 
    },

    get data() {
      return data;
    },

    get loading() {
      return loading;
    },

    get error() {
      return error;
    }
  }
}

window.SARCAZZO = "ciao";