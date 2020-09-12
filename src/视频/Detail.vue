<style lang="less">
.Detail {
    video { width: 100%; }
    h2 {
        margin: 0; font-size: 19px; line-height: 27px; color: #111;
        // 控制显示2行，应该不需要控制显示了，要不然没地方完全显示了
        // display: -webkit-box; overflow: hidden; text-overflow: ellipsis; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
    }
    .detail {
        padding: 8px 15px 0; color: #999; border-bottom: 1px solid;
        .time { font-size: 14px; line-height: 32px; }
    }
    .recommend {
        padding: 18px 15px;
    }
    .title1 {
        position: relative; padding: 0 0 8px 7px; margin: 0; font-size: 15px; line-height: 21px;
        &::before { position: absolute; left: 0; top: 4px; height: 12px; content: ''; border-left: 2px solid; }
    }
    .CVideoItem {
        position: relative; display: flex; min-height: 90px; padding: 10px 0; justify-content: space-between;
        border-bottom: 1px solid #eee;
        .poster {
            position: relative; width: 37%; margin: 5px 0 0;
            img { width: 100%; }
            .duration {
                position: absolute; right: 5px; bottom: 5px; padding: 0 4px;
                font-size: 11px; line-height: 19px; color: #fff;
                background: rgba(0, 0, 0, 0.7); border-radius: 2px;
            }
        }
        h3 {
            width: 56%; margin: 0; font-size: 17px; line-height: 23px; color: #333;
            // 控制显示2行
            display: -webkit-box; overflow: hidden; text-overflow: ellipsis; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
        }
        .tags { position: absolute; left: 15px; bottom: 10px; font-size: 12px; color: #999; }
    }
}
</style>
<template>
<div class="Detail">
    <video src=""></video>
    <div class="detail">
        <h2>3种常见食物，却是隐形的“升糖王”，吃一次，血糖飙一次</h2>
        <div class="time">2019-09-10 08:09</div>
    </div>
    <div class="recommend">
        <div class="title1">相关推荐</div>
        <div class="CVideoItem" v-for="c in j1.data" :key="c.wid">
            <h3>{{ v.title }}</h3>
            <div class="poster">
                <img :src="c.video.url" alt="视频封面图"/>
                <span class="duration">{{ c.video.duration | duration }}</span>
            </div>
            <div class="tags">{{ c.categoryName }}</div>
        </div>
    </div>
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
            j0, // { data: [] }
            j1, // { data: [] },
        };
    },
    filters: {
        duration,
    },
    created() {},
};
</script>
