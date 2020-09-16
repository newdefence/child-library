import Vue from 'vue';
import VueRouter from 'vue-router';

import '@/components/VanSelect.less';
import '@/components/VanSelect';

import App from './Main.vue';
import Books from './Books.vue';
import Users from './Users.vue';
import Mine from './Mine.vue';
import Book from './Book.vue';

// Vue.config.productionTip = false;

const routes = [
    { path: '/', redirect: '/books' },
    { path: '/books', component: Books },
    { path: '/book/:id', component: Book, props: true },
    { path: '/users', component: Users },
    { path: '/mine', component: Mine },
];

new Vue({
    router: new VueRouter({ routes }),
    render: (h) => h(App),
}).$mount('#app');
