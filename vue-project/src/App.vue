<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
    <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <div class="d-flex align-center">
        <router-link to="/">
          <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="@/assets/logo.png"
            transition="scale-transition"
            width="40"
          />
        </router-link>
        Saidit
      </div>
      <v-col cols='2' class="ml-4">
        <v-select v-model="currentCategory" @change="goToCategory" :items="categories" placeholder="Categories" item-text="title" hide-details></v-select>
      </v-col>
      <v-spacer></v-spacer>

      <v-btn fab small text
        class="white--text"
      >
        <v-icon>
          mdi-cog
        </v-icon>
      </v-btn>
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
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list>
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
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-navigation-drawer
      v-model="drawer"
      absolute
      bottom
      temporary
    >
      <v-list
        nav
        dense
      >
        <v-list-item-group
          v-model="group"
          active-class="deep-purple--text text--accent-4"
        >
          <router-link to="/categories/Animals">
            <v-list-item>
              <v-list-item-title>
                Animals
              </v-list-item-title>
            </v-list-item>
          </router-link>

          <router-link to="/categories/Engineering">
            <v-list-item>
              <v-list-item-title>
                Engineering
              </v-list-item-title>
            </v-list-item>
          </router-link>
          
          <router-link to="/categories/Gaming">
            <v-list-item>
              <v-list-item-title>
                Gaming
              </v-list-item-title>
            </v-list-item>
          </router-link>
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
  }),
  computed: {
    selectedCategory() {
      return this.$store.state.selectedCategory
    }
  },
  watch: {
    selectedCategory(newValue) {
      this.currentCategory = newValue
    }
  },
  mounted () {
    axios.get(this.$store.state.server+'/api/categories').then(response => {
      this.categories = response.data
      this.$store.commit('setCategories', response.data)
      console.log(response);
    })
    this.categories = this.$store.state.categories
    // read the auth_token cookie and post to login
    if (document.cookie.indexOf('auth_token') !== -1) {
      axios.post(this.$store.state.server+'/api/validate-token', {
        auth_token: document.cookie.split('auth_token=')[1]
      }).then(response => {
        if (response.data === 'success') {
          this.$store.commit('setUser', response.data)
          this.$store.commit('setLoggedIn', true)
        }
      })
    }
  },
  methods: {
    goToCategory() {
      this.$router.push('/categories/'+this.currentCategory)
      this.$store.commit('setSelectedCategory', this.currentCategory)
    },
  },
};
</script>
