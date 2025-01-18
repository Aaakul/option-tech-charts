import {
  SunOutlined,
  MoonOutlined,
  MenuUnfoldOutlined,
} from "@ant-design/icons";
import { Button, Dropdown, MenuProps, Radio } from "antd";
import { Header } from "antd/es/layout/layout";
import React from "react";

interface TitleProps {
  isDarkTheme: boolean;
  onToggleTheme: () => void;
  onChartSelect: (chartType: string) => void;
  onSymbolSelect: (symbol: string) => void;
}

const MyHeader: React.FC<TitleProps> = ({
  isDarkTheme,
  onToggleTheme,
  onChartSelect,
  onSymbolSelect,
}) => {
  const items: MenuProps["items"] = [
    {
      label: <p>Open Interest</p>,
      key: "0",
      onClick: () => onChartSelect("OI"),
    },
    {
      label: <p>GEX</p>,
      key: "1",
      onClick: () => onChartSelect("GEX"),
    },
    {
      label: <p>DEX</p>,
      key: "2",
      onClick: () => onChartSelect("DEX"),
    },
  ];

  return (
    <Header>
      <div className="title-container">
        <Dropdown menu={{ items }}>
          <a
            href={`${process.env.PUBLIC_URL}`}
            onClick={(e) => e.preventDefault()}
          >
            <Button type="text" icon={<MenuUnfoldOutlined />} />
          </a>
        </Dropdown>
        <div className="title">
          <Radio.Group defaultValue="SPY" buttonStyle="solid" size={"large"}>
            <Radio.Button value="SPY" onClick={() => onSymbolSelect("SPY")}>
              SPY
            </Radio.Button>
            <Radio.Button value="QQQ" onClick={() => onSymbolSelect("QQQ")}>
              QQQ
            </Radio.Button>
          </Radio.Group>
        </div>
        <div className="toggle-theme" onClick={onToggleTheme}>
          {isDarkTheme ? <SunOutlined /> : <MoonOutlined />}
        </div>
      </div>
    </Header>
  );
};

export default MyHeader;
