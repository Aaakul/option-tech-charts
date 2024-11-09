import { Layout } from "antd";
import { Content } from "antd/es/layout/layout";
import React from "react";
import MyHeader from "./MyHeader";
import MyFooter from "./MyFooter";
import Charts from "./Charts";

interface MyContentProps {
  isDarkTheme: boolean;
  onToggleTheme: () => void;
}

const MyContent: React.FC<MyContentProps> = ({
  isDarkTheme,
  onToggleTheme,
}) => {
  const labels = [
    "一月份",
    "二月份",
    "三月份",
    "四月份",
    "五月份",
    "六月份",
    "七月份",
  ]; // 设置 X 轴上对应的标签
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "",
        data: [65, 59, 80, 81, 56, 55, 40],
        // backgroundColor: [
        //   // 设置每个柱形图的背景颜色
        //   "rgba(255, 99, 132, 0.2)",
        //   "rgba(255, 159, 64, 0.2)",
        //   "rgba(255, 205, 86, 0.2)",
        //   "rgba(75, 192, 192, 0.2)",
        //   "rgba(54, 162, 235, 0.2)",
        //   "rgba(153, 102, 255, 0.2)",
        //   "rgba(201, 203, 207, 0.2)",
        // ],
        // borderColor: [
        //   //设置每个柱形图边框线条颜色
        //   "rgb(255, 99, 132)",
        //   "rgb(255, 159, 64)",
        //   "rgb(255, 205, 86)",
        //   "rgb(75, 192, 192)",
        //   "rgb(54, 162, 235)",
        //   "rgb(153, 102, 255)",
        //   "rgb(201, 203, 207)",
        // ],
        borderWidth: 1, // 设置线条宽度
      },
    ],
  };

  return (
    <Layout>
      <MyHeader isDarkTheme={isDarkTheme} onToggleTheme={onToggleTheme} />
      <Content style={{ margin: "0 16px" }}>
        <div className="chart-desc" style={{ margin: "16px 0" }}>
          description
        </div>
          <Charts chartData={chartData} />
      </Content>
      <MyFooter />
    </Layout>
  );
};

export default MyContent;
