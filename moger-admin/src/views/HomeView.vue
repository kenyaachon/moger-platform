<script setup lang="ts">
import axios from 'axios'
import { Auth } from 'aws-amplify'

async function testMogerProxy() {
  const mogerProxyrEGION = import.meta.env.VITE_REGION
  console.log(`region for moger proxy ${mogerProxyrEGION}`)
  const apiURL = `${import.meta.env.VITE_MOGER_PROXY_API}/eks/scale-up`
  console.log(`url for moger proxy ${apiURL}`)
  const authSession = await Auth.currentSession()
  const token = authSession.getAccessToken().getJwtToken()
  const { data } = await axios.post(apiURL, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  console.log(`data from api request ${data}`)
}
</script>

<template>
  <h3>Hello this is the home page</h3>
  <button @click="testMogerProxy">Test API</button>
</template>
