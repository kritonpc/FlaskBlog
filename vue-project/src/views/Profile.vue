<template>
  <div class="about">
    <div>
      {{user}}
    </div>
    <h2>User Color</h2>
    <v-row no-gutters style="width: 170px">
      <template v-for="color,n in colors">
        <v-col :key="n">
          <v-card
            class="pa-1"
            outlined
            :color="selectedColor === color ? 'black' : 'white'"
            tile
            :disabled="selectedColor === color"
            @click="setColor(color)"
          >
            <v-card
            width="30px"
            height="30px"
            class="mx-auto my-auto"
            :color="color"
            />
          </v-card>
        </v-col>
        <v-responsive
          v-if="(n+1) % 4 == 0 "
          :key="`width-${n}`"
          width="100%"
        ></v-responsive>
      </template>
    </v-row>
    <v-card width='400px'>
      <div>
        <h2>Upload Picture</h2>
        <v-img v-if="picture" :src="$store.state.server+'/storage/images/'+picture" width="400" contain></v-img>
        <input accept="image/*" type="file" @change="handleFileUpload( $event )"/>
        <v-btn v-if="file" @click="submitFile()">Upload</v-btn>
        <v-btn v-if="picture" @click="setProfPic()">Set as profile</v-btn>
      </div>
    </v-card>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'Profile',
    data() {
      return{
        user: {},
        file: '',
        selectedColor: '',
        picture: null,
        colors:[
          'blue',
          'blue-grey',
          'brown',
          'cyan',
          'deep-orange',
          'deep-purple',
          'green',
          'grey',
          'indigo',
          'light-blue',
          'light-green',
          'lime',
          'red',
          'teal',
          'yellow',
          'orange',
        ]
      }
    },
    methods: {
      setColor(color) {
        this.selectedColor = color
        this.$store.commit('setColor', color)
        if (this.$store.getters.isLoggedIn) {
          axios.post(this.$store.state.server+'/api/profile/setcolor', {
            auth_token: document.cookie.split('auth_token=')[1],
            color: color
          }).then(response => {
            console.log(response);
          })
        }
      },
      handleFileUpload( event ){
        this.file = event.target.files[0];
        this.picture = null
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
      setProfPic(){
        axios.post( this.$store.state.server+'/api/profile/setprofpic', {
          auth_token: document.cookie.split('auth_token=')[1],
          avatar: this.picture
        }).then(response => {
          if (response.data !== 'failed') { 
            this.$store.commit('setUser', response.data)
          }
        })
      }
    },
    mounted () {
      axios.post(this.$store.state.server+'/api/profile/', {
        auth_token: document.cookie.split('auth_token=')[1]
      }).then(response => {
        this.user = response.data
        this.selectedColor = this.user.color
      }).catch(error => {
        this.error = error.response.data.message
        this.errorDialog = true
      })
    },
  }
</script>
