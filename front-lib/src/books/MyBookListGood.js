import React, { Component } from 'react';
import {List} from "antd";
import {Link} from 'react-router-dom';

class MyBookListGood extends Component {

    constructor(props) {
        super(props);
        this.state = {
            loading: false,
        }
    }

    render() {

        const data = this.props.listGood;

        return(
            <div>
                <List
                    style={{width:800}}
                    itemLayout="vertical"
                    size="large"
                    dataSource={data}
                    renderItem={item => (
                        <List.Item
                            key={item.title}
                            actions={[<Link
                                style={{float:'right'}}
                                key={item.id}
                                to={`/home/book-info/${item.id}`}
                            >详情</Link>]}
                        >
                            <List.Item.Meta
                                title={<a href={item.href}>{item.title}</a>}
                                description={item.description}
                            />
                            <div>{item.content}</div>
                        </List.Item>
                    )}
                />
            </div>
        )
    }

}


export default MyBookListGood;
