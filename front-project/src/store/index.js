import Vue from 'vue'
import Vuex from 'vuex'
import user from './mymodule/user'
import app from './mymodule/app'
Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    //
  },
  mutations: {
    //
  },
  actions: {
    //
  },
  modules: {
    user,
    app
  }
})