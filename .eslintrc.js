module.exports = {
    root: true,
    env: {
        node: true,
    },
    extends: [
        'plugin:vue/essential',
        '@vue/airbnb',
    ],
    globals: {
        Vue: true,
        vant: true,
    },
    parserOptions: {
        parser: 'babel-eslint',
    },
    rules: {
        'import/prefer-default-export': 'off',
        'indent': ['error', 4],
        'max-len': ['error', { code: 240, tabWidth: 4 }],
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-param-reassign': 'off',
        'no-restricted-globals': 'off',
        'object-property-newline': 'off',
        'prefer-template': 'off',
    },
};
