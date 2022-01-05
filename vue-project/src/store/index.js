import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // server: 'http://192.168.1.16:2310',
    server: 'http://'+window.location.hostname+':2310',
    selectedCategory: null,
    posts:[
    ],
    categories: [
    ],
    user: {id: null, username: null, avatar: null, nickname: null},
    token: null,
    isLoggedIn: false,
    color: 'primary',
    textColor: 'black',
    likedCategories: [],
    darkMode: false,
    backgroundColor: '#fafafa',
  },
  mutations: {
    addPost(state, post){
      state.posts.push(post)
    },
    removePost(state, post){
      state.posts.splice(state.posts.indexOf(post), 1)
    },
    addCategory(state, category){
      state.categories.push(category)
    },
    removeCategory(state, category){
      state.categories.splice(state.categories.indexOf(category), 1)
    },
    setSelectedCategory(state, category){
      state.selectedCategory = category
    },
    setCategories(state, categories){
      state.categories = categories
    },
    setUser(state, user){
      state.user = user
    },
    setToken(state, token){
      state.token = token
    },
    setIsLoggedIn(state, isLoggedIn){
      state.isLoggedIn = isLoggedIn
    },
    setColor(state, color){
      state.color = color
    },
    setLikedCategories(state, categories){
      state.likedCategories = categories
    },
    setTextColor(state, color){
      state.textColor = color
    },
    setDarkMode(state, darkMode){
      state.darkMode = darkMode
      if (darkMode) {
        state.backgroundColor = '#212121'
      } else {
        state.backgroundColor = '#fafafa'
      }
    },
    setBackgroundColor(state, color){
      state.backgroundColor = color
    }
  },
  actions: {
    addPost({commit}, post){
      commit('addPost', post)
    },
    removePost({commit}, post){
      commit('removePost', post)
    },
    addCategory({commit}, category){
      commit('addCategory', category)
    },
    removeCategory({commit}, category){
      commit('removeCategory', category)
    },
    setCategories({commit}, categories){
      commit('setCategories', categories)
    },
    setSelectedCategory({commit}, category){
      commit('setSelectedCategory', category)
    },
    setUser({commit}, user){
      commit('setUser', user)
    },
    setToken({commit}, token){
      commit('setToken', token)
    },
    setIsLoggedIn({commit}, isLoggedIn){
      commit('setIsLoggedIn', isLoggedIn)
    },
    setColor({commit}, color){
      commit('setColor', color)
    },
    setLikedCategories({commit}, categories){
      commit('setLikedCategories', categories)
    },
    setTextColor({commit}, color){
      commit('setTextColor', color)
    },
    setDarkMode({commit}, darkMode){
      commit('setDarkMode', darkMode)
    },
    setBackgroundColor({commit}, color){
      commit('setBackgroundColor', color)
    }
  },
  getters: {
    posts: state => state.posts,
    categories: state => state.categories,
    selectedCategory: state => state.selectedCategory,
    user: state => state.user,
    token: state => state.token,
    isLoggedIn: state => state.isLoggedIn,
    color: state => state.color,
    likedCategories: state => state.likedCategories,
    textColor: state => state.textColor,
    textStyle: state => 'color: '+state.textColor,
    darkMode: state => state.darkMode,
    backgroundColor: state => state.backgroundColor,
  },
  modules: {
  }
})
