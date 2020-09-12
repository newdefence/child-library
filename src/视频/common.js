Vue.url.params = (obj) => {
    const escape = encodeURIComponent;
    let value;
    const array = [];
    // eslint-disable-next-line guard-for-in, no-restricted-syntax
    for (const key in obj) {
        value = obj[key];
        if (value === null) {
            array.push(escape(key) + '=');
        } else if (value !== undefined) {
            array.push(escape(key) + '=' + escape(value));
        }
    }
    return array.join('&').replace(/%20/g, '+');
};

Vue.http.options.emulateJSON = true;

const paddingNumber = (num) => (num > 9 ? '' : '0') + num;

export const duration = (seconds) => {
    if (duration < 60) {
        return '00:' + paddingNumber(seconds);
    }
    if (duration < 3600) {
        return paddingNumber(Math.floor(seconds / 60)) + ':' + paddingNumber(seconds % 60);
    }
    return Math.floor(seconds / 3600) + ':' + paddingNumber(Math.floor((seconds % 3600) / 60)) + ':' + paddingNumber(seconds % 60);
};

const { Toast } = vant;

// const mergeReactiveKeys = (target, source) => {
//     // const ignores = ignoreKeys ? ignoreKeys.split(',') : 0;
//     // Object.keys(source).forEach((key) => {
//     //     // if ((!ignores) || (ignores.indexOf(key) < 0)) {
//     //     Vue.set(target, key, source[key]);
//     //     // }
//     // });
//     for(const key in source) {
//         target[key] = source[key];
//     }
// };

const promiseReject = (title) => (response) => {
    Toast.fail(response.body.msg || (title + '失败'));
};

export const ajaxLoad = (model, title, request, successCallback, finallyCallback) => {
    const promise = request.then ? request : request(model);
    model.loading = true;
    promise.then(({ body }) => {
        if (body.success) {
            // NOTE: 默认不提示
            if (successCallback) {
                successCallback(body, model); // NOTE: 回调参数顺序
            } else {
                // eslint-disable-next-line
                for (const key in body) {
                    model[key] = body[key];
                }
                // mergeReactiveKeys(model, body); // 默认回调行为
            }
        } else {
            Toast.fail(body.msg || (title + '失败'));
        }
    }, promiseReject(title)).finally(() => {
        model.loading = false;
        if (finallyCallback) {
            finallyCallback();
        }
    });
};
export const ajaxPost = (model, title, request, successCallback, finallyCallback, errorCallback) => {
    const promise = request.then ? request : request(model);
    model.loading = true;
    promise.then(({ body }) => {
        if (body.success) {
            // NOTE: 默认提示
            Toast.success(body.msg || (title + '成功'));
            if (successCallback) {
                successCallback(model, body); // NOTE: 回调参数顺序
            }
        } else {
            Toast.fail(body.msg || (title + '失败'));
            if (errorCallback) {
                errorCallback(model, body);
            }
        }
    }, promiseReject(title)).finally(() => {
        model.loading = false;
        if (finallyCallback) {
            finallyCallback();
        }
    });
};

export const generateParams = (source, keys) => {
    const params = {};
    const [mustKeys, optionKeys] = keys.split('|');
    if (mustKeys) {
        mustKeys.split(',').forEach((key) => {
            params[key] = source[key];
        });
    }
    if (optionKeys) {
        optionKeys.split(',').forEach((key) => {
            const value = source[key];
            if (['', null, undefined].indexOf(value) < 0) {
                params[key] = value;
            }
        });
    }
    return params;
};
