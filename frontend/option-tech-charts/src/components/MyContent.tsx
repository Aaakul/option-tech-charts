import { Layout } from "antd";
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

  const handleChartSelect = (chartType: string) => {
    setSelectedChart(chartType);
  };
  
  const handleSymbolSelect = (symbol: string) => {
    setSelectedSymbol(symbol.toUpperCase);
  };

  const chartTitle = `${selectedSymbol} option ${selectedChart}`;
  let chartDesc = "Current month contracts total ",
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
          <p>{chartDesc}</p>
        </div>
        <Chart selectedChart={selectedChart} symbol={selectedSymbol} />
      </Content>
      <MyFooter />
    </Layout>
  );
};

export default MyContent;
