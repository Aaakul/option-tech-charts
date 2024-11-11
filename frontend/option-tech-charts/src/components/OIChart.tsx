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
        backgroundColor: "#00FF00", // green
        data: [],
      },
      {
        label: "Put Options",
        backgroundColor: "#FF0000", // red
        data: [],
      },
    ],
  });

  useEffect(() => {
    // fetch JSON data
    const fetchData = async () => {
      try {
        const response = await fetch("/data/SPY_OI_chart_data.json");
        const data: OptionData[] = await response.json();
        // get chart data
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
              backgroundColor: "#00FF00",
              data: callData,
            },
            {
              label: "Put Options",
              backgroundColor: "#FF0000",
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

export default OIChart;
