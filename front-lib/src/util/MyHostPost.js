export default function MyHostPost(url,data){
    console.log('send',url);
    return fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'authorization':'bearer',
        },
        body: JSON.stringify(data),
    }).then((response) => {
        return response.json().then((json) => {
            return {json,header:response.headers};
        });
    }).then(({json,header}) => {
        console.log('fetch',json);
        return {json,header};
    });
}