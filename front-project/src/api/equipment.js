import axios from '@/libs/api.request';
// 设备类型管理
/**
 * @description 增加设备类型
 */
export const addMacType = ({
  name,
  detail,
  code
}) => {
  return axios.request({
    url: 'linSystem/machType/add',
    data: {
      machTypeName: name,
      machTypeDesc: detail,
      machTypeCode: code
    },
    method: 'post'
  })
}
/**
 * @description 修改设备类型
 */
export const changeMacType = ({
  id,
  name,
  detail,
  code
}) => {
  return axios.request({
    url: 'linSystem/machType/mode',
    data: {
      machTypeId: id,
      machTypeName: name,
      machTypeDesc: detail,
      machTypeCode: code
    },
    method: 'post'
  })
}
/**
 * @description 删除设备类型
 */
export const deleteMacType = ({
  id,
}) => {
  return axios.request({
    url: 'linSystem/machType/del',
    data: {
      machTypeId: id,
    },
    method: 'post'
  })
}
/**
 * @description 获取所有设备类型
 */
export const getMacTypes = (sendPage) => {
  return axios.request({
    url: 'linSystem/machType/get',
    method: 'post',
    data: {
      sendPage: sendPage
    }
  })
}


// 设备管理
/**
 * @description 增加设备
 */
export const addMachine = ({
  name,
  code,
  desc,
  date,
  customer,
  office
}) => {
  return axios.request({
    url: 'linSystem/machine/add',
    data: {
      machineName: name,
      machTypeId: code,
      machineDesc: desc,
      dateOfProduct: date,
      customerId: customer,
      office: office
    },
    method: 'post'
  })
}
/**
 * @description 修改设备
 */
export const changeMachine = ({
  name,
  id,
  code,
  desc,
  date,
  customer,
  office
}) => {
  return axios.request({
    url: 'linSystem/machine/mode',
    data: {
      machineId: id,
      machineName: name,
      machTypeId: code,
      machineDesc: desc,
      dateOfProduct: date,
      customerId: customer,
      office: office
    },

    method: 'put'
  })
}
/**
 * @description 删除设备
 */
export const deleteMachine = ({
  id,
}) => {
  return axios.request({
    url: 'linSystem/machine/del',
    method: 'delete',
    data: {
      machineId: id,
    },
  })
}
/**
 * @description 获取所有设备
 */
export const getMachines = (sendPage) => {
  return axios.request({
    url: 'linSystem/machine/get',
    method: 'post',
    data: {
      sendPage: sendPage
    }
  })
}