<style lang="less">
.List {
    .van-tab { padding: 0 10px; }
    .CVideoItem {
        padding: 12px 0; margin: 0 15px; border-bottom: 1px solid #eee;
        h3 {
            margin: 0 0 10px; font-size: 18px; line-height: 24px; color: #333;
            // 控制显示2行
            display: -webkit-box; overflow: hidden; text-overflow: ellipsis; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
        }
        .poster {
            position: relative;
            img { width: 100%; }
            .duration {
                position: absolute; right: 10px; bottom: 10px; padding: 0 4px;
                font-size: 11px; line-height: 20px; color: #fff;
                background: rgba(0, 0, 0, 0.7); border-radius: 2px;
            }
        }
        .tags { margin: 10px 0 0; font-size: 12px; color: #999; }
    }
}
</style>
<template>
<div class="List">
    <VanTabs v-model="tab" :ellipsis="false">
        <VanTab v-for="c in j0.data" :key="c.id" :name="c.id" :title="c.name">
            <VanList v-model="c.loading" :finished="c.finished" @load="j1Load(c)">
                <VanCell v-for="v in c.data" :key="v.title" class="CVideoItem">
                    <h3>{{ v.title }}</h3>
                    <div class="poster" @click="goToDetail(v)">
                        <img :src="v.video.cover.url" alt="视频封面图"/>
                        <div class="duration">{{ v.video.duration | duration }}</div>
                    </div>
                    <div class="tags">{{ v.categoryName }}</div>
                </VanCell>
            </VanList>
        </VanTab>
    </VanTabs>
</div>
</template>

<script>
import j0 from '@/v7/res/channel.json';
import j1 from '@/v7/res/list.json';
import { duration } from '@/视频/common';

export default {
    name: 'List',
    data() {
        return {
            tab: null,
            j0, j1,
        };
    },
    filters: {
        duration,
    },
    methods: {
        j1Load() {
            // TODO: 加载数据
        },
        goToDetail(video) {
            location.href = './detail.html?id=' + video.hash;
        },
    },
    created() {
        this.tab = j0.data[0].id;
        j0.data[0].data = j1.data;
    },
};
</script>
