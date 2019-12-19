import React, { Component } from 'react';
import {List} from "antd";
import {Link} from 'react-router-dom';

class MyBookListBorrow extends Component {

    constructor(props) {
        super(props);
        this.state = {
        }
    }

    render() {

        const data = this.props.listBorrow;

        return(
            <div>
                <List
                    style={{width:350}}
                    itemLayout="horizontal"
                    dataSource={data}
                    renderItem={item => (
                        <List.Item
                            actions={[
                                <Link
                                    style={{float:'right'}}
                                    key={item.id}
                                    to={`/home/book-info/${item.id}`}
                                >详情</Link>
                            ]}
                        >
                            <List.Item.Meta
                                title={<a href="https://ant.design">{item.title}</a>}
                                description={item.description}
                            />

                        </List.Item>
                    )}
                />
            </div>
        )
    }

}


export default MyBookListBorrow;
