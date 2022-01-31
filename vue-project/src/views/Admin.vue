<template>
  <div v-if="$store.getters.isAdmin">
    <v-dialog v-model="addCategoryDialog" width="40vw">
      <v-card class="pa-4">
        <v-text-field
          v-model="newCategoryTitle"
          label="Title"
          required
        ></v-text-field>
        <v-textarea
          v-model="newCategoryDescription"
          label="Description"
          required
        ></v-textarea>
        <span>Category Image</span>
        <UploadImage @uploaded="changePic" />
        <div class="d-flex">
          <v-spacer />
          <v-btn type="submit" @click="addCategory">Add</v-btn>
        </div>
      </v-card>
    </v-dialog>
    <v-dialog v-model="removeCategoryDialog" width="40vw">
      <v-card>
        <v-toolbar flat :color="$store.getters.color">
          <v-toolbar-title>Remove Category by Id</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click.native="removeCategoryDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text class="pa-4">
          <v-text-field
            v-model="categoryId"
            label="Category Id"
            required
          ></v-text-field>
          <div class="d-flex">
            <v-spacer />
            <v-btn type="submit" @click="removeCategory">Remove</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="removePostDialog" width="40vw">
      <v-card>
        <v-toolbar flat :color="$store.getters.color">
          <v-toolbar-title>Remove Post by Id</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click.native="removePostDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text class="pa-4">
          <v-text-field
            v-model="postId"
            label="Post Id"
            required
          ></v-text-field>
          <div class="d-flex">
            <v-spacer />
            <v-btn type="submit" @click="removePost">Remove</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
    <div class="mt-3 d-flex px-10">
      <v-card rounded="xl" class="pa-4 text-center" width="300px">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              @click="addCategoryDialog = true"
              :color="$store.getters.color"
              class="mx-2"
              fab
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-card-plus</v-icon>
            </v-btn>
          </template>
          <span>Add Category</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              @click="removeCategoryDialog = true"
              :color="$store.getters.color"
              class="mx-2"
              fab
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-card-remove</v-icon>
            </v-btn>
          </template>
          <span>Remove Category</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              @click="removePostDialog = true"
              :color="$store.getters.color"
              class="mx-2"
              fab
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-note-remove</v-icon>
            </v-btn>
          </template>
          <span>Remove Post</span>
        </v-tooltip>
      </v-card>
      <v-spacer />
      <h2 class="my-auto">Administrator Dashboard</h2>
      <v-spacer />
      <v-card rounded="xl" class="pa-4 ma-0" width="300px">
        <v-slider
          v-model="cols"
          :tick-labels="ticksLabels"
          min="-3"
          max="-1"
          step="1"
          ticks="always"
          tick-size="4"
        ></v-slider>
      </v-card>
    </div>
    <v-row class="mt-4">
      <v-col :cols="12 / -cols">
        <v-card class="mx-10">
          <v-card-title class="justify-center"> Categories </v-card-title>
          <v-data-table
            :headers="categoryHeaders"
            :items="$store.getters.categories"
            :items-per-page="5"
            class="elevation-0"
          ></v-data-table>
        </v-card>
      </v-col>
      <v-col :cols="12 / -cols">
        <v-card class="mx-10">
          <v-card-title class="justify-center"> Users </v-card-title>
          <v-data-table
            :headers="usersHeaders"
            :items="users"
            :items-per-page="5"
            class="elevation-0"
          ></v-data-table>
        </v-card>
      </v-col>
      <v-col :cols="12">
        <v-card class="mx-10">
          <v-card-title class="justify-center"> Posts </v-card-title>
          <v-data-table
            :headers="postsHeaders"
            :items="posts"
            :items-per-page="5"
            class="elevation-0"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";
import UploadImage from "@/components/UploadImage";
export default {
  name: "Admin",
  components: {
    UploadImage,
  },
  data() {
    return {
      removeCategoryDialog: false,
      removePostDialog: false,
      categoryId: "",
      postId: "",
      addCategoryDialog: false,
      newCategoryTitle: "",
      newCategoryDescription: "",
      picUrl: "",
      users: [],
      posts: [],
      cols: -2,
      ticksLabels: ["Small", "Medium", "Large"],
      categoryHeaders: [
        { text: "Id", value: "id" },
        { text: "Title", value: "title" },
        { text: "Description", value: "description" },
        { text: "Likes", value: "likes_count" },
        { text: "Posts", value: "posts_count" },
      ],
      usersHeaders: [
        { text: "Id", value: "id" },
        { text: "Username", value: "username" },
        { text: "Nickname", value: "nickname" },
        { text: "Avatar", value: "avatar" },
      ],
      postsHeaders: [
        { text: "Id", value: "id" },
        { text: "Category", value: "category" },
        { text: "Title", value: "title" },
        { text: "Body", value: "body" },
        { text: "Poster", value: "poster_id" },
        { text: "Likes", value: "likes_count" },
        { text: "Dislikes", value: "dislikes_count" },
        { text: "Comments", value: "comments_count" },
      ],
    };
  },
  mounted() {
      this.fetch()
  },
  methods: {
    fetch() {
      axios
        .get(this.$store.state.server + "/api/admin/users")
        .then((response) => {
          this.users = response.data;
        });
      axios
        .get(this.$store.state.server + "/api/admin/posts")
        .then((response) => {
          this.posts = response.data;
        });
    },
    changePic(url) {
      this.picUrl = url;
    },
    addCategory() {
      axios
        .post(this.$store.state.server + "/api/admin/new/category", {
          auth_token: document.cookie.split("auth_token=")[1],
          title: this.newCategoryTitle,
          description: this.newCategoryDescription,
          image: this.picUrl,
          banner: this.picUrl,
        })
        .then(() => {
          this.addCategoryDialog = false;
          this.newCategoryTitle = "";
          this.newCategoryDescription = "";
          this.picUrl = "";
        })
        .finally(() => {
            this.fetch()
        })
    },
    removeCategory() {
      axios
        .post(this.$store.state.server + "/api/admin/remove/category", {
          auth_token: document.cookie.split("auth_token=")[1],
          category_id: this.categoryId,
        })
        .then(() => {
          this.removeCategoryDialog = false;
          this.categoryId = "";
        })
        .finally(() => {
            this.fetch()
        })
    },
    removePost() {
      axios
        .post(this.$store.state.server + "/api/admin/remove/post", {
          auth_token: document.cookie.split("auth_token=")[1],
          post_id: this.postId,
        })
        .then(() => {
          this.removePostDialog = false;
          this.postId = "";
        })
        .finally(() => {
            this.fetch()
        })
    },
  },
};
</script>
