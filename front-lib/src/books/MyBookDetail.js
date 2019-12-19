import React, { Component,Fragment } from 'react';
import { Descriptions, Spin, Button, Divider } from 'antd';
import MyHostPost from "../util/MyHostPost";
import MyNotification from "../util/MyNotification";
import MyUserTokenManager from "../util/MyUserTokenManager";


class MyBookDetail extends Component {

    constructor(props) {
        super(props);

        this.state = {
            loading:false,

            id: null,
            title: null,
            author: null,
            description: null,
            content: null,
            isBorrow: true,
            money: null,
        }
    }

    componentWillMount() {
        let parameters = {
            bookId:this.props.match.params.bookId,
        };
        if(MyUserTokenManager.getUserToken()){
            parameters.userId = MyUserTokenManager.getUserToken().userId;
        }
        this.fetchInfo(parameters);
    }

    fetchInfo = (parameters = {}) => {
        this.setState({loading: true});
        MyHostPost(
            '/search/searchQuery/',
            {...parameters},
            true
        ).then(({json})=>{
            if(json.code === 0){
                const { id, title, author, description, content, isBorrow, money } = json.info[0];
                this.setState({
                    loading:false,
                    id, title, author, description,
                    content, isBorrow, money
                })
            }else
                throw json;
        }).catch((error)=>{
            this.setState({loading:false});
            MyNotification.error('信息请求失败');
            console.log(error);
        });
    };

    handleBookSubscribe = () => {
        const {history} = this.props;
        this.setState({loading: true});
        MyHostPost('/user/bookBorrow/', {
            userId:MyUserTokenManager.getUserToken().userId,
            bookId:this.state.id
        }, true).then(({json})=>{
            if(json.code === 0){
                MyNotification.success('订阅成功');
                this.setState({loading:false});
                history.goBack();
            }else
                throw json;
        }).catch((error)=>{
            this.setState({loading:false});
            MyNotification.error('图书订阅失败');
            console.log(error);
        });
    };

    renderMain = () => {
        const { id, title, author, description, content, money } = this.state;

        return (
            <div style={{margin:'0px 30px'}}>
                <Descriptions
                    bordered={true}
                    column={3}
                >
                    <Descriptions.Item label="ID">{id}</Descriptions.Item>
                    <Descriptions.Item label="书名">{title}</Descriptions.Item>
                    <Descriptions.Item label="作者">{author}</Descriptions.Item>
                    <Descriptions.Item label="计费">{money}</Descriptions.Item>
                    <Descriptions.Item label="描述" span={2}>{description}</Descriptions.Item>
                    <Descriptions.Item label="简介" span={3}>{content}</Descriptions.Item>
                </Descriptions>

                <div>
                    {this.renderSubscribeButton()}
                </div>
            </div>
        );
    };

    renderSubscribeButton = () => {
        const {isBorrow} = this.state;
        let disabled,buttonTitle;

        if(!MyUserTokenManager.getUserToken()){
            disabled=true;
            buttonTitle='未登录，不可订阅';
        }else if(isBorrow){
            disabled=false;
            buttonTitle='可订阅';
        }else {
            // 未借，已登录
            disabled=true;
            buttonTitle='书籍不可订阅';
        }
        return (
            <Button
                style={{
                    float:'right',
                    marginTop:30
                }}
                disabled={disabled}
                type={'primary'}
                onClick={()=>this.handleBookSubscribe()}
            >{buttonTitle}</Button>
        );
    };

    renderLoading = () => {
        return (
            <div style={{
                display:'flex',
                justifyContent:'center',
                alignItems:'center',
                height:'100%',
                width:'100%',
            }}>
                <Spin tip="Loading..."/>
            </div>
        );
    };

    render() {
        const {loading} = this.state;
        return (
            <Fragment>
                <span style={{paddingTop: 20, fontSize:26, marginRight:20}}>
                    我的订阅
                </span>
                <Divider/>
                {loading?this.renderLoading():this.renderMain()}
            </Fragment>
        )
    }

}

export default MyBookDetail;
