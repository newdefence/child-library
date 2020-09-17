<template>
<div class="Login">
    <VanCellGroup>
        <VanField v-model="phone" label="手机：" placeholder="请输入用户名"/>
        <VanField v-model="passwd" label="密码：" placeholder="请输入密码"/>
        <VanButton round block type="info" @click="doLogin">登录</VanButton>
    </VanCellGroup>
</div>
</template>
<script>
import { ajaxPost } from '@/图书/ajax';

export default {
    name: 'Login',
    data() {
        return { phone: '', passwd: '' };
    },
    methods: {
        doLogin() {
            const vm = this;
            ajaxPost(vm, '登录', Vue.http.post('/rd/login', { phone: vm.phone, passwd: vm.passwd }), () => {
                location.href = '/rd/index.html';
            });
        },
    },
};
</script>
