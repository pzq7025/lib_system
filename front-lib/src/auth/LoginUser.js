import React, { Component } from 'react';
import { Input, Tooltip, Icon, Button } from 'antd';
import { Link } from 'react-router-dom';


class LoginUser extends Component {
    render() {
        return(
            <div id="LoginUser">
                <div style={{position:"fixed", top:0, left:0, right:0, bottom:0, margin:"auto", width:200, height:200}}>
                    <Input
                        placeholder="Enter your username"
                        prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                        suffix={
                            <Tooltip title="Extra information">
                                <Icon type="info-circle" style={{ color: 'rgba(0,0,0,.45)' }} />
                            </Tooltip>
                        }
                    />
                    <Input.Password
                        style={{marginTop:"10px"}}
                        placeholder="input password"
                        prefix={<Icon type="key" style={{ color: 'rgba(0,0,0,.25)' }} />}
                    />
                    <Button
                        type="primary"
                        style={{marginTop:"10px",marginRight:"20px",marginLeft:"25px"}}
                    >
                        <Link to="/home/">登陆</Link>
                    </Button>
                    <Button
                        type="primary"
                        style={{marginTop:"10px"}}
                    >
                        <Link to="/logon">注册</Link>
                    </Button>
                </div>

            </div>
        )
    }

}

export default LoginUser;