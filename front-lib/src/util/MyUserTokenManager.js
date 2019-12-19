export const StorageMode = {
    local:1,    // use LocalStorage
    session:0   // use SessionStorage
};

/**
 * 用userInfo来指代Token
 * */
export default {
    getUserToken(){
        try{
            if(localStorage.getItem('userInfo')){
                return JSON.parse(localStorage.getItem('userInfo'));
            }else if(sessionStorage.getItem('userInfo')){
                return JSON.parse(sessionStorage.getItem('userInfo'));
            }else
                return null;
        }catch{
            return null;
        }

    },
    setUserToken(mode,userInfo){
        let storage = mode ? localStorage : sessionStorage;
        storage.setItem('userInfo',JSON.stringify(userInfo));
    },
    removeUserToken(){
        localStorage.removeItem('userInfo');
        sessionStorage.removeItem('userInfo');
    },
    updateUserToken(userInfo){
        let storage;
        if(localStorage.getItem('userInfo')){
            storage = localStorage;
        }else if(sessionStorage.getItem('userInfo')){
            storage = sessionStorage;
        }else{
            console.error('updateUserToken ERROR');
            return ;
        }
        storage.setItem('userInfo',userInfo);
    }
}