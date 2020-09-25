import {
    getMenuByRouter,
    getBreadCrumbList,
    getHomeRoute
} from '@/libs/myutil'
import router from '@/router'
import routers from '@/router/routers'
import config from '@/config'
const {
    homeName
} = config

export default {
    state: {
        breadCrumbList: [],
        homeRoute: getHomeRoute(routers, homeName),
    },
    getters: {
        menuList: (state, getters, rootState) => getMenuByRouter(routers, rootState.user.access),
    },
    mutations: {
        setBreadCrumb(state, route) {
            state.breadCrumbList = getBreadCrumbList(route, state.homeRoute)
        },

    },
    actions: {

    },

}