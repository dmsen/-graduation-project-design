import axios from '@/libs/api.request';

export const getjson = () => {
  return axios.request({
    method: "get",
    url: "linSystem/jsonget"
  })
}