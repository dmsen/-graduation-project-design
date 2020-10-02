import {
  login,
  changeUser,
  changeUserPic,
  getNotice,
  readNotice,
  readEdNotice
} from "@/api/user"; //存储跨域请求的接口
import {
  setToken,
  getToken,
  setUserImage,
  saveUserId,
  saveUserName
} from "@/libs/myutil";
export default {
  state: {
    userName: "",
    userId: "",
    avatarImgPath: "",
    token: getToken(),
    access: "",
    userInfo: "",
    hasGetInfo: false,
  },
  mutations: {
    setAvator(state, img) {
      state.avatorImgPath = img;
      setUserImage(img);
    },
    setUserId(state, id) {
      state.userId = id;
      saveUserId(id)
    },
    setUserName(state, name) {
      state.userName = name;
      saveUserName(name)
    },
    setAccess(state, access) {
      state.access = access;
    },
    setToken(state, token) {
      state.token = token;
      setToken(token);
    },
    setHasGetInfo(state, status) {
      state.hasGetInfo = status;
    },
    setUserInfo(state, info) {
      state.userInfo = info;
    },
  },
  getters: {},
  actions: {
    // 登录
    handleLogin({
      state,
      commit
    }, {
      userName,
      password,
      optionLevel
    }) {
      userName = userName.trim();
      return new Promise((resolve, reject) => {
        // 跳过使用接口 ，直接登陆
        // commit('setUserInfo', 'msg')
        // commit('setToken', 1)
        // resolve("success");

        login({
            userName,
            password,
            optionLevel,
          })
          .then((res) => {
            const data = res.data;
            console.log("登陆接口数据");
            console.log(data);
            if (data.result !== 0) {
              resolve(data.msg);
            } else {
              commit("setUserInfo", data.msg);
              commit("setToken", data.msg.jurisdiction);
              commit("setAvator", data.msg.userTou);
              commit("setUserId", data.msg.userId);
              commit("setUserName", data.msg.userName);
              console.log(data.msg.userId);
              resolve("success");
            }
          })
          .catch((err) => {
            console.log("错误", err);
            reject(err);
          });
      });
    },
    // 退出登录
    handleLogOut({
      state,
      commit
    }) {
      return new Promise((resolve, reject) => {
        // logout(state.token).then(() => {
        //     commit('setToken', '')
        //     commit('setAccess', [])
        //     resolve()
        // }).catch(err => {
        //     reject(err)
        // })
        // 如果你的退出登录无需请求接口，则可以直接使用下面三行代码而无需使用logout调用接口
        commit("setToken", "");
        commit("setAccess", []);
        commit("setHasGetInfo", false);
        resolve();
      });
    },
    getUserInfo({
      state,
      commit
    }) {
      return new Promise((resolve, reject) => {
        commit("setAccess", [state.token].map(Number));
        commit("setHasGetInfo", true);
        resolve({
          access: state.access,
        });
      });
    },
    // 用户个人信息修改
    handPersonchange({
      commit
    }, {
      id,
      name,
      password,
      remark,
      status,
      mode
    }) {
      return new Promise((resolve, reject) => {
        changeUser({
            id,
            name,
            password,
            remark,
            status,
            mode,
          })
          .then((res) => {
            const data = res.data;
            if (data.status === 1) {} else {
              // commit('setToken', data.data.jurisdiction)
            }
            resolve(data);
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    // 用户头像修改
    UserPicChange({
      commit
    }, formData) {
      return new Promise((resolve, reject) => {
        changeUserPic(formData)
          .then((res) => {
            const data = res.data;
            if (data.status === 1) {} else {
              // commit('setToken', data.data.jurisdiction)
            }
            resolve(data);
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    // 获取用户通知
    handGetNotice({
      commit
    }, {
      userId,
      sendPage
    }) {
      return new Promise((resolve, reject) => {
        getNotice({
          userId,
          sendPage
        }).then(res => {
          const data = res.data;
          if (data.status === 1) {} else {
            // commit('setToken', data.data.jurisdiction)
          }
          resolve(data);
        }).catch(err => {
          reject(err)
        })
      })
    },
    // 标记通知已读
    handReadNotice({
      commit
    }, {
      id,
    }) {
      return new Promise((resolve, reject) => {
        readNotice({
          id,
        }).then(res => {
          const data = res.data;
          if (data.status === 1) {} else {
            // commit('setToken', data.data.jurisdiction)
          }
          resolve(data);
        }).catch(err => {
          reject(err)
        })
      })
    },
    // 获取已读通知
    handReadEdNotice({
      commit
    }, {
      userId,
      sendPage
    }) {
      return new Promise((resolve, reject) => {
        readEdNotice({
          userId,
          sendPage
        }).then(res => {
          const data = res.data;
          if (data.status === 1) {} else {
            // commit('setToken', data.data.jurisdiction)
          }
          resolve(data);
        }).catch(err => {
          reject(err)
        })
      })
    },

  },
};