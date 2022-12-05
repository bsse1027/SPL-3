import axios from "axios";

const Root = process.env.REACT_APP_ROOT_API;

export const runAnalytics = async (): Promise<any> => {
  return await axios.get(`${Root}/process_data`);
};
