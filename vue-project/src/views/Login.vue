<template>
    <div class="justify-center text-center">
        <v-dialog width="40vw" overlay-opacity='0.8' v-model='errorDialog'>
            <v-card class="pa-8">
                <h2 class="text-center">There was an error logging in, please try again.</h2>
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
            username: '',
            password: '',
            errorDialog: false,
        }
    },
    methods: {
        login() {
            axios.post(this.$store.state.server+'/api/login', {
                username: this.username,
                password: crypto.createHash('sha256').update(this.password).digest('hex'),
            }).then(response => {
                if(response.data){
                    this.$store.commit('setUser', response.data.user)
                    console.log('auth_token', response.data.auth_token);
                    this.$store.commit('setToken', response.data.auth_token)
                    this.$store.commit('setIsLoggedIn', true)
                    document.cookie = 'auth_token='+JSON.stringify(response.data.auth_token)
                    this.$router.push('/')
                }
                else{
                    this.errorDialog = true
                }
            }).catch(error => {
                this.error = error.response.data.message
                this.errorDialog = true
            }).finally(() => {
                this.loading = false
            })
        }
    },
}
</script>