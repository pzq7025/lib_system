import React, { Component } from 'react';
import { Button, Checkbox, Form, Icon, Input } from 'antd'
import PropTypes from 'prop-types'
import './MyLoginModalEx.css'

const FormItem = Form.Item;

class loginInputForm extends Component{
    constructor (props){
        super(props);
    }

    render () {
        const {getFieldDecorator} = this.props.form;
        return (
            <Form className="login-form">
                <FormItem>
                    {getFieldDecorator('userName', {
                        rules: [{required: true, message: '请输入用户名'}],
                    })(
                        <Input
                            prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            placeholder="Username"
                        />,
                    )}
                </FormItem>
                <FormItem>
                    {getFieldDecorator('password', {
                        rules: [{required: true, message: '请输入密码'}],
                    })(
                        <Input
                            prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            type="password"
                            placeholder="Password"
                        />,
                    )}
                </FormItem>
                <FormItem>
                    {getFieldDecorator('remember', {
                        valuePropName: 'checked',
                        initialValue: true,
                    })(<Checkbox>Remember me</Checkbox>)}
                </FormItem>
            </Form>
        );
    }
}

const MyLoginForm = Form.create({ name: 'normal_login' })(loginInputForm);

class MyLoginModalEx extends Component{
    constructor (props){
        super(props);
    }

    handleModalClose = (e) => {
        if(e.target.getAttribute('class')==='shadow-cover'){
            // 点击的是阴影遮罩层才会关闭modal
            this.props.setVisible(false);
        }
    };

    handleLogInButtonClick = () => {
        const formValue = this.formRef.getFieldsValue();
        this.formRef.validateFields((errors,values)=>{
            if(!errors){
                this.props.onLogin(formValue);
            }
        })
    };

    renderModal = () => {
        return (
            <div
                className="shadow-cover"
                // style={{
                //     position:'fixed',
                //     top: 0,
                //     right: 0,
                //     bottom: 0,
                //     left: 0,
                //     backgroundColor: 'rgba(0,0,0,0.3)',
                //     zIndex:1,
                //     display:'flex',
                //     justifyContent:'center',
                //     alignItems:'center'
                // }}
                onClick={(e)=>this.handleModalClose(e)}
            >
                <div
                    className="login-modal"
                    // style={{
                    //     position:'fixed',
                    //     width:350,
                    //     height:441,
                    //     zIndex:2,
                    //     borderRadius:10,
                    //     padding:'35px 20px 10px',
                    //     boxShadow:'0px 0px 5px 3px rgba(0,0,0,0.35)',
                    //     backgroundColor:'#fff'
                    // }}
                >
                    <h3 className="title">欢迎使用</h3>
                    <MyLoginForm ref={ref => this.formRef = ref}/>
                    <Button type="primary" style={{width:270}} onClick={()=>this.handleLogInButtonClick()}>Log In</Button>
                    <div
                        style={{
                            textAlign:'center',
                            marginTop:22,
                            color:'rgba(0,0,0,0.5)',
                            fontSize:13,
                            cursor:'pointer'
                        }}
                        onClick={()=>this.props.setVisible(false)}
                    >
                        --- Skip and Not log in ---
                    </div>
                </div>
            </div>
        ) ;
    };

    render () {
        return (
            this.props.visible && this.renderModal()
        )
    }
}

MyLoginModalEx.propTypes = {
    visible:PropTypes.bool.isRequired,
    setVisible:PropTypes.func.isRequired,
    onLogin:PropTypes.func.isRequired,
};

export default MyLoginModalEx;
