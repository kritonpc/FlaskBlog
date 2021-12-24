<template>
  <div class="text-center">
    <h2>{{$attrs.category}}</h2>
    <v-card color="#FFB6C1" class="mt-3 mx-auto text-left" width="50%" v-for="post in posts" :key="post">
      <v-card-title>
        {{post.title}}
      </v-card-title>
      <v-card-text>
        {{post.content}}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  export default {
    name: 'Categories',
    data() {
      return {
        posts: [],
        currentCategory:this.$attrs.category
      }
    },
    methods: {
      
    },
    watch: {
      $attrs() {
        this.posts = []
        this.$store.state.posts.forEach(post => {
        if(post.category === this.$attrs.category){
          this.posts.push(post)
        }
      }); 
      }
    },
    mounted () {
      this.$store.state.posts.forEach(post => {
        if(post.category === this.$attrs.category){
          this.posts.push(post)
        }
      });      
    },
  }
</script>
