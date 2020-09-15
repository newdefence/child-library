<style lang="less">
h1 { margin: 0; font-size: 20px; line-height: 36px; text-align: center; }
.Rd-Scan {
    position: fixed; bottom: 64px; left: 50%;
    width: 140px; height: 36px; margin-left: -70px;
    line-height: 36px; text-align: center; color: #fff;
    background: linear-gradient(90deg,#ffa232,#ff8017);
    border-radius: 18px;
    box-shadow: 0 4px 10px 0 #ffc593;
    .van-icon-scan { margin-right: 5px; line-height: 36px; vertical-align: top; }
}
</style>
<template>
<div class="RD">
    <h1>凯米宝贝双语图书馆</h1>
    <router-view/>
    <div class="Rd-Scan">
        <VanIcon name="scan"/>
        <template>我要还书</template>
    </div>
    <VanTabbar v-model="tab" route>
        <VanTabbarItem name="books" to="/books" icon="home-o">馆藏</VanTabbarItem>
        <VanTabbarItem name="users" to="/users" icon="friends-o">会员</VanTabbarItem>
        <VanTabbarItem name="book" to="/book" icon="add-o">新书</VanTabbarItem>
        <VanTabbarItem name="mine" to="/mine" icon="setting-o">我的</VanTabbarItem>
    </VanTabbar>
</div>
</template>
<script>
export default {
    name: 'RD',
    data() {
        return {
            tab: 'books',
        };
    },
};
</script>
