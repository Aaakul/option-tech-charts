import { HeartFilled } from "@ant-design/icons";
import { Space } from "antd";
import { Footer } from "antd/es/layout/layout";
import React from "react";

const MyFooter: React.FC = () => {
  return (
    <Footer>
      <a
        href="https://ant-design.antgroup.com/"
        target="_blank"
        rel="noopener noreferrer"
      >
        <Space>
          Made with antd and
          <HeartFilled />
        </Space>
      </a>
    </Footer>
  );
};

export default MyFooter;
