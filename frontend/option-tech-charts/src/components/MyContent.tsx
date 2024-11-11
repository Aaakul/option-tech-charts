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
  const chartTitle = "SPY Open Interest Chart of current month";
  const chartDesc = "Update at before-open every weekdays. *Negative numbers represent OI of puts";

  return (
    <Layout>
      <MyHeader isDarkTheme={isDarkTheme} onToggleTheme={onToggleTheme} />
      <Content>
        <h2>{chartTitle}</h2>
        <div className="chart-desc">{chartDesc}</div>
        <OIChart />
      </Content>
      <MyFooter />
    </Layout>
  );
};

export default MyContent;
