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
}

const MyHeader: React.FC<TitleProps> = ({ isDarkTheme, onToggleTheme }) => {
  const items: MenuProps["items"] = [
    {
      label: <a href="/">Open Interest</a>,
      key: "0",
    },
    {
      label: <a href="/">Coming soon: GEX</a>,
      key: "1",
      disabled: true,
    },
    {
      label: <a href="/">Coming soon: DEX</a>,
      key: "2",
      disabled: true,
    },
  ];

  return (
    <Header>
      <div className="title-container">
        <Dropdown menu={{ items }}>
          <a href="/#" onClick={(e) => e.preventDefault()}>
            <Button type="text" icon={<MenuUnfoldOutlined />} />
          </a>
        </Dropdown>
        <div className="title">
          <Radio.Group defaultValue="SPY" buttonStyle="solid" size={"large"}>
            <Radio.Button value="SPY">SPY</Radio.Button>
            <Radio.Button value="QQQ" disabled>
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
