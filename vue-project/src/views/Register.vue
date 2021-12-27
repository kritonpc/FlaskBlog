<template>
    <div class="text-center">
        <v-dialog width='40vw' v-model="successDialog">
            <v-card>
                <v-card-title class='justify-center'>
                    You have succesfully registered!
                </v-card-title>
                <v-card-actions class="justify-center">
                    <v-btn class="ma-2" @click="$router.push('/login')">Login</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog width='40vw' v-model="errorDialog">
            <v-card>
                <v-card-title class='justify-center'>
                    <span>There was an error registering you! Please check your credentials and try again.</span>
                </v-card-title>
                <v-card-actions class="justify-center">
                    <v-btn class="ma-2" @click="errorDialog=false">Login</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-card width="50vw" class="mx-auto my-10">
            <v-card-title>Register</v-card-title>
            <v-card-text>
                <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                >
                    <v-text-field
                        v-model="username"
                        :rules="nameRules"
                        label="Username"
                        required
                    ></v-text-field>
                    <v-text-field
                        v-model="nickname"
                        :rules="nicknameRules"
                        placeholder="How do you want people to call you?"
                        label="Nickname"
                        required
                    ></v-text-field>
                    <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    label="E-mail"
                    required
                    ></v-text-field>
                    <v-text-field
                    v-model="password"
                    :rules="passwordRules"
                    type="password"
                    label="Password"
                    required
                    ></v-text-field>
                    <v-text-field
                    v-model="password_confirmation"
                    :rules="confirmPasswordRules"
                    type="password"
                    label="Confirm Password"
                    required
                    ></v-text-field>
                    <!-- date of birth -->
                    <v-menu
                        ref="menu"
                        v-model="menu"
                        :close-on-content-click="false"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                        >
                        <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                            v-model="dob"
                            label="Birthday date"
                            prepend-icon="mdi-calendar"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            ></v-text-field>
                        </template>
                        <v-date-picker
                            v-model="dob"
                            :active-picker.sync="activePicker"
                            :max="(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)"
                            min="1950-01-01"
                            @change="save"
                        ></v-date-picker>
                        </v-menu>
                    <v-radio-group 
                        label="Gender: "
                        v-model="gender"
                        row
                        :rules="[v => v !== undefined || 'Item is required']"
                    >
                        <v-radio
                            label="Male"
                            :value="true"
                        >
                        </v-radio>
                        <v-radio
                            label="Female"
                            :value="false"
                        >
                        </v-radio>
                        <v-radio
                            label="Other"
                            :value="null"
                        >
                        </v-radio>
                    </v-radio-group>
                    <v-textarea v-model="description" outlined label="A few words about you"></v-textarea>
                    <v-btn
                        :disabled="!valid"
                        color="success"
                        class="mr-4"
                        @click="validate"
                        >
                        Validate
                    </v-btn>
                </v-form>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios'
import crypto from 'crypto'
export default {
  name: 'Register',
    watch: {
      menu (val) {
        val && setTimeout(() => (this.activePicker = 'YEAR'))
      },
    },
    data() {
    return {
        activePicker: null,
        menu: false,
        successDialog: false,
        errorDialog: false,
        username: '',
        password: '',
        password_confirmation: '',
        email: '',
        description: '',
        gender: null,
        dob: '',
        nickname: '',
        valid: true,
        nameRules: [
            v => !!v || 'Username is required',
            v => !(/[ ]/.test(v)) || 'No spaces allowed',
            v => (v && v.length <= 20) || 'Name must be less than 10 characters',
        ],
        nicknameRules: [
            v => !!v || 'Nickname is required',
            v => (v && v.length <= 20) || 'Name must be less than 10 characters',
        ],
        emailRules: [
            v => !!v || 'E-mail is required',
            v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
        ],
        passwordRules: [
        (value) => !!value || 'Please type password.',
        (value) => (value && value.length >= 6) || 'Minimum 6 characters required.',
        ],
        confirmPasswordRules: [
            (value) => !!value || 'Please confirm your password',
            (value) =>
            value === this.password || 'The password confirmation does not match.',
        ],
    }
  },
  methods: {
      save (dob) {
        this.$refs.menu.save(dob)
      },
      validate () {
        //   password hash with sha-256
        if (this.$refs.form.validate()){
            axios.post(this.$store.state.server+'/api/register', {
                username: this.username,
                nickname: this.nickname,
                gender: this.gender,
                password: crypto.createHash('sha256').update(this.password).digest('hex'),
                email: this.email,
                description: this.description,
                dob: this.dob,
                
        }).then(response => {
            if (response.data === 'success') {
                this.successDialog = true
            }else{
                this.errorDialog = true
            }
            // this.$router.push('/login')
        })
        }
        
      },
  },
}
</script>
