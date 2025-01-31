import { Layout, Select, Space } from "antd";
import { Content } from "antd/es/layout/layout";
import React, { useState } from "react";
import MyHeader from "./MyHeader";
import MyFooter from "./MyFooter";
import Chart from "./Chart";

interface MyContentProps {
  isDarkTheme: boolean;
  onToggleTheme: () => void;
}

const MyContent: React.FC<MyContentProps> = ({
  isDarkTheme,
  onToggleTheme,
}) => {
  const [selectedChart, setSelectedChart] = useState("OI"); // ...DEX, GEX
  const [selectedSymbol, setSelectedSymbol] = useState("SPY");
  const [selectedMaturity, setSelectedMaturity] = useState("month");

  const handleChartSelect = (chartType: string) => {
    setSelectedChart(chartType);
  };

  const handleSymbolSelect = (symbol: string) => {
    setSelectedSymbol(symbol.toUpperCase());
  };

  const handleMaturitySelect = (value: string) => {
    setSelectedMaturity(value);
  };

  const chartTitle = `${selectedSymbol} option ${selectedChart}`;
  let chartDesc = " contracts total ",
    chartDescExtra =
      "Update at GMT 05:00 every weekdays. Click the data labels to hide/unhide the data.";

  switch (selectedChart) {
    case "OI":
      chartDesc +=
        "open interest.  *Negative numbers represent OI of puts. " +
        chartDescExtra;
      break;
    case "DEX":
      chartDesc += "delta exposure. " + chartDescExtra;
      break;
    case "GEX":
      chartDesc += "gamma exposure. " + chartDescExtra;
  }

  const selectMaturity = (
    <Select
      defaultValue="month"
      onChange={handleMaturitySelect}
      style={{ width: 128 }}
      options={[
        { value: "month", label: <p>Current month</p> },
        { value: "0dte", label: <p>0DTE</p> },
        { value: "week", label: <p>Current week</p>, disabled: true },
      ]}
    />
  );

  return (
    <Layout>
      <MyHeader
        isDarkTheme={isDarkTheme}
        onToggleTheme={onToggleTheme}
        onChartSelect={handleChartSelect}
        onSymbolSelect={handleSymbolSelect}
      />
      <Content>
        <h2>{chartTitle}</h2>
        <div className="chart-desc">
          <Space>
            {selectMaturity}
            <p>{chartDesc}</p>
          </Space>
        </div>
        <Chart
          selectedChart={selectedChart}
          symbol={selectedSymbol}
          maturity={selectedMaturity}
        />
      </Content>
      <MyFooter />
    </Layout>
  );
};

export default MyContent;
