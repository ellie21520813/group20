import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useSearchParams } from 'react-router-dom';
import { Avatar, Col, Row, Space, TablePaginationConfig, message } from 'antd';
import type { MenuProps } from 'antd';
import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
import * as S from '@app/components/tables/Tables/Tables.styles';
import { httpApi } from '@app/api/http.api';
import { readToken } from '@app/services/localStorage.service';
import { DeviceConfigTable } from '@app/components/tables/DeviceTable/ConfigTable';
import Column from 'antd/lib/table/Column';
import { notificationController } from '@app/controllers/notificationController';

interface IDevice {
  id: string;
  ip: string;
  hostname: string;
  name: string;
}

const DeviceDetailsPage: React.FC = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [devices, setDevices] = useState<Record<string, IDevice>>({});
  const [deviceId, setDeviceID] = useState<string>('');

  useEffect(() => {
    const deviceIDParam = searchParams.get('id');
    setDeviceID(deviceIDParam || '');
  });
  

  return (
    <>
      <PageTitle>Device</PageTitle>
      <S.TablesWrapper>
        <S.Card id="devices" key="device-table" padding="1.25rem 1.25rem 1.25rem">
          <Row gutter={16}>
            <Col span={10}>
              <DeviceConfigTable device_id={deviceId} />
            </Col>
            <Col span={14}>
              
            </Col>
          </Row>
        </S.Card>
      </S.TablesWrapper>
    </>
  );
};
export default DeviceDetailsPage;
