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
        <v-select v-model="selectedCategory" @change="goToCategory" :items="categories" placeholder="Categories" item-text="title" hide-details></v-select>
      </v-col>
      <v-spacer></v-spacer>

      <v-btn fab small text>
        <v-icon>
          mdi-cog
        </v-icon>
      </v-btn>
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
    selectedCategory: ''
  }),
  mounted () {
    axios.get(this.$store.state.server+'/api/categories').then(response => {
      this.categories = response.data
      this.$store.commit('setCategories', response.data)
      console.log(response);
    })
    this.categories = this.$store.state.categories
  },
  methods: {
    goToCategory() {
      console.log(this.selectedCategory.title.toLowerCase());
      this.$router.push('/categories/'+this.selectedCategory.title.toLowerCase())
      this.$store.commit('setSelectedCategory', this.selectedCategory)
    }
  },
};
</script>
