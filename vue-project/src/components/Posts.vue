<template>
  <div>
    <v-dialog v-model="addPostDialog" width='50%'>
      <v-card class=" mx-auto">
        <v-toolbar  flat>
          <v-toolbar-title>
            New Post
          </v-toolbar-title>
            <v-spacer/>
            <v-btn fab small text @click="addPostDialog = false">
              <v-icon>
                mdi-close
              </v-icon>
            </v-btn>
        </v-toolbar>
        <v-divider/>
        <v-textarea outlined hide-details class="pa-3" rows="1" placeholder="Title" no-resize v-model="newPost.title"></v-textarea>
        <v-textarea outlined hide-details class="pa-3" rows="3" placeholder="Content" v-model="newPost.content"></v-textarea>
        <v-select class="pa-3" :items='categories' v-model='newPost.category' placeholder="Category"></v-select>
        <v-card-actions class="justify-end" >
          <v-btn class="ma-2" @click="createPost">Post</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-container class="justify-center">
      <v-card v-for="post in listOfPosts.slice().reverse()" :key="post.content" width='50vw' class="mt-5 mx-auto">
        <v-card-title >{{post.title}}</v-card-title>
        <v-card-text>{{post.content}}
        </v-card-text>
        <v-divider/>
        <v-card-actions>
          <v-btn x-small text fab>
            <v-icon>
              mdi-thumb-up
            </v-icon>
          </v-btn>
          <v-btn x-small text fab>
            <v-icon>
              mdi-thumb-down
            </v-icon>
          </v-btn>
          <v-btn x-small text fab>
            <v-icon>
              mdi-comment
            </v-icon>
          </v-btn>
          <v-spacer/>
          <v-btn x-small text fab>
            <v-icon>
              mdi-cog
            </v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
    <v-btn @click="addPostDialog = true" class="ma-4" x-large fab fixed bottom right color="blue">
      <v-icon>mdi-plus</v-icon>
    </v-btn>
  </div>
</template>

<script>
  export default {
    name: 'Posts',
    data() {
      return {
        addPostDialog: false,
        postName: '',
        categories:[
          'karkinos',
          'oxi karkinos'
        ],
        newPost:{
          name:'',
          content: ''
        },
        emptyPost:{
          name:'',
          content: ''
        },
        listOfPosts: [],
      }
    },
    methods: {
      createPost() {
        this.listOfPosts.push({...this.newPost})
        this.newPost = {...this.emptyPost}
        this.addPostDialog = false
      },
    }
  }
</script>
