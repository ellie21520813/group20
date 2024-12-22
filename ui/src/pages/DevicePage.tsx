import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button, Card, notification } from 'antd';
import { UploadOutlined, InboxOutlined } from '@ant-design/icons';

import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
import { DiscoverTable } from '@app/components/tables/DeviceTable/DiscoverTable';

import * as S from '@app/components/tables/Tables/Tables.styles';
import { httpApi } from '@app/api/http.api';
import { readToken } from '@app/services/localStorage.service';
import * as mqtt from 'mqtt';
import { Dictionary } from '@reduxjs/toolkit';
import { DeviceTable } from '@app/components/tables/DeviceTable/DeviceTable';

interface IDevice {
  id: string;
  ip: string;
  hostname: string;
  name: string;
}

const DevicePage: React.FC = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [share, setShare] = useState(false);
  const [devices, setDevices] = useState<Record<string, IDevice>>({});

  // useEffect(() => {
  //   httpApi.post(`${process.env.REACT_APP_API_URL}/v1/device/discover/all`).then((response) => {
  //     console.log(response);
  //     const file_info = response.data;
  //     message.success(`${file_info['name']} removed`);
  //   });
  // });

  // const clientId = "emqx_react_" + Math.random().toString(16).substring(2, 8);
  // const mqtthost = process.env.REACT_APP_MQTT_CONNECTION!
  // const username = process.env.REACT_APP_MQTT_USER!
  // const password = process.env.REACT_APP_MQTT_PASSWORD!
  // const mqttClient = mqtt.connect(mqtthost, {
  //   clientId, username, password
  // });

  // useEffect(() => {
  //   if (mqttClient){
  //     mqttClient.on("connect", () => {
  //       mqttClient.subscribe("edge/device/+");
  //     });
  //     mqttClient.on("message", (topic, message) => {
  //       const info: IDevice = JSON.parse(message.toString());
  //       setDevices(devices => (
  //         {
  //           ...devices,
  //           [info.id]: info
  //         }
  //       ))
  //       console.log(devices);
  //     });
  //   }
  // }, [mqttClient]);

  return (
    <>
      <PageTitle>Devices</PageTitle>
      <S.TablesWrapper>
        {/* <S.Card id="discovered-devices" key="discovered-table" title="Discovered Devices" padding="1.25rem 1.25rem 0">
          <DiscoverTable/>
        </S.Card> */}
        <S.Card id="devices" key="device-table" title="Devices" padding="1.25rem 1.25rem 1.25rem">
          <DeviceTable />
        </S.Card>
      </S.TablesWrapper>
    </>
  );
};
export default DevicePage;
