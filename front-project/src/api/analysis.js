import axios from '@/libs/api.request';

export const getHistory = ({
  req,
}) => {
  return axios.request({
    method: "post",
    data: req,
    url: "linSystem/data/historyDatas"
  })
}

export const getHistoryDate = ({
  sendJson,
}) => {
  return axios.request({
    url: 'linSystem/data/historyDatasLimitCount',
    data: sendJson,
    method: "post",
  })
};

export const getHistoryDate2 = ({
                                   sendJson,
                               }) => {
    return axios.request({
        url: 'linSystem/data/historyDatasLimitCount2',
        data: sendJson,
        method: "post",
    })
};

export const getHistoryDate3 = ({
                                   sendJson,
                               }) => {
    return axios.request({
        url: 'linSystem/data/historyDatasLimitCount3',
        data: sendJson,
        method: "post",
    })
};

export const getHistoryContrast = ({
                               req,
                           }) => {
    return axios.request({
        method: "post",
        data: req,
        url: "linSystem/data/Contrast"
    })
}