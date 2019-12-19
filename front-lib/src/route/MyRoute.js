import React, { Component } from 'react';
import { HashRouter,Route,Switch,Redirect } from "react-router-dom";
import MyLayout from '../MyLayout';
import history from './history'
import MyUserTokenManager from "../util/MyUserTokenManager";


class MyRoute extends Component {

    render() {
        const login = Boolean(MyUserTokenManager.getUserToken());
        const userInfo = MyUserTokenManager.getUserToken();
        const bookHref = login ? `/home/book/${userInfo.userId}` : `/home/book/0`;
        return (
            <HashRouter history={history}>
                <div style={{height: '100%'}}>
                    <Switch>
                        <Route path="/home/:firstLevel" render={(props)=>(<MyLayout {...props}/>)}/>
                        <Redirect to={bookHref}/>
                    </Switch>
                </div>
            </HashRouter>
        )
    }

}

export default MyRoute;
