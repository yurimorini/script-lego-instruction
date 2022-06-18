import { define } from 'https://unpkg.com/uce?module';

const t = {
  search: "✕",
  placeholder: "Cosa stai cercando ?"
}

define('ym-lego-search', {
  extends: "div",
  
  props: {
    query: "",
  },

  bound: [
    'clear', 'input', 'keydown'
  ],

  connected() {
    this.form = this.querySelector('form');
  },

  input(e) {
    e.preventDefault();
    this.query = e.target.value;

    this.dispatchEvent(new CustomEvent('query', { 
      detail: { query: this.query },
      bubbles: true
    }));
  },

  clear(e) {
    e.preventDefault();
    
    this.form.reset();
    this.query = "";
    
    this.dispatchEvent(new CustomEvent('query', { 
      detail: { query: this.query },
      bubbles: true
    }));
  },

  keydown(e) {
    if (e.keyCode == 13) {
      e.preventDefault();
    } else if (e.keyCode == 27) {
      this.clear(e);
    }
  },

  render() {
    this.html`
      <form class="search">

        <input 
          onkeydown="${this.keydown}"
          class="search__input"
          oninput=${this.input} 
          placeholder="${t.placeholder}"
          autocomplete="off"
          type="text" 
          name="search" 
          value="${this.query}" />

        <button 
          onclick="${this.clear}"
          class="search__button" 
          style="${this.query.length == 0 ? 'display:none' : ''}">
          ${t.search}
        </button>

      </form>
    `;
  }
});
  