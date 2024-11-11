import { GithubOutlined} from "@ant-design/icons";
import {  Space } from "antd";
import { Footer } from "antd/es/layout/layout";
import React from "react";

const MyFooter: React.FC = () => {
  return (
    <Footer>
      <Space>
        <a
          href="https://www.github.com/aaakul"
          target="_blank"
          rel="noopener noreferrer"
          className="main-card-extra"
        >
          <GithubOutlined />
        </a>
        <br />
        <a
          href="https://ant-design.antgroup.com/"
          target="_blank"
          rel="noopener noreferrer"
        >
          Made with antd and react-chartjs-2
        </a>
      </Space>
    </Footer>
  );
};

export default MyFooter;
