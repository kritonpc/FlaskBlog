<template>
  <div>
    <v-row v-if="categories">
      <v-col cols="6" sm="2" md="4" v-for="category,index in categories" :key="index" >
          <v-card @click="goToCategory(category)" class="ma-5 text-center">
            <v-img
              height="250"
              :src="$store.state.server+'/storage/images/'+category.image"
            ></v-img>
            <v-card-actions class="justify-center">
              {{category.title}}
            </v-card-actions>
          </v-card>
      </v-col>
  </v-row>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'Categories',
    data() {
      return {
        categories:[
        ],
      }
    },
    methods: {
      goToCategory(category){
        this.$router.push('/categories/'+category.title)
        this.$store.commit('setSelectedCategory', category)
        console.log('You pressed ',category.title);
      }
    },
    mounted () {
      axios.get(this.$store.state.server+'/api/categories').then(response => {
        this.categories = response.data
        console.log(response);
      })
      // this.categories = this.$store.state.categories
    },
  }
</script>
