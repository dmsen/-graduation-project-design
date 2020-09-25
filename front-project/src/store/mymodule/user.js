import {
    login,
    logout,
    getUserInfo,
} from '@/api/user' //存储跨域请求的接口
import {
    setToken,
    getToken,
    setUserImage
} from '@/libs/myutil'
export default {
    state: {
        userName: '',
        userId: '',
        avatarImgPath: '',
        token: getToken(),
        access: '',
        userInfo: '',
        hasGetInfo: false,
    },
    mutations: {
        setAvator(state, img) {
            state.avatorImgPath = img;
            setUserImage(img)
        },
        setUserId(state, id) {
            state.userId = id
        },
        setUserName(state, name) {
            state.userName = name
        },
        setAccess(state, access) {
            state.access = access
        },
        setToken(state, token) {
            state.token = token
            setToken(token)
        },
        setHasGetInfo(state, status) {
            state.hasGetInfo = status
        },
        setUserInfo(state, info) {
            state.userInfo = info
        },

    },
    getters: {

    },
    actions: {
        // 登录
        handleLogin({
            state,
            commit
        }, {
            userName,
            password
        }) {
            userName = userName.trim()
            return new Promise((resolve, reject) => {
                // 跳过使用接口 ，直接登陆
                commit('setUserInfo', 'msg')
                commit('setToken', 1)
                resolve("success");
                // 使用接口的方法如下  之后改进
                // login({
                //     userName,
                //     password
                // }).then(res => {
                //     const data = res.data

                //     commit('setToken', data.token)
                //     resolve()
                // }).catch(err => {

                //     reject(err)
                // })

            })
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
                commit('setToken', '')
                commit('setAccess', [])
                resolve()
            })
        },
        getUserInfo({
            state,
            commit
        }) {
            return new Promise((resolve, reject) => {
                commit('setAccess', [state.token].map(Number));
                commit('setHasGetInfo', true);
                commit('setUserId', state.userId);
                commit('setUserName', state.userName);
                resolve({
                    access: state.access
                })
            })
        },
    }
}