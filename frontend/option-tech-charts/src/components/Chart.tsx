import React, { useEffect, useState } from "react";
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

// register chart components
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
  call_delta: number;
  put_delta: number;
  call_gamma: number;
  put_gamma: number;
  net_gamma: number;
  net_delta: number;
}

type DatasetField = keyof OptionData;

interface DatasetConfigItem {
  field: DatasetField;
  label: string;
  color: string;
}

type DatasetConfig = Record<string, DatasetConfigItem[]>;

// define bar color
const color = {
  blue: "#6495ED",
  green: "#00FF00",
  red: "#FF0000",
};

const datasetConfig: DatasetConfig = {
  OI: [
    { field: "call_open_interest", label: "Call Options", color: color.green },
    { field: "put_open_interest", label: "Put Options", color: color.red },
  ],
  DEX: [
    { field: "call_delta", label: "Call Delta", color: color.green },
    { field: "put_delta", label: "Put Delta", color: color.red },
    { field: "net_delta", label: "Net Delta", color: color.blue },
  ],
  GEX: [
    { field: "call_gamma", label: "Call Gamma", color: color.green },
    { field: "put_gamma", label: "Put Gamma", color: color.red },
    { field: "net_gamma", label: "Net Gamma", color: color.blue },
  ],
};

interface ChartProps {
  selectedChart: keyof DatasetConfig;
  symbol: string;
}

const Chart: React.FC<ChartProps> = ({ selectedChart, symbol }) => {
  const [chartData, setChartData] = useState<{
    labels: number[];
    datasets: {
      label: string;
      backgroundColor: string;
      data: number[];
    }[];
  }>({
    labels: [],
    datasets: [],
  });

  useEffect(() => {
    // fetch JSON data
    const fetchData = async () => {
      try {
        const response = await fetch(
          `${process.env.PUBLIC_URL}/data/${symbol}_data.json`
        );
        const data: OptionData[] = await response.json();
        // get chart data
        data.sort((a, b) => b.strike - a.strike);
        const labels = data.map((item) => item.strike);

        // select dataset
        const datasets = datasetConfig[selectedChart].map(
          (config: DatasetConfigItem) => ({
            label: config.label,
            backgroundColor: config.color,
            data: data.map((item) => item[config.field]),
          })
        );

        const newChartData = {
          labels: labels,
          datasets: datasets,
        };

        setChartData(newChartData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [selectedChart, symbol]);

  const options: ChartOptions<"bar"> = {
    maintainAspectRatio: false,
    responsive: true,
    indexAxis: "y", // set y as index axes
    scales: {
      x: {
        stacked: true,
        ticks: {
          display: false,
        },
        grid: {
          display: false,
        },
      },
      y: {
        stacked: true,
        beginAtZero: true,
        ticks: {
          maxTicksLimit: 15,
        },
        grid: {
          display: false,
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

export default Chart;
