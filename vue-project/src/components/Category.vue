<template>
  <div class="text-center">
    <h2>{{category.title}}</h2>
    <v-card color="#FFB6C1" class="mt-3 mx-auto text-left" width="50%" v-for="post in posts" :key="post">
      <v-card-title>
        {{post.title}}
      </v-card-title>
      <v-card-text>
        {{post.body}}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'Categories',
    data() {
      return {
        posts: [],
        category: [],
        currentCategory:this.$attrs.category
      }
    },
    methods: {
      
    },
    watch: {
      $attrs() {
        axios.get(this.$store.state.server+'/api/'+this.$attrs.category+'/posts').then(response => {
          this.posts = response.data.posts
          this.category = response.data.category
          console.log(response);
        })
      //   this.$store.state.posts.forEach(post => {
      //   if(post.category === this.$attrs.category){
      //     this.posts.push(post)
      //   }
      // }); 
      }
    },
    mounted () {
      // this.$store.state.posts.forEach(post => {
      //   if(post.category === this.$attrs.category){
      //     this.posts.push(post)
      //   }
      // });     
      axios.get(this.$store.state.server+'/api/'+this.$attrs.category+'/posts').then(response => {
          this.posts = response.data.posts
          this.category = response.data.category
          console.log(response);
        }) 
    },
  }
</script>
