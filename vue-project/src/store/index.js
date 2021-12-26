import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // server: 'http://192.168.1.16:2310',
    server: 'http://localhost:2310',
    selectedCategory: null,
    posts:[
    ],
    categories: [
    ]
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
    }
  },
  getters: {
    posts: state => state.posts,
    categories: state => state.categories,
    selectedCategory: state => state.selectedCategory
  },
  modules: {
  }
})
