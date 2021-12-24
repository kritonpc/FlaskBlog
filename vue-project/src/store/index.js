import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    server: 'http://192.168.1.16:2310',
    posts:[
      {
        title: 'Test',
        category: 'Gaming',
        content:'This is a test'
      },
      {
        title: 'Test',
        category: 'Animals',
        content:'This is a test'
      },{
        title: 'Test',
        category: 'Animals',
        content:'This is a test'
      },{
        title: 'Test',
        category: 'Gaming',
        content:'This is a test'
      },{
        title: 'Test',
        category: 'Gaming',
        content:'This is a test'
      }
    ],
    categories: [
      {
        title: 'Animals',
        picUrl: 'https://a-z-animals.com/media/2021/01/mammals-400x300.jpg',
        route: 'Animals'
      },
      {
        title: 'Gaming',
        picUrl: 'https://threepixelslab.gr/wp-content/uploads/2020/05/gaming-revenue-3pl.jpg',
        route: 'Gaming'
      },
      {
        title: 'Engineering',
        picUrl: 'https://d3jh33bzyw1wep.cloudfront.net/s3/W1siZiIsIjIwMTkvMTEvMjEvMTIvMDYvMjcvMzIvc2h1dHRlcnN0b2NrXzE0OTg3NDI1MTkuanBnIl0sWyJwIiwidGh1bWIiLCI4MDB4NDUwIyJdXQ',
        route: 'Engineering'
      },
      {
        title: 'Books',
        picUrl: 'https://topsites.gr/wp-content/uploads/2020/08/books.jpg',
        route: 'Books'
      },
      {
        title: 'Memes',
        picUrl: 'http://nina07.github.io/assets/images/hero/meme-background.jpg',
        route: 'Memes'
      },
      {
        title: 'News',
        picUrl: 'https://dg31sz3gwrwan.cloudfront.net/fanart/368787/1383613-0-q80.jpg',
        route: 'News'
      },
      {
        title: 'Food',
        picUrl: 'https://www.wikihow.com/images/thumb/5/50/Eat-More-Food-Step-1-Version-2.jpg/v4-460px-Eat-More-Food-Step-1-Version-2.jpg',
        route: 'Food'
      },
      {
        title: 'Movies',
        picUrl: 'https://www.newstatesman.com/wp-content/uploads/sites/2/2021/12/2ATHYW0-1038x778.jpg',
        route: 'Movies'
      },
      {
        title: 'Music',
        picUrl: 'https://learnenglishfunway.com/wp-content/uploads/2020/12/Music-2.jpg',
        route: 'Music'
      },
    ]
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
