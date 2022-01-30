<template>
  <div>
    <v-img v-if="picture" :src="$store.state.server+'/storage/images/'+picture" width="400" contain></v-img>
    <input accept="image/*" type="file" @change="handleFileUpload( $event )"/>
    <!-- <v-btn v-if="file" @click="submitFile()">Upload</v-btn>
    <v-btn v-if="picture" @click="setProfPic()">Set as profile</v-btn> -->
  </div>
</template>

<script>
import axios from "axios";
  export default {
    name: 'UploadImage',
    data() {
        return {
            file: '',
            picture: null,
        }
    },
    methods: {
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
          this.$emit('uploaded', response.data)
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      },
    },
  }
</script>
