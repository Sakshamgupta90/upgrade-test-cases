import Vue from 'vue';
import VueRouter from 'vue-router';
import axios from 'axios';
import App from './App.vue';

Vue.use(VueRouter);
Vue.config.productionTip = false;
Vue.prototype.$http = axios;

Vue.filter('currency', (value) => `$${Number(value).toFixed(2)}`);

export const bus = new Vue();

const Home = { render: (h) => h('p', 'Welcome to the shop') };

const router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '/', component: Home },
    { path: '*', redirect: '/' },
  ],
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
