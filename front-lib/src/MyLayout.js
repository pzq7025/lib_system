import React, { Component } from 'react';
import { Route, Link, Switch} from 'react-router-dom';
import { Layout, Menu, Icon, Avatar, Divider, Dropdown, Tooltip } from 'antd'
import MyBook from './own/MyBook';
import MyInfo from './own/MyInfo'
import MyDefault from './books/MyDefault';
import MySearch from './books/MySearch';
import MyHostPost from "./util/MyHostPost";
import MyNotification from "./util/MyNotification";
import MyBookDetail from './books/MyBookDetail';
import MyLoginModalEx from './auth/MyLoginModalEx'
import history from './route/history'
import {StorageMode} from './util/MyUserTokenManager'
import MyUserTokenManager from './util/MyUserTokenManager'
import 'antd/dist/antd.css'
import './MyLayout.css'

const { Content, Sider } = Layout;
const { SubMenu } = Menu;

class MyLayout extends Component {

    constructor(props) {
        super(props);
        this.state = {
            //组件
            collapsed: false,
            loading: false,

            //用户信息
            userName: '',
            userId: '',
            userInfo:MyUserTokenManager.getUserToken(),

            //登陆
            login: Boolean(MyUserTokenManager.getUserToken()),
            loginVisible: false,

            //搜索
            searchValue:'',
            searchResult:[],
        }
    }

    fetchLogin = (params = {}) => {
        MyHostPost('/user/login/', {...params}, true).then(({json}) => {
            if (json.code === 0) {
                const {remember} = params;
                const mode = remember ? StorageMode.local:StorageMode.session;
                MyUserTokenManager.setUserToken(mode,json.data[0]);
                this.setState({
                    userInfo:json.data[0],
                    login: true,
                });
                MyNotification.success("登陆成功");
            } else {
                throw json;
            }
        }).catch((error) => {
            MyNotification.error("登陆失败");
            console.log('error',error);
        });
    };

    onCollapse = (collapsed) => {
        this.setState({
            collapsed,
        });
    };

    renderMenu = () => {
        const {firstLevel} = this.props.match.params;
        const { login,userInfo } = this.state;
        const bookHref = login ? `/home/book/${userInfo.userId}` : `/home/book/0`;
        let items = [];
        items.push(
            <Menu.Item key="book">
                <Icon type="file" />
                <Link to={bookHref} style={{display:"inline-block"}}>图书</Link>
            </Menu.Item>
        );
        if(login){
            items.push(
                <SubMenu
                    key="info"
                    title={
                        <span>
                        <Icon type="user"/>
                        <span>个人</span>
                    </span>
                    }
                >
                    <Menu.Item key="own-book">
                        <Icon type="book" />
                        <Link to={`/home/own-book/${userInfo.userId}`} style={{display:"inline-block"}}>个人书籍管理</Link>
                    </Menu.Item>
                    <Menu.Item key="own-info">
                        <Icon type="info-circle" />
                        <Link to={`/home/own-info/${userInfo.userId}`} style={{display:"inline-block"}}>个人信息管理</Link>
                    </Menu.Item>
                </SubMenu>
            );
        }
        return (
            <Menu
                mode="inline"
                defaultSelectedKeys={['book']}
                selectedKeys={[firstLevel]}
            >
                {items}
            </Menu>
        );
    };

    handleLogin = (values) => {
        this.setState({
            loading: true,
        });
        setTimeout(() => {
            this.setState({
                loading: false,
                loginVisible: false
            });
        }, 1000);
        this.fetchLogin(values);
    };

    handleQuit = () => {
        MyUserTokenManager.removeUserToken();
        this.setState({
            login: false,
        });
    };

    handleSearch = () => {
        if(this.props.match.params.firstLevel !== 'book-search'){
            history.push({pathname:'/home/book-search/'});
        }
    };

    setLoginModalVisible = (setValue) => {
        this.setState({loginVisible:setValue});
    };

    render() {
        const { login, loginVisible, userInfo, loading } = this.state;
        const menu = (
            login ?
                <Menu>
                    <Menu.Item key="1" onClick={this.handleQuit}>
                        <Icon type="user" />
                        退出登录
                    </Menu.Item>
                </Menu>
                :
                <Menu>
                    <Menu.Item key="1" onClick={()=>this.setLoginModalVisible(true)}>
                        <Icon type="user" />
                        登陆账号
                    </Menu.Item>
                </Menu>
        );
        const notLogin = <Tooltip title='点击以登录'><span onClick={()=>this.setLoginModalVisible(true)}>未登录</span></Tooltip>;
        const userNameDisplay = login?userInfo.userName:notLogin;

        return(
            <div>
                <div
                    className="custom-header"
                    style={{height:64,boxShadow:'0 5px 10px rgba(0,0,0,0.04)'}}
                >
                    <div className="logo" style={{float:'left',color:'#808080',height:64,width:200,textAlign:'center',paddingTop:15}}>
                        <span style={{fontSize:20,fontWeight:20,color:'#001529'}}>图书管理系统</span>
                    </div>
                    <Divider type={'vertical'} style={{margin:'20px 0px',height:24}}/>
                    <div className="search-input" style={{display:'inline',height:30,margin:'30px 0px 0px 18px'}}>
                        <Icon
                            type={"search"}
                            style={{color:'rgba(0, 0, 0, 0.2)',fontSize:14}}
                            onClick={()=>this.handleSearch()}
                        />
                        <input
                            className="header-search"
                            placeholder="Search here by book name"
                            value={this.state.searchValue}
                            onChange={ e => this.setState({searchValue:e.target.value})}
                            onKeyPress={e => {
                                // Enter键触发
                                if(e.charCode === 13){
                                    this.handleSearch();
                                }
                            }}
                        />
                    </div>
                    <Dropdown overlay={menu} placement="bottomCenter">
                        <Avatar size="primary" icon="user" style={{float:'right',marginRight:35, marginTop:15}}/>
                    </Dropdown>
                    <div style={{float:'right',height:64,marginRight:20,paddingTop:20}}>{userNameDisplay}</div>
                </div>
                <div style={{marginTop:15,}}>
                    <Layout style={{ minHeight: '100vh' }}>
                        <Sider
                            theme="light"
                            // collapsible
                            // collapsed={this.state.collapsed}
                            // onCollapse={this.onCollapse}
                            style={{minHeight:981}}
                        >
                            {this.renderMenu()}
                        </Sider>
                        <Content>
                            <Layout className="mainLayout" style={{ padding: '24px 0', background: '#fff', minHeight:'100%' }}>
                                <Content style={{ padding: '0 24px',minHeight:780 }}>
                                    <Switch>
                                        <Route path="/home/book/:userId" component={MyDefault} />
                                        <Route path="/home/own-book/:userId" component={MyBook} />
                                        <Route path="/home/own-info/:userId" component={MyInfo} />
                                        <Route path="/home/book-search/" render={()=>(<MySearch searchValue={this.state.searchValue}/>)}/>
                                        <Route path="/home/book-info/:bookId" component={MyBookDetail} />
                                    </Switch>
                                </Content>
                            </Layout>
                        </Content>
                    </Layout>
                </div>
                <div
                    className="custom_footer"
                    style={{textAlign: 'center',height:80,background:'#dadada',paddingTop:33}}
                >
                    ©2019 Created by Ye
                </div>
                <MyLoginModalEx
                    visible={loginVisible}
                    setVisible={this.setLoginModalVisible}
                    onLogin={this.handleLogin}
                />
            </div>
        )
    }

}

export default MyLayout;
