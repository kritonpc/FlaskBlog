<template>
  <div>
    <v-dialog v-model="showPostDialog" :width="calculateWidth()">
      <v-card class='mx-auto' light v-if="currentPost !== undefined" rounded='lg'>
        <v-card-title class="d-flex flex-row">
          <v-avatar size="68">
            <v-img :src="$store.state.server+'/storage/images/'+currentPost.poster.avatar" />
          </v-avatar>
          <div>
            <v-card-title>
              {{currentPost.title}}
            </v-card-title>
            <v-card-subtitle>
              Posted by {{currentPost.poster.nickname}} {{moment(currentPost.timestamp).fromNow()}}
            </v-card-subtitle>
          </div>
        </v-card-title>
        <v-card-text>
          <h3>{{currentPost.body}}</h3>
        </v-card-text>
        <v-card-text v-if="currentPost.media">
          <v-img :src="$store.state.server+'/storage/images/'+currentPost.media" width="100%"></v-img>
        </v-card-text>
        <v-divider/>
        <v-card-actions>
          <!-- like button -->
          <v-btn x-small text fab @click="like(currentPost)" :disabled="!$store.getters.isLoggedIn">
            <v-icon :color='hasUserLiked(currentPost)'>
              mdi-thumb-up
            </v-icon>
          </v-btn>
          <span class="mr-3" style="font-size: 10px">{{currentPost.likes_count}}</span>
          <v-btn x-small text fab @click="dislike(currentPost)" :disabled="!$store.getters.isLoggedIn">
            <v-icon :color='hasUserDisliked(currentPost)'>
              mdi-thumb-down
            </v-icon>
          </v-btn>
          <span class="mr-3" style="font-size: 10px">{{currentPost.dislikes_count}}</span>
          <!-- comment button -->
          <v-btn x-small text fab :disabled="!$store.getters.isLoggedIn">
            <v-icon>
              mdi-comment
            </v-icon>
          </v-btn>
          <span class="mr-3" style="font-size: 10px">{{currentPost.comments_count}}</span>
        </v-card-actions>
        <v-divider/>
        <v-card-actions v-if="currentPost.comments_count>0">
          <v-list id="scroll" style="width:100%" :style="currentPost.media ? 'max-height: 20vh' : 'max-height: 50vh' " class="overflow-y-auto">
            <v-list-item v-for="comment,i in currentPost.comments" :key="i" class="my-2 align-start">
              <div class="d-flex flex-row align-center">
                  <v-avatar size='36'>
                    <v-img :src="$store.state.server+'/storage/images/'+comment.user.avatar" alt="avatar" />
                  </v-avatar>
                  <div class="d-flex flex-column mx-1">
                    <span style="font-size:12px">{{comment.user.nickname}}</span>
                    <span style="font-size:8px">{{moment(comment.timestamp).fromNow()}}</span>
                  </div>
              </div>
              <v-spacer/>
              <v-card rounded='xl' class="mx-2 pa-2 justify-end" style='font-color: white; font-size: 12px' :color="$store.getters.color" max-width='60%'>
                {{comment.body}}
              </v-card>
            </v-list-item>
          </v-list>
        </v-card-actions>
        <v-card-actions class="py-0 px-4" v-if="$store.getters.isLoggedIn">
          <v-textarea rows='1' v-model="comment" placeholder="Comment" class="py-1 my-1" hide-details style="font-size: 12px" @keyup.enter="addComment(currentPost)">
            <!-- append post button in slot -->
            <template slot="append-outer">
              <v-btn fab text x-small @click="addComment(currentPost)">
                <v-icon>
                  mdi-send
                </v-icon>
              </v-btn>
            </template>
          </v-textarea>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog :width="calculateWidth()" v-model="addPostDialog">
      <v-card>
        <v-card-title>
          <span class="headline">Add Post</span>
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="newPost.title" label="Name" required></v-text-field>
          <v-textarea v-model="newPost.body" label="Content" required></v-textarea>
          <div v-if='showUpload'>
            <label>Upload Picture</label>
            <v-img v-if="picture" :src="$store.state.server+'/storage/images/'+picture" width="400" contain></v-img>
            <input accept="image/*" type="file" @change="handleFileUpload( $event )"/>
            <!-- <v-btn v-if="file" @click="submitFile()">Upload</v-btn> -->
          </div>
        </v-card-text>
        <v-card-actions class="" >
          <v-btn text fab @click="showUpload = !showUpload"><v-icon :color="showUpload ? 'blue' : 'black'">mdi-image-plus</v-icon></v-btn>
          <v-spacer/>
          <v-btn class="ma-2" @click="createPost">Post</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <div class="text-center">
      <v-img v-if="category.image !== undefined" width="100%" max-height="180px" class="align-center" :src="$store.state.server+'/storage/images/'+category.banner">
      <v-chip large class='mt-2' color='black'><h1 style='color: white'>
        <div>
          <span>{{category.title}}</span>
          <v-btn fab x-small class="ml-2" @click="likeCategory">
            <v-icon size='24' :color='isCategoryLiked()'>
              mdi-heart
            </v-icon>
          </v-btn>
        </div>
        </h1></v-chip>
        <br>
        <v-chip color='black'>
        <h3 style='color: white'>{{category.description}}</h3>
        </v-chip>
      </v-img>
      
      <h1 v-if="posts.length === 0">There is nothing to see here yet.</h1>
      <v-container>
      <div v-for="post,index in posts.slice().reverse()" :key="index">
        <v-card rounded='xl' :color="$store.getters.color" class="mt-3 mx-auto text-left" width="100%" @click="openPost(posts.length-index-1)">
          <v-card-title class="d-flex flex-row">
            <v-avatar size="68">
              <v-img :src="$store.state.server+'/storage/images/'+post.poster.avatar" />
            </v-avatar>
            <div>
              <v-card-title>
                {{post.title}}
              </v-card-title>
              <v-card-subtitle>
                Posted by <strong>{{post.poster.nickname}}</strong> {{moment(post.timestamp).fromNow()}}
              </v-card-subtitle>
            </div>
          </v-card-title>
          <v-card-text>
            <h3>{{post.body}}</h3>
          </v-card-text>
          <v-card-text v-if="post.media">
            <v-img :src="$store.state.server+'/storage/images/'+post.media" width="100%"></v-img>
          </v-card-text>
          <v-divider/>
          <v-card-actions class="pb-3 pl-4">
            <!-- like button -->
            <div class="d-flex align-center">
              <v-icon :color='hasUserLiked(post)'>
                mdi-thumb-up
              </v-icon>
            </div>
            <span class="mr-3" style="font-size: 10px">{{post.likes_count}}</span>
            <div class="d-flex align-center">
              <v-icon :color='hasUserDisliked(post)'>
                mdi-thumb-down
              </v-icon>
            </div>
            <span class="mr-3" style="font-size: 10px">{{post.dislikes_count}}</span>
            <!-- comment button -->
            <div class="d-flex align-center">
              <v-icon color='black'>
                mdi-comment
              </v-icon>
            </div>
            <span class="mr-3" style="font-size: 10px">{{post.comments_count}}</span>
          </v-card-actions>
        </v-card>
      </div>
      </v-container>
      <v-btn v-if="$store.getters.isLoggedIn" fixed bottom right fab :color='$store.getters.color' class="mx-6 my-10" @click="addPostDialog = true"><v-icon>mdi-plus</v-icon></v-btn>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import moment from 'moment'
  export default {
    name: 'Categories',
    data() {
      return {
        comment: '',
        currentPostIndex: 0,
        currentPost: undefined,
        posts: [],
        category: [],
        currentCategory:this.$attrs.category,
        addPostDialog: false,
        showPostDialog: false,
        showUpload: false,
        newPost:{
          title:'',
          body: ''
        },
        file: '',
        picture: null,
      }
    },
    methods: {
      moment,
      likeCategory(){
        console.log('Like/Unlike',this.currentCategory);
        axios.post(this.$store.state.server+'/api/categories/like/'+this.$store.getters.selectedCategory, {
          auth_token: JSON.stringify(this.$store.getters.token)
        }).then(response => {
          console.log(response.data);
          this.$store.commit('setLikedCategories', response.data.liked_categories);
        }).catch(error => {
          this.error = error.response.data.message
          this.errorDialog = true
        })
      },
      like(post){
        console.log('like',this.$store.getters.token)
        axios.post(this.$store.state.server+'/api/like/'+post.id, {
          auth_token: JSON.stringify(this.$store.getters.token)
        }).then(response => {
          console.log(response);
          this.getPosts()
        }).catch(error => {
          this.error = error.response.data.message
          this.errorDialog = true
        })
      },
      dislike(post){
        console.log('dislike',this.$store.getters.token)
        axios.post(this.$store.state.server+'/api/dislike/'+post.id, {
          auth_token: JSON.stringify(this.$store.getters.token)
        }).then(response => {
          console.log(response);
          this.getPosts()
        }).catch(error => {
          this.error = error.response.data.message
          this.errorDialog = true
        })
      },
      hasUserLiked(post){
        if (post.likes.filter(like => like.user_id === this.$store.getters.user.id).length > 0) {
          return 'blue'
        }else{
          return 'black'
        }
      },
      hasUserDisliked(post){
        if (post.dislikes.filter(dislike => dislike.user_id === this.$store.getters.user.id).length > 0) {
          return 'blue'
        }else{
          return 'black'
        }
      },
      addComment(post){
        axios.post(this.$store.state.server+'/api/comment/'+post.id, {
          auth_token: JSON.stringify(this.$store.getters.token),
          body: this.comment
        }).then( response => {
          console.log(response);
          this.getPosts()
        }
        ).catch(error => {
          this.error = error.response.data.message
          this.errorDialog = true
        }).finally(()=>{
          this.comment = ''
        })
      },
      getPosts(){
        axios.get(this.$store.state.server+'/api/'+this.$store.state.selectedCategory +'/posts').then(response => {
          this.posts = response.data.posts
          this.category = response.data.category
          this.posts.push('')
          this.posts.pop()
          this.currentPost = this.posts[this.currentPostIndex]
          this.scrollToBottom()
        }) 
      },
      calculateWidth(){
        if(document.body.clientWidth > 1000){
          return '50vw'
        }else{
          return '100vw%'
        }  
      },
      openPost(index){
        this.currentPostIndex = index
        this.currentPost = this.posts[index]
        this.showPostDialog = true
        this.scrollToBottom()
      },
      isCategoryLiked(){
        console.log();
        if(this.$store.getters.likedCategories.some(e => e.category_name === this.category.title)){
          console.log('CAT NAME:',this.category.title);
          return 'red'
        }else{
          return 'grey'
        }
      },
      createPost(){
        console.log(this.$store.getters.token)
        axios.post(this.$store.state.server+'/api/posts/create', {
          title: this.newPost.title,
          body: this.newPost.body,
          poster_id: this.$store.getters.user.id,
          category_id: this.category.id,
          auth_token: JSON.stringify(this.$store.getters.token),
          media: this.picture
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
      scrollToBottom(){
          setTimeout(function() {
          const ctr = document.getElementById('scroll')
          if (ctr) {
            ctr.scrollTop = ctr.scrollHeight;
          }
        }, 1);
      },
      handleFileUpload( event ){
        this.file = event.target.files[0];
        this.picture = null
        this.submitFile()
      },
      submitFile(){
        let formData = new FormData();
        formData.append('file', this.file);
        axios.post( this.$store.state.server+'/api/upload',
            formData,
            {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
          }
        ).then(response => {
          this.picture = response.data
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      },
    },
    watch: {
      $attrs(newValue, oldValue) {
        if(oldValue !== this.$store.getters.selectedCategory){
          this.$store.commit('setSelectedCategory', this.$attrs.category)
          this.getPosts()
        }
      }
    },
    mounted () {
      // set selected category on store 
      this.$store.commit('setSelectedCategory', this.$attrs.category)
      // this.$store.state.posts.forEach(post => {
      //   if(post.category === this.$attrs.category){
      //     this.posts.push(post)
      //   }
      // });     
      this.getPosts()
    },
  }
</script>

<style scoped>
@media (min-width: 1264px){
  .container {
      max-width: 627px;
  }
}
@media (min-width: 700px){
  .container {
      max-width: 600px;
  }
}
@media (min-width: 1400px){
  .container {
      max-width: 700px;
  }
}
</style>