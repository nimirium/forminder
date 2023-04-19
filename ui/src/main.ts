import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './assets/main.css'

/* import the fontawesome core */
// @ts-ignore
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
// @ts-ignore
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
// @ts-ignore
import { faBars, faCopy } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faBars, faCopy);

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
