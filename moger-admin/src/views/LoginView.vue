<script setup lang="ts">
import { Authenticator } from '@aws-amplify/ui-vue'
import { Auth, Hub, Amplify } from 'aws-amplify'
import '@aws-amplify/ui-vue/styles.css'
// import awsconfig from '@/aws-exports'
import awsmobile from '@/aws-exports'

// Amplify.configure(awsconfig)
Amplify.configure(awsmobile)
Hub.listen('auth', async ({ payload }) => {
  console.log(payload)
  try {
    const data = await Auth.currentSession()
    console.log(data)
    console.log(`here is the access token${data.getAccessToken()}`)
  } catch (err) {
    console.log(err)
  }
})
</script>

<template>
  <Authenticator>
    <template v-slot="{ user, signOut }">
      <h1>Hello {{ user.username }}</h1>
      <button @click="signOut">Sign Out</button>
    </template>
  </Authenticator>
</template>
