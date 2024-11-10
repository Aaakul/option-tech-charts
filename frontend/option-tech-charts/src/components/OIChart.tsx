import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import { ChartOptions } from "chart.js/auto";
import {
  Chart as ChartJS,
  registerables,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

// 注册所有必要的图表组件
ChartJS.register(
  ...registerables,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

interface OptionData {
  strike: number;
  call_open_interest: number;
  put_open_interest: number;
}

const OIChart = () => {
  const [chartData, setChartData] = useState<{
    labels: number[];
    datasets: {
      label: string;
      backgroundColor: string;
      data: number[];
    }[];
  }>({
    labels: [],
    datasets: [
      {
        label: "Call Options",
        backgroundColor: "#00FF00", // 绿色
        data: [],
      },
      {
        label: "Put Options",
        backgroundColor: "#FF0000", // 红色
        data: [],
      },
    ],
  });

  useEffect(() => {
    // 从本地JSON文件获取数据
    const fetchData = async () => {
      try {
        const response = await fetch("/data/SPY_chart_data_11.json");
        const data: OptionData[] = await response.json();
        // 准备图表数据
        data.sort((a, b) => b.strike - a.strike);
        const labels = data.map((item) => item.strike);
        const callData = data.map((item) => item.call_open_interest);
        const putData = data.map((item) => item.put_open_interest);

        const newChartData = {
          type: "bar",
          labels: labels,
          datasets: [
            {
              label: "Call Options",
              backgroundColor: "#00FF00", // 绿色
              data: callData,
            },
            {
              label: "Put Options",
              backgroundColor: "#FF0000", // 红色
              data: putData,
            },
          ],
        };

        setChartData(newChartData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [chartData.labels.length]);

  const options: ChartOptions<"bar"> = {
    maintainAspectRatio: false,
    responsive: true,
    indexAxis: "y", // 将索引轴设置为 Y 轴
    scales: {
      x: {
        stacked: true,
        ticks: {
          display: false, // 隐藏 X 轴的刻度线和坐标标签
        },
        grid: {
          display: false, // 隐藏 X 轴的网格线
        },
      },
      y: {
        stacked: true,
        beginAtZero: true,
        ticks: {
          maxTicksLimit: 15, // 设置 Y 轴最多显示 5 个刻度
        },
        grid: {
          display: false, // 隐藏 Y 轴的网格线
        },
      },
    },
    plugins: {
      legend: {
        display: true,
      },
    },
  };

  return (
    <div className="chart-container">
      {chartData.labels.length > 0 && (
        <Bar data={chartData} options={options} />
      )}
    </div>
  );
};

export default OIChart;
