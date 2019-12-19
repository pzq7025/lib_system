import React, { Component } from 'react';
import {Avatar, Divider, List, Popconfirm} from "antd";
import {Link} from 'react-router-dom';
import MyHostPost from "../util/MyHostPost";
import MyNotification from "../util/MyNotification";

class MyBook extends Component {

    constructor(props) {
        super(props);
        this.state = {
            data:[],
            total:-1,
            current:1,
            pageSize:10,
            loading:false,
        }
    }

    componentWillMount(){
        const {userId} = this.props.match.params;
        const {pageSize} = this.state;
        this.fetchShowBook({userId,pageSize,skipPage:1});
    }

    componentWillReceiveProps(nextProps){
        const {userId} = this.props.match.params;
        const {pageSize} = this.state;
        this.fetchShowBook({userId,pageSize,skipPage:1});
    }

    fetchShowBook = (params = {}) => {
        this.setState({loading: true});
        MyHostPost('/user/searchOwnBook/', {...params}, true).then(({json}) => {
            if (json.code === 0) {
                this.setState({
                    loading: false,
                    data: json.rows,
                    total:json.total,
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

    fetchBookCancelBorrow = (params = {}) => {
        this.setState({loading: true});
        MyHostPost('/user/bookCancelBorrow/', {...params}, true).then(({json}) => {
            if (json.code === 0) {
                this.setState({
                    loading: false,
                });
                MyNotification.success("取消成功");
            } else {
                throw json;
            }
        }).catch((error) => {
            this.setState({loading: false});
            MyNotification.error("取消失败");
            console.log(error);
        })
    };

    fetchBookContinueBorrow = (params = {}) => {
        this.setState({loading: true});
        MyHostPost('/user/bookBorrowContinue/', {...params}, true).then(({json}) => {
            if (json.code === 0) {
                this.setState({
                    loading: false,
                });
                MyNotification.success("续订成功，时间延长三十天");
            } else {
                throw json;
            }
        }).catch((error) => {
            this.setState({loading: false});
            MyNotification.error("续订失败");
            console.log(error);
        })
    };

    bookContinueBorrow = (id) => {
        this.fetchBookContinueBorrow({
            userId: this.props.match.params.userId,
            bookId: id,
        })
    };

    bookCancelBorrow = (id) => {
        this.fetchBookCancelBorrow({
            userId: this.props.match.params.userId,
            bookId: id,
        })
    };

    handlePageChange = (nextPage) => {
        const {userId} = this.props.match.params;
        const {pageSize} = this.state;
        this.fetchShowBook({userId,pageSize,skipPage:nextPage-1});
        this.setState({current:nextPage});
    };

    render() {
        const { data,current,total,pageSize } = this.state;

        return(
            <div>
                <span style={{paddingTop: 20, fontSize:26, marginRight:20}}>
                    我的订阅
                </span>
                <Divider/>
                <List
                    itemLayout="horizontal"
                    dataSource={data}
                    pagination={{
                        onChange: this.handlePageChange,
                        current: current,
                        total: total,
                        pageSize: pageSize,
                        size:'small'
                    }}
                    renderItem={item => (
                        <List.Item>
                            <List.Item.Meta
                                title={<Link
                                    key={item.id}
                                    to={`/home/book-info/${item.id}`}
                                >{item.title}</Link>}
                                description={item.description}
                            />
                            <div>剩余天数：{item.time}天</div>
                            <List.Item.Meta
                                title={
                                    <div>
                                        <Link key="list-loadmore-edit" onClick={()=>this.bookContinueBorrow(item.id)}>续订</Link>
                                        &nbsp;/&nbsp;
                                        <Link key="list-loadmore-more" onClick={()=>this.bookCancelBorrow(item.id)}>取消订阅</Link>
                                    </div>
                                }
                            />
                        </List.Item>
                    )}
                />
            </div>
        )
    }


}


export default MyBook;
