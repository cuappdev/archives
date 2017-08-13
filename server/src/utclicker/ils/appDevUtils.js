// @flow
// General utility functions / Objects helpful in a JS setting across
// all AppDev projects
import axios from 'axios';

const encodeUrlParams = (params: { [string]: any }): string => {
  return Object.keys(params).map((k: string) => {
    return `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`;
  }).join('&');
};

const googleAxios = axios.create({
  baseURL: 'https://www.googleapis.com',
  timeout: 5000
});

export default {
  encodeUrlParams,
  googleAxios
};
