<template>
    <div class="justify-center text-center">
        <v-dialog width="40vw" overlay-opacity='0.8' v-model='errorDialog'>
            <v-card >
                <v-toolbar height="50px" :color="$store.getters.color" flat dark>
                    <v-toolbar-title>Error</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn icon @click.native="errorDialog = false">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-toolbar>
                <v-card-text class="pa-8">
                    <h2 class="text-center">{{errorMessage}}</h2>
                </v-card-text>
            </v-card>
        </v-dialog>
        <v-card class="ma-10 mx-auto pa-5" width="40vw">
        <v-form>
            <v-text-field
                v-model="username"
                type="username"
                label="Username"
                required
            ></v-text-field>
            <v-text-field
                v-model="password"
                type="password"
                label="Password"
                required
            ></v-text-field>
            <v-btn type="submit" @click="login">Login</v-btn>
        </v-form>
        </v-card>
    </div>
</template>
<script>
import axios from 'axios'
import crypto from 'crypto'
export default {
    name: 'Login',
    data() {
        return {
            errorMessage: '',
            username: '',
            password: '',
            errorDialog: false,
        }
    },
    methods: {
        getTextColor(hexcolor){
            hexcolor = hexcolor.replace("#", "");
            var r = parseInt(hexcolor.substr(0,2),16);
            var g = parseInt(hexcolor.substr(2,2),16);
            var b = parseInt(hexcolor.substr(4,2),16);
            var yiq = ((r*299)+(g*587)+(b*114))/1000;
            this.$store.commit('setDarkText', (yiq < 128));
            return (yiq >= 128) ? 'black' : 'white';
        },
        login() {
            axios.post(this.$store.state.server+'/api/login', {
                username: this.username,
                password: crypto.createHash('sha256').update(this.password).digest('hex'),
            }).then(response => {
                if(response.data.success === true){
                    console.log('success');
                    this.$store.commit('setUser', response.data.user)
                    console.log('auth_token', response.data.auth_token);
                    this.$store.commit('setToken', response.data.auth_token)
                    this.$store.commit('setIsLoggedIn', true)
                    this.$store.commit('setColor', response.data.user.color)
                    this.$store.commit('setTextColor', this.getTextColor(response.data.user.color))
                    this.$store.commit('setDarkMode', response.data.user.dark_mode)
                    document.cookie = 'auth_token='+JSON.stringify(response.data.auth_token)
                    this.$router.push('/')
                }
                else{
                    this.errorDialog = true
                    this.errorMessage = response.data.message
                }
            }).catch(error => {
                // console.log(error);
                console.log('resp: ',error.response);
                if (error.response.data.message){
                    this.errorMessage = error.response.data.message
                }else{
                    this.errorMessage = 'There was an error please try again later.'
                }
                this.errorDialog = true
            }).finally(() => {
                this.loading = false
            })
        }
    },
}
</script>