const paddingNumber = (num) => (num > 9 ? num : ('0' + num));
const fmtDate = (pickerValue) => [
    pickerValue.getFullYear(),
    paddingNumber(pickerValue.getMonth() + 1),
    paddingNumber(pickerValue.getDate()),
].join('-');
const fmtDatePickerLabel = (value, valueType) => {
    if (value) {
        if (valueType === 'date') {
            return fmtDate(value);
        }
        if (valueType === 'number') {
            return fmtDate(new Date(value));
        }
        return value;
    }
    return '';
};

const Select = {
    inheritAttrs: false,
    data() {
        return { popup: false };
    },
    methods: {
        beforePopup() {},
        beforeConfirm() {},
        popupPicker() {
            this.beforePopup();
            this.popup = true;
        },
        onInput($event) {
            this.popup = $event;
        },
        onCancel() {
            this.popup = false;
        },
        onConfirm($event) {
            this.beforeConfirm($event);
            this.popup = false;
        },
    },
};

const fnSelectValueColumnsChange = (columns, value, vm) => {
    let obj;
    if (vm.valueKey) {
        obj = columns.find((c) => c[vm.valueKey] === value);
        return obj ? obj[vm.labelKey] : null;
        // eslint-disable-next-line
    } else {
        return value || null;
    }
};

Vue.component('VanSelect', {
    name: 'VanSelect',
    extends: Select,
    // inheritAttrs: false,
    // options: ['value1', 'value2']
    // props: ['title', 'columns', 'value'],
    props: {
        // placeholder: String,
        columns: { type: Array, required: true },
        // columnType: { default: 'string' },
        valueKey: String, // 取值的key（与默认api不一样，注意）
        labelKey: { default: 'name' }, // 显示文字的key（不是取值的key)，如果有 valueKey，则默认值是 name
        value: [String, Number],
    },
    data() {
        // const { columns } = this;
        // let columnType = null;
        // if (this.columns) {
        //     columnType = typeof this.columns[0];
        // }
        // const pickerValue = this.value || null;
        // const { valueKey } = this;
        // let pickerLabel = null;
        // let pickerObj;
        // if (valueKey) { // if (pickerValue !== null && pickerValue !== undefined) {
        //     pickerObj = this.columns.find(c => c[valueKey] === pickerValue);
        //     pickerLabel = pickerObj ? pickerObj[this.labelKey] : pickerValue;
        // } else {
        //     pickerLabel = pickerValue;
        // }
        const vm = this;
        return {
            // popup: false,
            // columnType: typeof this.columns[0],
            // pickerValue: this.value || null,
            pickerLabel: fnSelectValueColumnsChange(vm.columns, vm.value || null, vm),
            defaultIndex: 0,
        };
    },
    watch: {
        value(value) {
            const vm = this;
            // const { columns, valueKey } = vm;
            // let obj;
            // if (valueKey) {
            //     obj = columns.find(c => c[valueKey] === value);
            //     vm.pickerLabel = obj ? obj[vm.labelKey] : null;
            // } else {
            //     vm.pickerLabel = value || null;
            // }
            vm.pickerLabel = fnSelectValueColumnsChange(vm.columns, value, vm);
        },
        columns(columns) {
            const vm = this;
            vm.pickerLabel = fnSelectValueColumnsChange(columns, vm.value, vm);
        },
    },
    methods: {
        beforePopup() {
            const vm = this;
            const { columns, valueKey, value } = vm;
            const defaultIndex = valueKey ? columns.indexOf(value) : columns.findIndex((c) => c[valueKey] === value);
            vm.defaultIndex = defaultIndex < 0 ? 0 : defaultIndex;
            // vm.popup = true;
        },
        beforeConfirm($event) {
            const vm = this;
            const { valueKey } = vm;
            vm.pickerLabel = valueKey ? $event[vm.labelKey] : $event;
            vm.$emit('input', valueKey ? $event[valueKey] : $event);
            vm.$emit('change', $event);
            // vm.popup = false;
        },
        // onCancel() {
        //     this.popup = false;
        // },
        // onInput($event) {
        //     this.popup = $event;
        // },
    },
    render(h) {
        const vm = this;
        return h('div', {
            staticClass: 'VanSelect',
            class: { Opening: vm.popup },
            on: { click: vm.popupPicker },
        }, [
            h('VanField', {
                attrs: vm.$attrs,
                props: { value: vm.pickerLabel },
            }),
            h('VanPopup', {
                props: { value: vm.popup, position: 'bottom', getContainer: 'body' },
                on: {
                    input: vm.onInput,
                },
            }, [
                h('VanPicker', {
                    props: {
                        title: '请选择', showToolbar: true,
                        columns: vm.columns, valueKey: vm.valueKey ? vm.labelKey : null,
                        defaultIndex: vm.defaultIndex,
                    },
                    on: {
                        confirm: vm.onConfirm,
                        cancel: vm.onCancel,
                    },
                }),
            ]),
        ]);
    },
});

Vue.component('VanDateSelect', {
    name: 'VanDateSelect',
    extends: Select,
    // inheritAttrs: false,
    props: {
        minDate: Date,
        maxDate: Date,
        value: [String, Number, Date],
        valueType: { default: 'string' }, // 默认显示 yyyy-MM-dd 格式；可选值：number, date
    },
    data() {
        // const { valueType } = this;
        const pickerValue = this.value || null;
        // let pickerLabel = '';
        // if (pickerValue) {
        //     if (valueType === 'date') {
        //         pickerLabel = fmtDate(pickerValue);
        //     } else if (valueType === 'number') {
        //         pickerLabel = fmtDate(new Date(pickerValue));
        //     } else {
        //         pickerLabel = pickerValue;
        //     }
        // }
        return {
            // popup: false,
            pickerValue,
            pickerLabel: fmtDatePickerLabel(pickerValue, this.valueType),
        };
    },
    watch: {
        value(val) {
            this.pickerLabel = fmtDatePickerLabel(val, this.valueType);
            // const vm = this;
            // if (val) {
            //     if (vm.valueType === 'date') {
            //         vm.pickerLabel = fmtDate(vm.pickerValue = val);
            //     } else if (vm.valueType === 'number') {
            //         vm.pickerLabel = fmtDate(vm.pickerValue = new Date(val));
            //     } else {
            //         vm.pickerValue = new Date(vm.pickerLabel = val);
            //     }
            // } else {
            //     vm.pickerLabel = null;
            //     vm.pickerValue = null;
            // }
        },
    },
    methods: {
        beforePopup() {
            const { value } = this;
            // eslint-disable-next-line
            this.pickerValue = value ? (this.valueType === 'date' ? value : new Date(value)) : null;
            // this.popup = true;
        },
        beforeConfirm($event) {
            const vm = this;
            const { valueType } = vm;
            vm.pickerValue = $event;
            vm.pickerLabel = fmtDate($event);
            // eslint-disable-next-line
            vm.$emit('input', valueType === 'string' ? fmtDate($event) : (valueType === 'number' ? +$event : $event));
            // vm.popup = false;
        },
        // onCancel() {
        //     this.popup = false;
        // },
        // onInput($event) {
        //     this.popup = $event;
        // },
    },
    render(h) {
        const vm = this;
        return h('div', {
            staticClass: 'VanDateSelect',
            props: { title: vm.title },
            on: { click: vm.popupPicker },
        }, [
            h('VanField', {
                attrs: vm.$attrs,
                props: { value: vm.pickerLabel },
            }),
            h('VanPopup', {
                props: { value: vm.popup, position: 'bottom', getContainer: 'body' },
                on: {
                    input: vm.onInput,
                },
            }, [
                h('VanDatetimePicker', {
                    props: {
                        type: 'date', value: vm.pickerValue,
                        title: '请选择',
                        minDate: vm.minDate, maxDate: vm.maxDate,
                    },
                    on: {
                        confirm: vm.onConfirm,
                        cancel: vm.onCancel,
                    },
                }),
            ]),
        ]);
    },
});
