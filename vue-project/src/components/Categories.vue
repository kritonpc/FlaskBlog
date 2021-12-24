<template>
  <div>
    <v-row v-if="categories">
      <v-col cols="6" sm="2" md="4" v-for="(item, index) in categories" :key="index" >
          <v-card @click="goToCategory(item)" class="ma-5 text-center">
            <v-img
              height="250"
              :src="$store.state.server+'/storage/images/'+item.image"
            ></v-img>
            <v-card-actions class="justify-center">
              {{item.title}}
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
      goToCategory(item){
        this.$router.push('/categories/'+item.title)
        console.log('You pressed ',item.title);
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
