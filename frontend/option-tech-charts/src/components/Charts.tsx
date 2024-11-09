import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

interface Dataset<T> {
  label?: string;
  data: T[];
  backgroundColor?: string[];
  borderColor?: string[];
  borderWidth?: number;
}

interface ChartData<T> {
  labels: string[];
  datasets: Dataset<T>[];
}

interface ChartsProps {
  chartData: ChartData<number>;
}
const Charts: React.FC<ChartsProps> = ({ chartData }) => {
  return (
    <div className="chart-container">
      <Bar
        data={chartData}
        options={{
          indexAxis: "y", // 设置为 'y' 以创建水平条形图
          scales: {
            y: {
              beginAtZero: true, // 设置 y 轴从 0 开始
            },
          },
          plugins: {
            title: {
              display: true,
              text: "Cryptocurrency prices",
            },
            legend: {
              display: false,
              position: "bottom",
            },
          },
          responsive: true, // 确保图表响应式
          maintainAspectRatio: false, // 不保持宽高比
        }}
      />
    </div>
  );
};

export default Charts;
