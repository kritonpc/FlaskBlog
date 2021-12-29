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
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'Profile',
    data() {
      return{
        user: {},
        selectedColor: '',
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
      }
    },
    mounted () {
      axios.post(this.$store.state.server+'/api/profile/', {
        auth_token: JSON.stringify(this.$store.getters.token)
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
