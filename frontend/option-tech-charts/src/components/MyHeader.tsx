import {
  SunOutlined,
  MoonOutlined,
  MenuUnfoldOutlined,
  GithubOutlined,
} from "@ant-design/icons";
import { Button, Dropdown, MenuProps, Radio, Space } from "antd";
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
        <div className="symbol-selector">
          <Radio.Group defaultValue="SPY" buttonStyle="solid" size={"large"}>
            <Radio.Button value="SPY" onClick={() => onSymbolSelect("SPY")}>
              SPY
            </Radio.Button>
            <Radio.Button value="QQQ" onClick={() => onSymbolSelect("QQQ")}>
              QQQ
            </Radio.Button>
          </Radio.Group>
        </div>
        <div className="icons">
          <Space size={'large'}>
            <a
              href="https://github.com/Aaakul/option-tech-charts"
              target="_blank"
              rel="noopener noreferrer"
            >
              <GithubOutlined />
            </a>
            <div className="toggle-theme" onClick={onToggleTheme}>
              {isDarkTheme ? <SunOutlined /> : <MoonOutlined />}
            </div>
          </Space>
        </div>
      </div>
    </Header>
  );
};

export default MyHeader;
