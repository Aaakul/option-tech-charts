import { Layout } from "antd";
import { Content } from "antd/es/layout/layout";
import React from "react";
import MyHeader from "./MyHeader";
import MyFooter from "./MyFooter";
import OIChart from "./OIChart";

interface MyContentProps {
  isDarkTheme: boolean;
  onToggleTheme: () => void;
}

const MyContent: React.FC<MyContentProps> = ({
  isDarkTheme,
  onToggleTheme,
}) => {
  return (
    <Layout>
      <MyHeader isDarkTheme={isDarkTheme} onToggleTheme={onToggleTheme} />
      <Content style={{ margin: "0 16px" }}>
        <h2>Open Interest Chart</h2>
        <div className="chart-desc" style={{ margin: "16px 0" }}>
          description
        </div>
        <OIChart />
      </Content>
      <MyFooter />
    </Layout>
  );
};

export default MyContent;
