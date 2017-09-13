// @flow

class Model {
  fields: Object;

  constructor (json: Object) {
    this.fields = {};
    for (let k in json) {
      this.fields[k] = json[k];
    }
  }
}

export default Model;
