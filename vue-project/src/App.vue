<template>
  <v-app :style="{background: $store.getters.backgroundColor}">
    <v-app-bar
      app
      :color="$store.getters.color"
      dark
    >
    <v-app-bar-nav-icon :color="$store.getters.textColor" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <div class="d-flex align-center">
        <router-link to="/">
          <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            :src="$store.state.server +'/storage/images/logo-alb.png'"
            transition="scale-transition"
            width="40"
          />
        </router-link>
        <span :style="$store.getters.textStyle">Saidit</span>
      </div>
      <div class="ml-4" style="width: 250px">
        <v-select  v-model="currentCategory" @change="goToCategory" :items="categories" placeholder="Categories" item-text="title" hide-details></v-select>
      </div>
      <v-spacer></v-spacer>
      <v-btn @click="toggleDarkMode" fab small class="mx-2">
        <v-icon>mdi-theme-light-dark</v-icon>
      </v-btn>
      <v-menu
        ref="colorMenu"
        :close-on-content-click="false"
        v-model="colorMenu"
        :nudge-right="40"
        offset-y
        transition="scale-transition"
        origin="top right"
        class="hidden-md-and-down"
      >
        <template v-slot:activator="{ on }">
          <v-btn style="background-color: black" fab v-on="on" small>
            <v-avatar
            size="30"
            :color="$store.getters.color"
            style="font-size: 7px"
            >Color</v-avatar>
          </v-btn>
        </template>
        <v-card rounded='md'>
          <v-row no-gutters style="width: 170px">
            <template v-for="color,n in colors">
              <v-col :key="n">
                <v-card
                  class="pa-1"
                  outlined
                  :color="selectedColor === color ? 'black' : 'white'"
                  rounded='md'
                  :disabled="selectedColor === color"
                  @click="setColor(color)"
                >
                  <v-card
                  width="30px"
                  height="30px"
                  rounded='md'
                  class="mx-auto my-auto"
                  :color="color"
                  />
                </v-card>
              </v-col>
              <v-responsive
                v-if="(n+1) % 4 == 0 "
                :key="`width-${n}`"
                width="100%"
              ></v-responsive>
            </template>
          </v-row>
        </v-card>
      </v-menu>
      <v-menu
        ref="menu"
        :close-on-content-click="false"
        v-model="menu"
        :nudge-right="40"
        offset-y
        transition="scale-transition"
        origin="top right"
        class="hidden-md-and-down"
      >
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon v-if="!$store.getters.isLoggedIn">mdi-account</v-icon>
            <v-avatar color='grey' size='36' v-else>
              <span v-if="!$store.getters.user.avatar" class='text-h6'>{{$store.getters.user.username.charAt(0)}}</span>
              <v-img v-else :src="$store.state.server+'/storage/images/'+$store.getters.user.avatar" alt="avatar" />
            </v-avatar>
          </v-btn>
        </template>
        <v-list v-if="!$store.getters.isLoggedIn">
          <v-list-item>
            <v-list-item-title>
              <router-link to="/login">Login</router-link>
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>
              <router-link to="/register">Register</router-link>
            </v-list-item-title>
          </v-list-item>
        </v-list>
        <v-list v-else>
          <v-list-item>
            <v-list-item-title>
              <router-link to="/profile">{{$store.getters.user.nickname}}</router-link>
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>
              <router-link to="/settings">Settings</router-link>
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>
              <router-link to="/logout">Logout</router-link>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-navigation-drawer
      v-model="drawer"
      absolute
      bottom
      temporary
    >
      <v-card v-if="$store.getters.isLoggedIn" class="pa-0 ma-2">
        <v-card-title class="d-flex flex-row py-1 px-2">
          <v-btn text fab x-large @click="$router.push('/profile')">
            <v-avatar size="68">
              <v-img :src="$store.state.server+'/storage/images/'+$store.getters.user.avatar" />
            </v-avatar>
          </v-btn>
          <div>
            <v-card-title>
              {{$store.getters.user.nickname}}
            </v-card-title>
            <v-card-subtitle>
              @{{$store.getters.user.username}}
            </v-card-subtitle>
          </div>
        </v-card-title>
      </v-card>
      <v-list
        nav
        dense
      >
        <v-list-item-group
          v-model="group"
          active-class="deep-purple--text text--accent-4"
        >
        <div class="text-center">
          <h3>Liked Categories</h3>
        </div>
        <div v-for="category,i in $store.getters.likedCategories" :key="i">
          <v-card @click="$router.push('/categories/'+category.category.title)" class="pa-0 my-1">
            <v-card-title class="d-flex flex-row py-1 px-2">
                <v-avatar size="40">
                  <v-img :src="$store.state.server+'/storage/images/'+category.category.image" />
                </v-avatar>
              <div>
                <v-card-title class="py-2">
                  {{category.category.title}}
                </v-card-title>
              </div>
            </v-card-title>
          </v-card>
        </div>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
      <router-view/>
    </v-main>
    <v-footer app bottom fixed padless>Made by PP</v-footer>
  </v-app>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',

  data: () => ({
    categories: [],
    drawer: false,
    group: null,
    currentCategory: '',
    menu: false,
    colorMenu: false,
    selectedColor: '',
    colors:[
          '#9c9d97',
          '#474f52',
          '#1d1c21',
          '#ffce08',
          '#fd790d',
          '#e01010',
          '#825432',
          '#84db0d',
          '#03a903',
          '#3ab3da',
          '#169c9d',
          '#3c44a9',
          '#f38caa',
          '#c64fbd',
          '#8932b7',
          "#ff009e"
        ]
  }),
  computed: {
    selectedCategory() {
      return this.$store.state.selectedCategory
    },
    storeColor() {
      return this.$store.getters.color
    },
  },
  watch: {
    selectedCategory(newValue) {
      this.currentCategory = newValue
    },
    storeColor(newValue) {
      this.selectedColor = newValue
    },
  },
  mounted () {
    if (document.cookie.indexOf('auth_token') !== -1) {
      axios.post(this.$store.state.server+'/api/validate-token', {
        auth_token: document.cookie.split('auth_token=')[1]
      }).then(response => {
        if (response.data !== 'failed') { 
          this.$store.commit('setUser', response.data),
          this.$store.commit('setColor', response.data.color)
          this.$store.commit('setTextColor', this.getTextColor(response.data.color))
          this.$store.commit('setDarkMode', response.data.dark_mode)
          // this.$vuetify.theme.dark = true
          this.selectedColor = response.data.color
          this.$store.commit('setLikedCategories', response.data.liked_categories)
          this.$store.commit('setToken', JSON.parse(document.cookie.split('auth_token=')[1]))
          this.$store.commit('setIsLoggedIn', true)
        }
      })
    }
    axios.get(this.$store.state.server+'/api/categories').then(response => {
      this.categories = response.data
      this.$store.commit('setCategories', response.data)
    })
    this.categories = this.$store.state.categories
    // read the auth_token cookie and post to login
  },
  methods: {
    setColor(color) {
        this.selectedColor = color
        this.$store.commit('setTextColor', this.getTextColor(color))
        this.$store.commit('setColor', color)
        if (this.$store.getters.isLoggedIn) {
          axios.post(this.$store.state.server+'/api/profile/setcolor', {
            auth_token: document.cookie.split('auth_token=')[1],
            color: color
          }).then(response => {
            console.log(response);
          })
        }
    },
    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    },
    goToCategory() {
      this.$router.push('/categories/'+this.currentCategory)
      this.$store.commit('setSelectedCategory', this.currentCategory)
    },
    getTextColor(hexcolor){
      hexcolor = hexcolor.replace("#", "");
      var r = parseInt(hexcolor.substr(0,2),16);
      var g = parseInt(hexcolor.substr(2,2),16);
      var b = parseInt(hexcolor.substr(4,2),16);
      var yiq = ((r*299)+(g*587)+(b*114))/1000;
      return (yiq >= 128) ? 'black' : 'white';
    },
    toggleDarkMode() {
      this.$store.commit('setDarkMode',!this.$store.state.darkMode)
      if(this.$store.getters.isLoggedIn){
        axios.post(this.$store.state.server+'/api/profile/setdarkmode', {
          auth_token: document.cookie.split('auth_token=')[1],
          darkmode: this.$store.state.darkMode
        }).then(response => {
          console.log(response);
        })
      }
    },
  },
};
</script>

<style>
/* html {
  overflow: hidden !important;
  scrollbar-width: none;
  -ms-overflow-style: none;
} */

html::-webkit-scrollbar {
  width: 0;
  height: 0;
}

  /* width */
  ::-webkit-scrollbar {
    width: 8px;
  }

  /* Track */
  ::-webkit-scrollbar-track {
    background: #b1b1b12c;
    border-radius: 20px;
  }

  /* Handle */
  ::-webkit-scrollbar-thumb {
    background: rgb(90, 90, 90);
    border-radius: 20px;
  }

  /* Handle on hover */
  ::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
</style>