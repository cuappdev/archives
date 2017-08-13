// @flow
// General utility functions helpful in a JS setting across all AppDev projects

const encodeUrlParams = (params: { [string]: any }): string => {
  return Object.keys(params).map((k: string) => {
    return `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`;
  }).join('&');
};

export default {
  encodeUrlParams
};
