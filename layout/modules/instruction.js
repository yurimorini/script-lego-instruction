

export const Store = (data) => {
  const collection = data.map(i => Instruction(i));
  return {
    all() {
      return collection;
    }
  };
}
  
export const Instruction = (data) => {
  return {
    get name() {
      return data?.title || "";
    },
  
    get family() {
      return data?.family || "";
    },
  
    get code() {
      return data?.code || "";
    },
  
    get image() {
      return data?.media[0] || null;
    }
  }
};