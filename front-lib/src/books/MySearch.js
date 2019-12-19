import React, { Component,Fragment } from 'react';
import { Divider, Input, List } from 'antd';
import {Link} from 'react-router-dom';
import PropTypes from 'prop-types'
import MyHostPost from '../util/MyHostPost'
import MyNotification from '../util/MyNotification'

const { Search } = Input;

class MySearch extends Component {

    constructor(props) {
        super(props);
        this.state = {
            result:[],
        }
    }

    componentWillMount() {
        this.fetch({bookName:this.props.searchValue});
    }

    componentWillReceiveProps(nextProps, nextContext) {
        if(this.props.searchValue !== nextProps.searchValue){
            this.fetch({bookName:nextProps.searchValue});
        }
    }

    fetch = (parameters = {}) => {
        MyHostPost(
            '/search/searchBook/',
            {...parameters},
            true
        ).then(({json})=>{
            if(json.code === 0){
                this.setState({result:json.info});
            }else
                throw json;
        }).catch((error) => {
            MyNotification.error("搜索失败");
            console.log('error',error);
        });
    };

    render() {
        const {result} = this.state;
        return (
            <Fragment>
                <span style={{paddingTop: 20, fontSize:26, marginRight:20}}>
                    搜索结果
                </span>
                {/*<Search*/}
                {/*style={{float:'right',width: 200}}*/}
                {/*placeholder = "Search"*/}
                {/*/>*/}
                <Divider/>
                <List
                    style={{width:800}}
                    itemLayout="vertical"
                    size="large"
                    dataSource={result}
                    renderItem={item => (
                        <List.Item
                            key={item.title}
                            actions={[
                                <Link
                                    style={{float:'right'}}
                                    key={item.id}
                                    to={`/home/book-info/${item.id}`}
                                >详情</Link>
                            ]}
                        >
                            <List.Item.Meta
                                title={<a href={item.href}>{item.title}</a>}
                                description={item.description}
                            />
                            <div>{item.content}</div>
                        </List.Item>
                    )}
                />
            </Fragment>
        );
    }

}

MySearch.propTypes = {
    searchValue:PropTypes.string.isRequired,
};

export default MySearch;
