
/**
 * Generate native event target 
 */
const createEventTarget = () => {
  class MyTarget extends EventTarget {}
  return new MyTarget();
}

/**
 * Create an internal dispatcher which dispatch
 * an event for every batch of sync changes.
 * 
 * Asynchronously dispatch the event as soon as possible.
 */
const createDispatcher = (events) => {
  return {
    changed: [],
    enqueued: false,

    dispatch(proxy) {
      const props = [...this.changed];
      this.reset();

      props.forEach(prop => {
        const name = generateEventProp(prop);
        const detail = { detail: { [prop]: proxy[prop], state: proxy } };
        const e = new CustomEvent(name, detail)
        events.dispatchEvent(e);
      });
    },

    enqueue(prop, proxy) {;
      if (!this.changed.includes(prop)) {
        this.changed.push(prop);
        if (!this.enqueued) {
          setTimeout(() => this.dispatch(proxy), 0);
          this.enqueued = true;
        }
      }
    },

    reset() {
      this.changed = [];
      this.enqueued = false;
    },
  };
}

/**
 * Proxy the object and enqueue the change
 * to the dispatcher. 
 */
const createProxy = (state, queue) => {
  const handler = {
    set(object, prop, value, proxy) {
      object[prop] = value;
      queue.enqueue(prop, proxy);
      return true;
    }
  };
  return new Proxy(state, handler);
}

const generateEventProp = (property) => {
  return `stateChanged__${property}`
}

/**
 * Wraps a state object and provide a subscription
 * method to be notified whenever a property of the state
 * changes. 
 */
export const State = (state) => {
  const events = createEventTarget();
  const internal = createDispatcher(events, state);
  const proxy = createProxy(state, internal);

  return {
    get state() {
      return proxy;
    },

    subscribe(property, handler) {
      const event = generateEventProp(property)
      events.addEventListener(event, handler);
    },
  };
};
