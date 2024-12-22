import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button, Modal, Space, Card, notification } from 'antd';
import { UploadOutlined, PlusOutlined } from '@ant-design/icons';
import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
import { Input, TextArea } from '@app/components/common/inputs/Input/Input';

import { httpApi } from '@app/api/http.api';
import { createToken } from '@app/api/device-token.api';
import { readToken } from '@app/services/localStorage.service';
import { DeviceTokenTable } from '@app/components/tables/DeviceTokenTable/DeviceTokenTable';

import * as S from '@app/components/tables/Tables/Tables.styles';
import * as SU from '@app/pages/uiComponentsPages//UIComponentsPage.styles';
import { notificationController } from '@app/controllers/notificationController';

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
  const [tokenDescription, setTokenDescription] = useState(String);

  const showModal = () => {
    setOpen(true);
  };

  const handleCancel = () => {
    setOpen(false);
  };

  const handleCreateToken = () => {
    createToken(tokenDescription)
      .then((res) => {
        notificationController.success({ message: `${res.data['token']} created` });
        setTokenDescription('');
        setOpen(false);
      })
      .catch((err) => {
        notificationController.error({ message: err.message });
      });
  };

  return (
    <>
      <PageTitle>Devices</PageTitle>
      <S.TablesWrapper>
        {/* <S.Card id="discovered-devices" key="discovered-table" title="Discovered Devices" padding="1.25rem 1.25rem 0">
          <DiscoverTable/>
        </S.Card> */}
        <S.Card
          id="device-token"
          key="device-token-table"
          title="Tokens"
          padding="1.25rem 1.25rem 1.25rem"
          extra={
            <Button type="primary" shape="circle" size="small" icon={<PlusOutlined onClick={showModal} />}></Button>
          }
        >
          <DeviceTokenTable />
        </S.Card>
      </S.TablesWrapper>
      <Modal
        title="Add New Token"
        open={open}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        onOk={handleCreateToken}
      >
        <SU.InputsWrapper>
          Description
          <TextArea
            rows={4}
            value={tokenDescription}
            onChange={(e) => {
              setTokenDescription(e.target.value);
            }}
          />
        </SU.InputsWrapper>
      </Modal>
    </>
  );
};
export default DevicePage;
