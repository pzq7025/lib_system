import {notification} from 'antd'

const defaultTitle = '温馨提示';

//type 可选 success info warning error
const notify = (type,description,title=defaultTitle) => {
    notification[type]({
        message: title,
        description:description,
        top: 70,
        duration: 2,
    });
};

const success = function(description,title=defaultTitle){
    notify('success',description,title);
};

const info = function(description,title=defaultTitle){
    notify('info',description,title);
};

const warning = function(description,title=defaultTitle){
    notify('warning',description,title);
};

const error = function(description,title=defaultTitle){
    notify('error',description,title);
};


export default {
    success,info,warning,error
};