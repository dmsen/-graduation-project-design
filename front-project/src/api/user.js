import axios from '@/libs/api.request'

export const login = ({
  userName,
  password,
  optionLevel
}) => {
  const data = {
    userName,
    password,
    optionLevel
  }
  return axios.request({
    url: 'linSystem_login',
    data: data,
    method: 'post'
  })
}
// export const getUserInfo = (token) => {
//   return axios.request({
//     url: 'get_info',
//     params: {
//       token
//     },
//     method: 'get'
//   })
// }

// export const logout = (token) => {
//   return axios.request({
//     url: 'logout',
//     method: 'post'
//   })
// }



/**
 * @description 获取所有用户
 */
export const getUsers = ({
  sendPage
}) => {
  return axios.request({
    url: 'linSystem/userGet',
    method: 'post',
    data: {
      sendPage: sendPage
    }

  })
};

/**
 * @description 增加用户
 */
export const addUser = ({
  jurisdiction,
  name,
  password,
  remark,
  status
}) => {
  return axios.request({
    url: 'linSystem/userAdd',
    data: {
      userName: name,
      jurisdiction: Number(jurisdiction),
      password: password,
      remarks: remark,
      status: Number(status)
    },
    method: 'post'
  })
};

/**
 * @description 删除用户
 */
export const deleteUser = ({
  id,
  userId
}) => {
  return axios.request({
    url: 'linSystem/userDel',
    data: {
      id: id,
      userId: Number(userId)
    },
    method: 'post'
  })
};
/**
 * @description 修改用户
 */
export const changeUser = ({
  id,
  jurisdiction,
  name,
  password,
  remark,
  role,
  status,
  mode
}) => {
  return axios.request({
    url: 'linSystem/userUpdata',
    data: {
      id: id,
      userName: name,
      jurisdiction: jurisdiction,
      password: password,
      remarks: remark,
      roles: role,
      status: status,
      mode: mode
    },
    method: 'post'
  })
};

/**
 * @description 修改用户头像
 */
export const changeUserPic = (
  formData
) => {
  return axios.request({
    url: 'linSystem/modePic',
    data: formData,

    method: 'post'
    // file:file
  })
};

/**
 * @description 发布通知
 */
export const noticeSub = ({
  hutUserId,
  userName,
  content,
  evaDate
}) => {
  return axios.request({
    url: 'linSystem/notice',
    data: {
      userName: userName,
      hutUserId: hutUserId.toString(),
      courseEvaluateMsg: content,
      courseEvaluateDate: evaDate,
    },
    method: 'post'
  })
};



/**
 * @description 获取用户对应的通知
 */
export const getNotice = ({
  userId,
  sendPage
}) => {
  return axios.request({
    url: 'linSystem/getNotice',
    method: 'post',
    data: {
      userId: userId,
      sendPage: sendPage
    }

  })
};

/**
 * @description 标记用户已读的通知
 */
export const readNotice = ({
  id
}) => {
  return axios.request({
    url: 'linSystem/readNotice',
    method: 'post',
    data: {
      noticeId: id,
    }

  })
};

/**
 * @description 获取用户已读的通知
 */
export const readEdNotice = ({
  userId,
  sendPage
}) => {
  return axios.request({
    url: 'linSystem/readEdNotice',
    method: 'post',
    data: {
      userId: userId,
      sendPage: sendPage
    }

  })
};




// export const getUnreadCount = () => {
//   return axios.request({
//     url: 'message/count',
//     method: 'get'
//   })
// }

// export const getMessage = () => {
//   return axios.request({
//     url: 'message/init',
//     method: 'get'
//   })
// }

// export const getContentByMsgId = msg_id => {
//   return axios.request({
//     url: 'message/content',
//     method: 'get',
//     params: {
//       msg_id
//     }
//   })
// }

// export const hasRead = msg_id => {
//   return axios.request({
//     url: 'message/has_read',
//     method: 'post',
//     data: {
//       msg_id
//     }
//   })
// }

// export const removeReaded = msg_id => {
//   return axios.request({
//     url: 'message/remove_readed',
//     method: 'post',
//     data: {
//       msg_id
//     }
//   })
// }

// export const restoreTrash = msg_id => {
//   return axios.request({
//     url: 'message/restore',
//     method: 'post',
//     data: {
//       msg_id
//     }
//   })
// }