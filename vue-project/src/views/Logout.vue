<template>
  <h1 class="text-center pt-10">You have successfully logged out!</h1>
</template>

<script>
  export default {
    name: 'Logout',
    data() {
      return {
      }
    },
    methods: {
      logout() {
        this.$store.commit('setIsLoggedIn', false)
        this.$store.commit('setUser', '')
        this.$store.commit('setToken', '')
        this.$store.commit('setLikedCategories', [])
        document.cookie = 'auth_token=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      },
    },
    mounted () {
      this.logout()
    },
  }
</script>
