import './assets/main.css'
import 'mdb-vue-ui-kit/css/mdb.min.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)

app.use(router)
app.use(store)

app.mount('#app')
