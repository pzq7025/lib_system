import React, { Component } from 'react';
import {Input, Divider} from "antd";
import MyBookListGood from './MyBookListGood';
import MyBookListBorrow from './MyBookListBorrow';
import MyHostPost from "../util/MyHostPost";
import MyNotification from "../util/MyNotification";

const { Search } = Input;

class MyDefault extends Component {

    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            listGood: [],
            listBorrow: [],
            login: true,
        }
    }

    componentWillMount(){
        this.fetch({
            userId: this.props.match.params.userId,
        });
    }

    fetch = (params = {}) => {
        this.setState({loading: true});
        MyHostPost('/search/home/', {...params}, true).then(({json}) => {
            if (json.code === 0) {
                this.setState({
                    loading: false,
                    listGood: json.listGood,
                    listBorrow: json.listBorrow,
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

    render() {
        const { listGood, listBorrow } = this.state;

        return(
            <div>
                <span style={{paddingTop: 20, fontSize:26, marginRight:20}}>
                    所有图书
                </span>
                {/*<Search*/}
                {/*style={{float:'right',width: 200}}*/}
                {/*placeholder = "Search"*/}
                {/*onSearch = {(value) => {this.props.history.push({pathname:`/home/book-search/${value}`})}}*/}
                {/*/>*/}
                <Divider/>
                <div>
                    <div style={{float:'left'}}>
                        <h2>图书好评排行榜</h2>
                        <MyBookListGood
                            style={{width:800}}
                            listGood={listGood}
                        />
                    </div>
                    <div style={{float:'right'}}>
                        <h2>图书借阅榜</h2>
                        <MyBookListBorrow
                            style={{width:600,float:'right'}}
                            listBorrow={listBorrow}
                        />
                    </div>
                </div>
            </div>
        )
    }


}

export default MyDefault;