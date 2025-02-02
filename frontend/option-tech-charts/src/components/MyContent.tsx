import { Layout, Select } from "antd";
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
  const [selectedChart, setSelectedChart] = useState("GEX"); // ...OI, DEX
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

  let chartTitle = "",
    chartDesc = "Click labels to hide/unhide the data.";

  switch (selectedChart) {
    case "OI":
      chartTitle += "Open interest: ";
      chartDesc += ` \n*Negative numbers represent OI of puts. `;
      break;
    case "DEX":
      chartTitle += "Delta exposure: ";
      break;
    case "GEX":
      chartTitle += "Gamma exposure: ";
  }

  const selectMaturity = (
    <Select
      defaultValue="month"
      onChange={handleMaturitySelect}
      style={{ width: "10rem" }}
      options={[
        { value: "month", label: "Current month" },
        { value: "0dte", label: "0DTE" },
        { value: "week", label: "Current week", disabled: true },
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
        <div className="chart-title">
          <h3>
            {chartTitle}
            {selectMaturity}
          </h3>
          <p>Update at GMT 05:00 every weekdays.</p>
        </div>
        <Chart
          selectedChart={selectedChart}
          symbol={selectedSymbol}
          maturity={selectedMaturity}
        />
        <div className="chart-desc">
          <i>{chartDesc}</i>
        </div>
      </Content>
      <MyFooter />
    </Layout>
  );
};

export default MyContent;
