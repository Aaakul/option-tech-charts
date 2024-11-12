import { GithubOutlined } from "@ant-design/icons";
import { Space } from "antd";
import { Footer } from "antd/es/layout/layout";
import React from "react";

const MyFooter: React.FC = () => {
  return (
    <Footer>
      <Space>
        <p>NON-INVESTMENT ADVICE</p>
        <a
          href="https://github.com/Aaakul/option-tech-charts"
          target="_blank"
          rel="noopener noreferrer"
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
