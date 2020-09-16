// eslint-disable-next-line no-unused-vars
const HA_CONFIG = {
    pages: {
        list: { entry: 'src/视频/list.js', template: 'src/视频/index.html' },
        detail: { entry: 'src/视频/detail.js', template: 'src/视频/index.html' },
    },
    publicPath: '/h5/',
};

// eslint-disable-next-line no-unused-vars
const SA_CONFIG = {
    pages: {
        rd: { entry: 'src/图书/rd/main.js', template: 'src/图书/index.html' },
    },
    publicPath: process.env.NODE_ENV === 'production' ? '' : '',
};

// const CONFIG = HA_CONFIG;
const CONFIG = SA_CONFIG;

module.exports = {
    chainWebpack(config) {
        if (process.env.NODE_ENV === 'production') {
            Object.keys(CONFIG.pages).forEach((key) => {
                config.plugins.delete(`prefetch-${key}`);
                config.plugins.delete(`preload-${key}`);
            });
        }
        config.module.rule('images').use('url-loader').tap((options) => {
            options.limit = 1024 * 10;
            return options;
        });
        config.plugin('copy').tap((args) => {
            args[0][0].ignore.push('static/**', 'img/**', '*.html', 'h5/**');
            return args;
        });
    },
    configureWebpack(config) {
        if (process.env.NODE_ENV === 'production') {
            config.devtool = 'none';
        }
        // eslint-disable-next-line no-param-reassign
        config.externals = {
            vue: 'Vue',
            'vue-router': 'VueRouter',
            vant: 'vant',
        };
    },
    devServer: {
        port: 8999,
        headers: {
            'Access-Control-Allow-Origin': '*',
        },
        proxy: {
            '/api': { target: 'http://test.js' },
        },
    },
    pages: CONFIG.pages,
    css: {
        loaderOptions: {
            less: { strictMath: true },
        },
    },
    productionSourceMap: false,
    publicPath: CONFIG.publicPath,
};
