import { define } from 'https://unpkg.com/uce?module';

const t = {
  search: "Search",
  placeholder: "Cosa stai cercando ?"
}

define('ym-lego-search', {
  extends: "div",
  
  props: {
    query: "",
  },

  bound: [
    'submit', 'input'
  ],

  input(e) {
    e.preventDefault();
    this.query = e.target.value;
  },

  submit(e) {
    e.preventDefault();

    this.dispatchEvent(new CustomEvent('search', { 
      detail: { query: this.query },
      bubbles: true
    }));
  },

  render() {
    this.html`
      <form class="search" onsubmit="${this.submit}">

        <input 
          class="search__input"
          oninput=${this.input} 
          placeholder="${t.placeholder}"
          type="text" 
          name="search" 
          value="${this.query}" />

        <button class="search__button">
          ${t.search}
        </button>

      </form>
    `;
  }
});
  