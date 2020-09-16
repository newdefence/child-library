<style lang="less">
.Users {
    .item {
        position: relative;
        .avatar {
            position: absolute;
            img { width: 44px; height: 44px; border-radius: 100%; }
            i {
                position: absolute; right: 3px; bottom: 3px; width: 16px; height: 16px;
                background: url(../imgs/男.png) 0 0 / contain no-repeat;
            }
            i.女 { background-image: url(../imgs/女.png); }
        }
        h3 { height: 22px; margin: 0 0 0 50px; font-size: 16px; line-height: 22px; color: #333; }
        .age {
            display: inline-block; padding: 0 5px; margin-left: 10px;
            font-size: 12px; font-weight: normal; line-height: 16px; color: #fe9700;
            background: #fff3e6; border-radius: 6px;
        }
        .info {
            display: flex; padding-left: 50px; justify-content: space-between;
            b { color: #ff9528; }
        }

        .actions { display: flex; justify-content: space-between; }
        .actions .van-icon { margin-right: 3px; line-height: 24px; }
        .action-record { color: #ff9528; }
        .action-borrow { color: #bfbfbf; }
    }
}
</style>

<template>
<div class="Users">
    <VanSearch v-model="keyword" placeholder="请输入会员名称/手机号/家长姓名" @search="doSearch(0)"/>
    <div>有效会员{{ total }}人</div>
    <VanList v-model="loading" :finished="finished" @load="doSearch">
        <VanCell v-for="b in data" :key="b.id">
            <div class="item">
                <div class="avatar">
                    <img :src="b.photo" alt="头像"/>
                    <i :class="b.gender"/>
                </div>
                <h3>{{ b.childName }}<b class="age">{{ b.age }}</b></h3>
                <div class="info">
                    <div>{{ b.card }} 距离到期日<b>{{ b.untilEndTime || 0 }}</b>天</div>
                    <div>在读图书<b>{{ b.readingBookNum }}</b>本</div>
                </div>
                <!-- TODO: 功能待开发 -->
                <div>备注：点击填写备注</div>
                <div class="actions">
                    <div class="action-record"><VanIcon name="notes-o" />借阅纪录</div>
                    <div class="action-borrow" @click="b1 = { show: true }"><VanIcon name="edit" />扫码枪借书</div>
                </div>
            </div>
        </VanCell>
    </VanList>
    <VanDialog v-if="b1" v-model="b1.show" title="条形码输入" showCancelButton
        @confirm="addBorrowCode" @closed="b1 = null;">
        <VanField v-model="b1.code" label="条形码：" placeholder="请输入条形码"/>
    </VanDialog>
</div>
</template>
<script>
/* eslint-disable */
const getBookLend = {"statusCode":0,"message":"success","data":{"memberList":[{"id":3130304,"jgid":3863,"uid":680552,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":146947,"cardno":"30051743a13811855993","activedjgid":3863,"lend_time":"2020-09-13 10:21:43","return_time":"2020-09-13 11:17:59","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-11-24","childId":680552,"renewal_type":0,"begintime":"2018-11-22","update_time":"0000-00-00 00:00:00","child_name":"朱柯馨","age":"4.3","birthday":"2016-06-09","gender":2,"relationship":503,"mobile":"13811855993","nickname":"朱柯馨","faceimg":"https:\/\/scdn.yourbay.net\/wxFaceUrlConvert\/680551.jpg","days":69,"readingBookNum":20},{"id":3897851,"jgid":3863,"uid":809321,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":169061,"cardno":"479541435j18610911826","activedjgid":3863,"lend_time":"2020-08-16 14:30:10","return_time":"2020-08-16 19:59:29","stopcard_start_time":null,"remarks":"12月23日办卡，于2019年1月1日开始使用","stopcard_end_time":null,"endtime":"2021-03-01","childId":809321,"renewal_type":0,"begintime":"2019-01-01","update_time":"0000-00-00 00:00:00","child_name":"周飞彤","age":"3.6","birthday":"2017-02-18","gender":2,"relationship":503,"mobile":"18610911826","nickname":"周飞彤","faceimg":"https:\/\/scdn.yourbay.net\/wxFaceUrlConvert\/809320.jpg","days":166,"readingBookNum":16},{"id":9502370,"jgid":3863,"uid":1863350,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":344572,"cardno":"242631509f","activedjgid":3863,"lend_time":"2020-08-09 12:46:56","return_time":"2020-08-11 18:51:20","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-12-01","childId":1863350,"renewal_type":0,"begintime":"2019-12-01","update_time":"0000-00-00 00:00:00","child_name":"王禹兮","age":"3.4","birthday":"2017-05-04","gender":2,"relationship":503,"mobile":"18622490595","nickname":"张曦元","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":76,"readingBookNum":24},{"id":9454791,"jgid":3863,"uid":1738387,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":328242,"cardno":"569414342y","activedjgid":3863,"lend_time":"2020-08-11 18:12:06","return_time":"2020-08-11 18:46:14","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-11-07","childId":1738387,"renewal_type":0,"begintime":"2019-11-07","update_time":"0000-00-00 00:00:00","child_name":"李佳倪","age":"3.5","birthday":"2017-03-17","gender":2,"relationship":503,"mobile":"13520393999","nickname":"李家倪","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":52,"readingBookNum":9},{"id":9447095,"jgid":3863,"uid":1704176,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":325814,"cardno":"777974447x","activedjgid":3863,"lend_time":"2020-08-02 10:27:46","return_time":"2020-08-08 22:06:18","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-11-02","childId":1704176,"renewal_type":0,"begintime":"2019-11-02","update_time":"0000-00-00 00:00:00","child_name":"魏小亨","age":"1.6","birthday":"2019-02-23","gender":1,"relationship":502,"mobile":"13601218641","nickname":"魏小亨","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":47,"readingBookNum":0},{"id":8130450,"jgid":3863,"uid":1224860,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":249667,"cardno":"56325458e","activedjgid":3863,"lend_time":"2020-08-02 10:49:45","return_time":"2020-08-02 14:33:07","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-09-19","childId":1224860,"renewal_type":0,"begintime":"2019-05-19","update_time":"0000-00-00 00:00:00","child_name":"张洺赫","age":"4.6","birthday":"2016-02-14","gender":1,"relationship":503,"mobile":"18001166637","nickname":"唐平","faceimg":"https:\/\/scdn.yourbay.net\/wxFaceUrlConvert\/1224859.jpg","days":3,"readingBookNum":34},{"id":9246798,"jgid":3863,"uid":1369577,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":274266,"cardno":"798255728i","activedjgid":3863,"lend_time":"2020-05-02 14:42:53","return_time":"2020-08-01 11:57:19","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2021-02-07","childId":1369577,"renewal_type":0,"begintime":"2019-07-07","update_time":"0000-00-00 00:00:00","child_name":"景恩婕","age":"5.6","birthday":"2015-02-17","gender":2,"relationship":503,"mobile":"13621091396","nickname":"景恩婕","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":144,"readingBookNum":32},{"id":2916248,"jgid":3863,"uid":636472,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":143812,"cardno":"975944739s13661177586","activedjgid":3863,"lend_time":"2020-01-11 10:56:25","return_time":"2020-07-07 13:47:31","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-11-16","childId":636472,"renewal_type":0,"begintime":"2018-11-11","update_time":"0000-00-00 00:00:00","child_name":"刘熙彤","age":"6.0","birthday":"2014-10-05","gender":2,"relationship":502,"mobile":"13661177586","nickname":"刘熙彤","faceimg":"https:\/\/scdn.yourbay.net\/wxFaceUrlConvert\/636471.jpg","days":61,"readingBookNum":0},{"id":9569566,"jgid":3863,"uid":2064467,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":364763,"cardno":"747217696y","activedjgid":3863,"lend_time":"2020-01-18 15:36:32","return_time":"2020-07-07 11:40:45","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2021-01-18","childId":2064467,"renewal_type":0,"begintime":"2020-01-18","update_time":"0000-00-00 00:00:00","child_name":"李若溪","age":"3.5","birthday":"2017-04-01","gender":1,"relationship":502,"mobile":"13520013521","nickname":"李若溪","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":124,"readingBookNum":0},{"id":9520947,"jgid":3863,"uid":1925813,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":350285,"cardno":"809307803b","activedjgid":3863,"lend_time":"2020-09-10 18:29:00","return_time":"2020-05-16 15:30:33","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-12-13","childId":1925813,"renewal_type":0,"begintime":"2019-12-13","update_time":"0000-00-00 00:00:00","child_name":"师铭悦","age":"2.2","birthday":"2018-07-11","gender":2,"relationship":503,"mobile":"13552748565","nickname":"师铭悦","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":88,"readingBookNum":50},{"id":9472740,"jgid":3863,"uid":1789522,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":334358,"cardno":"105735216g","activedjgid":3863,"lend_time":"2020-05-09 16:36:05","return_time":"2020-05-09 16:35:51","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-11-16","childId":1789522,"renewal_type":0,"begintime":"2019-11-16","update_time":"0000-00-00 00:00:00","child_name":"刘一丁（李莫）","age":"4.2","birthday":"2016-07-13","gender":1,"relationship":503,"mobile":"13720095167","nickname":"李莫","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":61,"readingBookNum":10},{"id":9388278,"jgid":3863,"uid":1574878,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":308034,"cardno":"312530813a","activedjgid":3863,"lend_time":"2020-01-18 11:45:36","return_time":"2020-05-05 21:18:20","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-10-05","childId":1574878,"renewal_type":0,"begintime":"2019-09-19","update_time":"0000-00-00 00:00:00","child_name":"杨懿涵","age":"4.0","birthday":"2016-09-04","gender":2,"relationship":503,"mobile":"13159950220","nickname":"杨懿涵","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":19,"readingBookNum":2},{"id":9386056,"jgid":3863,"uid":1571602,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":307379,"cardno":"11111049e","activedjgid":3863,"lend_time":"2020-01-12 11:42:16","return_time":"2020-05-02 14:40:03","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-09-22","childId":1571602,"renewal_type":0,"begintime":"2019-09-22","update_time":"0000-00-00 00:00:00","child_name":"王恩庆","age":"3.8","birthday":"2016-11-24","gender":1,"relationship":503,"mobile":"13466404899","nickname":"王恩庆","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":6,"readingBookNum":0},{"id":2572140,"jgid":3863,"uid":583846,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":138504,"cardno":"649490622i18910980721","activedjgid":3863,"lend_time":"2020-01-11 15:34:31","return_time":"2020-01-11 15:34:48","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-11-03","childId":583846,"renewal_type":0,"begintime":"2018-10-25","update_time":"0000-00-00 00:00:00","child_name":"郭宥初","age":"4.0","birthday":"2016-10-04","gender":1,"relationship":503,"mobile":"18910980721","nickname":"郭宥初","faceimg":"https:\/\/scdn.yourbay.net\/wxFaceUrlConvert\/583845.jpg","days":48,"readingBookNum":2},{"id":9330715,"jgid":3863,"uid":1475285,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":291403,"cardno":"918468294o","activedjgid":3863,"lend_time":"2019-10-24 15:01:45","return_time":"2019-10-24 15:30:42","stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-11-18","childId":1475285,"renewal_type":0,"begintime":"2019-08-18","update_time":"0000-00-00 00:00:00","child_name":"朱璟旭","age":"3.1","birthday":"2017-08-29","gender":1,"relationship":503,"mobile":"13651181795","nickname":"朱璟旭","faceimg":"https:\/\/scdn.yourbay.net\/wxFaceUrlConvert\/1475281.jpg","days":63,"readingBookNum":8},{"id":9716295,"jgid":3863,"uid":2749579,"group_id":600,"cardtype":2,"card_name":"季卡","cardid":423216,"cardno":"789984859k","activedjgid":3863,"lend_time":"2020-09-15 15:52:51","return_time":null,"stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2020-12-15","childId":2749579,"renewal_type":0,"begintime":"2020-09-15","update_time":"0000-00-00 00:00:00","child_name":"韩湘（铮铮）","age":"4.2","birthday":"2016-07-01","gender":1,"relationship":503,"mobile":"13141232176","nickname":"韩湘","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":90,"readingBookNum":8},{"id":9583738,"jgid":3863,"uid":2352799,"group_id":600,"cardtype":1,"card_name":"年卡","cardid":369445,"cardno":"379246419n","activedjgid":3863,"lend_time":null,"return_time":null,"stopcard_start_time":null,"remarks":null,"stopcard_end_time":null,"endtime":"2021-04-20","childId":2352799,"renewal_type":0,"begintime":"2020-04-20","update_time":"0000-00-00 00:00:00","child_name":"国防","age":"0.7","birthday":"2019-12-20","gender":1,"relationship":502,"mobile":"13167358875","nickname":"国防","faceimg":"https:\/\/scdn.yourbay.net\/tst\/ui\/my\/logo.jpeg","days":216,"readingBookNum":0}],"memberTotal":17}};
const list = getBookLend.data.memberList.map(b => ({
    id: b.uid, cardno: b.cardno,
    name: b.nickname, childName: b.child_name, gender: [0, '男', '女'][b.gender],
    age: b.age, photo: b.faceimg,
    card: b.card_name, endtime: b.endtime, // 卡结束时间
    readingBookNum: b.readingBookNum, remarks: b.remarks,
}));
/* eslint-enable */

export default {
    name: 'Users',
    data() {
        return {
            keyword: '',
            total: 0, data: list,
            loading: false, finished: true,
            b1: null, // 条形码输入弹框
        };
    },
    methods: {
        doSearch() {},
        addBorrowCode() {},
    },
};
</script>
