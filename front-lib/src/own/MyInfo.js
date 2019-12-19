import React, { Component } from 'react';
import { Collapse, Icon, Input, Button, InputNumber, Tooltip } from 'antd'
import MyHostPost from "../util/MyHostPost";
import MyNotification from "../util/MyNotification";
import MyUserTokenManager from '../util/MyUserTokenManager'

const { Panel } = Collapse;

class MyInfo extends Component {

    constructor(props) {
        super(props);
        this.state = {
            info: MyUserTokenManager.getUserToken(),
            oldPassword: null,
            newPassword: null,
            checkPassword: null,
            money: null,
        }
    }

    // componentWillMount(){
    //     this.fetchShowInfo({
    //         userId: this.props.match.params.userId,
    //     });
    // }

    // componentWillReceiveProps(nextProps){
    //     this.fetchShowInfo({
    //         userId: this.props.match.params.userId,
    //     })
    // }

    // fetchShowInfo = (params = {}) => {
    //     this.setState({loading: true});
    //     MyHostPost('/searchInfo', {...params}, true).then(({json}) => {
    //         if (json.code === 0) {
    //             const {pagination} = this.state;
    //             pagination.total = json.total;
    //             this.setState({
    //                 loading: false,
    //                 info: json.info,
    //             });
    //         } else {
    //             throw json;
    //         }
    //     }).catch((error) => {
    //         this.setState({loading: false});
    //         MyNotification.error("加载数据失败");
    //     })
    // };

    handleMoneyAdd = () => {
        const { money } = this.state;
        const params = {
            userId: this.props.match.params.userId,
            money: money,
        };
        this.setState({loading: true});
        MyHostPost('/user/addMoney/', {...params}, true).then(({json}) => {
            if (json.code === 0) {
                this.setState({
                    loading: false,
                    info: json.info[0],
                    money: null,
                },()=>{
                    MyUserTokenManager.updateUserToken(json.info[0]);
                });
            } else {
                throw json;
            }
        }).catch((error) => {
            this.setState({loading: false});
            MyNotification.error("加载数据失败");
            console.log(error);
        })

    };

    handlePasswordChange = () => {
        const {oldPassword,newPassword,checkPassword} = this.state;
        if(newPassword === checkPassword){
            this.setState({loading: true});
            const params = {
                userId: this.props.match.params.userId,
                oldPassword,newPassword
            };
            MyHostPost('/user/changePassword/', {...params}, true).then(({json}) => {
                if (json.code === 0) {
                    this.setState({
                        loading: false,
                        oldPassword:'',
                        newPassword:'',
                        checkPassword:'',
                    });
                    MyNotification.success('密码修改成功');
                } else if(json.code === 1){
                    this.setState({loading:false});
                    MyNotification.error('旧密码输入错误');
                } else {
                    throw json;
                }
            }).catch((error) => {
                this.setState({loading: false});
                MyNotification.error("加载数据失败");
                console.log(error);
            })
        }else {
            MyNotification.error('两次输入的新密码不一致');
        }
    };


    render() {
        const { userName, userType, leftMoney } = this.state.info;
        const { money } = this.state;
        const panelStyle = {
            // background: '#f7f7f7',
            background:'#ffffff',
            borderRadius: 4,
            marginBottom: 24,
            border: 0,
            overflow: 'hidden',
        };
        const panelItemStyle = {
            margin:'10px 0px',
            fontSize:15
        }
        return(
            <div>
                <Collapse
                    defaultActiveKey={['1']}
                    bordered={false}
                    expandIcon={({ isActive }) => <Icon type="caret-right" rotate={isActive ? 90 : 0} />}
                >

                    <Panel header="个人信息" style={panelStyle} key="1">
                        <div style={{marginLeft:30}}>
                            <div style={panelItemStyle}>
                                <span className="title">姓名：</span>
                                <span>{userName}</span>
                            </div>
                            <div style={panelItemStyle}>
                                <span className="title">类别：</span>
                                <span>{userType===1?'本科生':'研究生'}</span>
                            </div>
                            <div style={panelItemStyle}>
                                <span className="title">剩余费用：</span>
                                <span>{leftMoney} 元</span>
                            </div>
                        </div>
                    </Panel>

                    <Panel header="修改密码" style={panelStyle} key="2">
                        <div style={{marginLeft:30}}>
                            <Input.Password
                                placeholder="Please type your old password"
                                style={{width:300, marginTop:10, display:'block'}}
                                value={this.state.oldPassword}
                                onChange={(e)=>{this.setState({oldPassword:e.target.value})}}
                            />
                            <Input.Password
                                placeholder="Please type your new password"
                                style={{width:300, marginTop:20, display:'block'}}
                                value={this.state.newPassword}
                                onChange={(e)=>{this.setState({newPassword:e.target.value})}}
                            />
                            <Input.Password
                                placeholder="Please type your new password again"
                                style={{width:300, marginTop:20, display:'block'}}
                                value={this.state.checkPassword}
                                onChange={(e)=>{this.setState({checkPassword:e.target.value})}}
                            />
                            <Button
                                onClick={this.handlePasswordChange}
                                type={"primary"}
                                style={{marginTop:20,width:64,marginLeft:236}}
                            >修改</Button>
                        </div>
                    </Panel>

                    <Panel header="续费缴费" style={panelStyle} key="3">
                        <div style={{marginLeft:30}}>
                            <div style={panelItemStyle}>
                                <span className="title">剩余费用：</span>
                                <span>{leftMoney} 元</span>
                            </div>
                            <div style={panelItemStyle}>
                                <span className="title">充值：</span>
                                <Tooltip title="下限为1元，上限为100元">
                                    <InputNumber style={{marginRight:15,width:176}} value={money} min={1} max={100} onChange={(value)=>{this.setState({money:value})}}/>
                                </Tooltip>
                                <Button onClick={this.handleMoneyAdd} style={{width:64}}>确定</Button>
                            </div>
                        </div>
                    </Panel>
                </Collapse>
            </div>
        )
    }


}

export default MyInfo;