<style lang="less">
.Books {
    .item {
        height: 70px; padding-left: 78px;
        // background: red;
        img { position: absolute; top: 0; left: 0; width: 70px; height: 70px; border-radius: 5px; }
        h3 { margin: 0; font-size: 16px; }
        .isbn { font-size: 12px; }
        a {
            position: absolute; top: 23px; right: 0;
            width: 5em; height: 24px; border-radius: 12px;
            text-align: center; color: #fff;
        }
        a.status-1 { background: cornflowerblue; }
        a.status-0 { background: darkgoldenrod; }
    }
}
</style>
<template>
<div class="Books">
    <VanSearch v-model="keyword" placeholder="请输入书名/ISBN/条形码" @search="doSearch(0)"/>
    <VanDropdownMenu>
        <VanDropdownItem v-model="age" :options="ages"/>
        <VanDropdownItem v-model="topic" :options="topics"/>
        <VanDropdownItem v-model="lang" :options="langEnTypes"/>
    </VanDropdownMenu>
    <VanList v-model="loading" :finished="finished" @load="doSearch">
        <VanCell v-for="b in data" :key="b.id">
            <div class="item">
                <img :src="b.photo" alt="图书封面"/>
                <h3>{{ b.name }}</h3>
                <div class="isbn">ISBN: {{ b.isbn }}</div>
                <a href="javascript:" :class="'status-' + b.status">借出</a>
            </div>
        </VanCell>
    </VanList>
</div>
</template>
<script>
import { ages, topics, langEnTypes } from '@/图书/common';
import { ajaxLoad } from '@/图书/ajax';

/* eslint-disable */
const getBookLend = {"statusCode":0,"message":"success","data":{"tatalBorrowSum":638.3,"bookTotal":20,"bookData":[{"lend_seq":26280590,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"妈妈，你在哪儿？","isbn":"9787505632004","barcode":"38630012186","book_id":566344,"cover_photo":"http:\/\/cdn.yourbay.net\/ybbooklib\/faceimages\/200423\/a3c3h3w4p_w.jpg","price":34,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":2197115,"category_id":566344,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280591,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"可爱动物操（启发）","isbn":"9787543474260","barcode":"38630018706","book_id":951120,"cover_photo":"http:\/\/cdn.yourbay.net\/ybbooklib\/bookimgs\/old_system\/book-82-cover.jpg","price":32.8,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":2192908,"category_id":951120,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280592,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"彼得与狼","isbn":"9787537667210","barcode":"38630017228","book_id":69142,"cover_photo":"http:\/\/cdn.yourbay.net\/ybbooklib\/bookimgs\/OBImg\/20140115\/3281404.jpg","price":29.8,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":2194326,"category_id":69142,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280593,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"100层的巴士","isbn":"9787556829293","barcode":"38630014623","book_id":69854,"cover_photo":"http:\/\/cdn.yourbay.net\/ybbooklib\/faceimages\/190722\/caoedzfas_w.jpg","price":35,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":2194039,"category_id":69854,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280594,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"小猫鱼系列：成了晚餐的小猫鱼","isbn":"9787556818839","barcode":"38630024196","book_id":1210130,"cover_photo":"http:\/\/cdn.yourbay.net\/ybkidsreader\/faceimages\/thumb_1571881658701.jpeg","price":20,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":5289921,"category_id":1210130,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280595,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"包公审石头","isbn":"9787545062601","barcode":"38630001081","book_id":1307732,"cover_photo":"http:\/\/cdn.yourbay.net\/ybkidsreader\/faceimages\/thumb_1577173490549.jpeg","price":39.8,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":5335005,"category_id":1307732,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280596,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"外星人爱内裤","isbn":"9787538575415","barcode":"38630013046","book_id":456559,"cover_photo":"http:\/\/cdn.yourbay.net\/ybbooklib\/bookimgs\/OBImg\/20130716\/3154540.jpg","price":28,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":2198561,"category_id":456559,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280597,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"乐乐趣绘本馆 好长好长的蛇","isbn":"9787545041064","barcode":"38630017907","book_id":172547,"cover_photo":"http:\/\/cdn.yourbay.net\/ybkidsreader\/faceimages\/thumb_1537863030240.jpeg","price":29.8,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":2193813,"category_id":172547,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280598,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"不管怎样","isbn":"9787534656255","barcode":"38630012018","book_id":68304,"cover_photo":"http:\/\/cdn.yourbay.net\/ybbooklib\/faceimages\/180905\/w2djf8fxt_w.png","price":28,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":2197924,"category_id":68304,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2},{"lend_seq":26280599,"lend_time":"2020-09-13 10:21:43","return_time":null,"booktitle":"外星人爱圣诞内裤","isbn":"9787538575422","barcode":"38630012315","book_id":456561,"cover_photo":"http:\/\/cdn.yourbay.net\/ybbooklib\/bookimgs\/OBImg\/20130716\/3154542.jpg","price":28,"owner_lib_id":3863,"storage_state":2,"book_status":1,"storage_id":2198422,"category_id":456561,"title":"北京悠贝朝阳未来广场双语馆","fudd":"朝阳区北四环东路73号未来广场四层英华公学国际早教中心","lendDay":2}],"borrowTimes":62}};
const list = getBookLend.data.bookData.map(b => ({
    id: b.book_id,
    name: b.booktitle,
    isbn: b.isbn,
    photo: b.cover_photo,
    status: b.return_time ? 1 : 0,
}));
/* eslint-enable */

export default {
    name: 'Books',
    data() {
        return {
            // 搜索区域
            keyword: '',
            age: '',
            topic: '',
            lang: '',
            // 加载区域
            loading: false, finished: true,
            data: list,
            ages: [{ text: '年龄筛选', value: '' }].concat(ages),
            topics: [{ text: '主题分类', value: '' }].concat(topics),
            langEnTypes: [{ text: '语言筛选', value: '' }].concat(langEnTypes),
        };
    },
    methods: {
        doSearch() {
            const vm = this;
            ajaxLoad(vm, '图书数据', Vue.http.get('/rd/books'));
        },
    },
    created() {
        this.doSearch();
    },
};
</script>
