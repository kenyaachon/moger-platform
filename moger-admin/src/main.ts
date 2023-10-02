import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
// import awsconfig from './aws-exports'
import awsmobile from './aws-exports'
import { Amplify } from 'aws-amplify'
import AmplifyVue from '@aws-amplify/ui-vue'

Amplify.configure(awsmobile)
// Amplify.configure(awsconfig)

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(AmplifyVue)
app.use(createPinia())
app.use(router)

app.mount('#app')
