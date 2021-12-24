<template>
  <v-container>
    <v-card v-for="item in listOfNames" :key="item" width='50vw' class="mt-5">
      <v-card-title >{{item.name}}</v-card-title>
      <v-card-text>My birthday is in {{item.dob}}
      </v-card-text>
      <v-text-field v-model="item.name"></v-text-field>
        <v-btn class="ma-3">Test</v-btn>
    </v-card>
  </v-container>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data: () => ({
      listOfNames: [
        {name: 'tsopanhs', dob: '5/7/1997'},
        {name: 'darras', dob: '5/7/1997'},
        {name: 'Mr.Tortellini', dob: '5/7/1997'},
        {name: 'Pavlidion', dob: '5/7/1997'},
        ]
    })
  }
</script>
