<template>
  <div>
    <v-dialog v-model="showPostDialog">
      <v-card>
        <v-card-title>
          {{currentPost.title}}
        </v-card-title>
        <v-card-text>
          {{currentPost.body}}
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="addPostDialog">
      <v-card>
        <v-card-title>
          <span class="headline">Add Post</span>
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="newPost.title" label="Name" required></v-text-field>
          <v-textarea v-model="newPost.body" label="Content" required></v-textarea>
        </v-card-text>
        <v-card-actions class="justify-end" >
          <v-btn class="ma-2" @click="createPost">Post</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <div class="text-center">
      <h2>{{category.title}}</h2>
      <h3>{{category.description}}</h3>
      <h1 v-if="posts.length === 0">There is nothing to see here yet.</h1>
      <div v-for="post,index in posts" :key="index">
        <v-card color="#FFB6C1" class="mt-3 mx-auto text-left" width="50%" @click="openPost(post)">
          <v-card-title>
            {{post.title}}
          </v-card-title>
          <v-card-text>
            {{post.body}}
          </v-card-text>
        </v-card>
      </div>
      <v-btn fixed bottom right fab class="mx-6 my-10" @click="addPostDialog = true"><v-icon>mdi-plus</v-icon></v-btn>
    </div>
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
        currentCategory:this.$attrs.category,
        addPostDialog: false,
        showPostDialog: false,
        newPost:{
          title:'',
          body: ''
        },
        currentPost: {}
      }
    },
    methods: {
      getPosts(){
        axios.get(this.$store.state.server+'/api/'+this.$attrs.category+'/posts').then(response => {
          this.posts = response.data.posts
          this.category = response.data.category
          console.log(response);
        }) 
      },
      openPost(post){
        this.currentPost = post
        this.showPostDialog = true
      },
      createPost(){
        axios.post(this.$store.state.server+'/api/posts/create', {
          title: this.newPost.title,
          body: this.newPost.body,
          poster_id: '07196a56-08b9-4952-9986-694f9b90a10e',
          category_id: this.category.id
        })
        .then(response => {
          console.log('Post response',response);
          if(response.data === 'success'){
            this.getPosts()
          }
        })
        .catch(error => {
          console.log(error)
        }).finally(() => {
          this.addPostDialog = false
        })
      },
      
    },
    watch: {
      $attrs() {
        this.getPosts()
        
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
      this.getPosts()
    },
  }
</script>
