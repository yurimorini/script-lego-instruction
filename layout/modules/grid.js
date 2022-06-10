import { define, html } from 'https://unpkg.com/uce?module';

define('ym-lego-list', {
  extends: "div",
  
  prefix: "../",

  props: {
    list: []
  },

  render() {
    this.html`
    <ul class="grid">
      ${this.list.map((item) => { return html`
        <li class="grid__item">
          <figure class="grid-item" data-family="${item.family}">
            <a class="grid-item__link" href="">
              
              <img 
                class="grid-item__thumb" 
                src="${this.prefix + item.image}" 
                loading="lazy" />
              
              <figcaption class="grid-item__desc">
                <span class="grid-item__code">${item.code}</span>
                <span class="grid-item__name">${item.name}</span> 
              </figcaption>
            
            </a>
          </figure>
        </li>
      `})}
    </ul>`;
  }
});
  