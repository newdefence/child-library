<template>
<div class="Book">
    <VanForm colon @submit="onSubmit">
        <VanField label="封面" :rules="[{ required: true, message: '请上传封面', validator() { return !!photos[1] }  }]">
            <template #input>
                <VanUploader v-model="photos" :afterRead="afterRead"/>
            </template>
        </VanField>
        <VanField v-model="name" label="书名" placeholder="请输入书名" :rules="[{ required: true, message: '请输入书名' }]"/>
        <VanField v-model="isbn" label="ISBN" placeholder="请输入ISBN" :rules="[{ required: true, message: '请输入ISBN' }]"/>
        <VanField v-model="code" label="条形码" placeholder="请输入条形码" :rules="[{ required: true, message: '请输入条形码' }]"/>
        <VanField v-model="price" type="number" label="图书价格" placeholder="请输入图书价格" :rules="[{ required: true, message: '请输入图书价格' }]"/>
        <VanSelect v-model="age" label="适读年龄" placeholder="请输入适读年龄"
            :columns="ages" valueKey="value" labelKey="text"
            :rules="[{ required: true, message: '请输入适读年龄' }]"/>
        <VanField label="图书分类">
            <template #input>
                <VanCheckboxGroup v-model="topic">
                    <VanCheckbox v-for="t in topics" :key="t.value" :name="t.value">{{ t.text }}</VanCheckbox>
                </VanCheckboxGroup>
            </template>
        </VanField>
        <VanSelect v-model="lang" label="所属语种" placeholder="请输入所属语种"
            :columns="langEnTypes" valueKey="value" labelKey="text"
            :rules="[{ required: true, message: '请输入适读年龄' }]"/>
        <VanField v-model="author" label="作者" placeholder="请输入作者全名" :rules="[{ required: true, message: '请输入作者全名' }]"/>
        <VanField v-model="press" label="出版社" placeholder="请输入出版社" :rules="[{ required: true, message: '请输入出版社' }]"/>
        <VanDateSelect v-model="pubDate" label="出版日期" placeholder="请输入出版日期" :rules="[{ required: true, message: '请输入出版日期' }]"/>
        <VanField v-model="intro" type="textarea" rows="2" autosize label="图书简介" placeholder="请输入图书简介" :rules="[{ required: true, message: '请输入图书简介' }]"/>
        <VanButton round block type="info" native-type="submit">{{ id ? '保存修改' : '上架图书' }}</VanButton>
    </VanForm>
</div>
</template>
<script>
import { ages, topics, langEnTypes } from '@/图书/common';

export default {
    name: 'Book',
    props: {
        id: Number,
    },
    data() {
        return {
            photos: [],
            name: '', isbn: '', code: '', price: null,
            topic: [],
            age: null, lang: '中文',
            author: null, press: null, pubDate: null, intro: null,
            // 下拉框
            ages, topics,
            langEnTypes: [{ text: '中文', value: '中文' }].concat(langEnTypes),
        };
    },
    methods: {
        afterRead(file) {
            console.log('TODO 上传文件：', file);
        },
        onSubmit() {
            // TODO: 保存图书
        },
    },
    created() {
        if (this.id) {
            //
        } else {
            document.title = '新书上架';
        }
    },
};
</script>
