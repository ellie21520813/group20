import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button, Col, Modal, Row, Space, message, Upload, notification } from 'antd';
import { UploadOutlined, InboxOutlined } from '@ant-design/icons';
// import { Upload, UploadDragger } from '@app/components/common/Upload/Upload';
import { BaseButtonsForm } from '@app/components/common/forms/BaseButtonsForm/BaseButtonsForm';
import { notificationController } from '@app/controllers/notificationController';

import { Switch } from '@app/components/common/Switch/Switch';
import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
import { FilesTable } from '@app/components/tables/FilesTable/FilesTable';
import type { RcFile, UploadFile, UploadProps } from 'antd/es/upload/interface';

import * as S from '@app/components/tables/Tables/Tables.styles';
import { httpApi } from '@app/api/http.api';
import { readToken } from '@app/services/localStorage.service';

const { Dragger } = Upload;

const FilesPage: React.FC = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [share, setShare] = useState(false);

  const showModal = () => {
    setOpen(true);
  };

  const handleCancel = () => {
    setOpen(false);
  };

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: true,
    action: `${process.env.REACT_APP_API_URL}/v1/file/upload?share=${share}`,
    headers: {
      Authorization: `Bearer ${readToken()}`,
    },
    onChange(info) {
      const { status } = info.file;
      if (status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (status === 'done') {
        notificationController.success({ message: `${info.file.name} uploaded successfully.` });
      } else if (status === 'error') {
        notificationController.error({ message: `${info.file.name} upload failed.` });
      }
    },
    onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files);
    },
    onRemove(e) {
      console.log('Delete', e.response);
      httpApi.delete(`${process.env.REACT_APP_API_URL}/v1/file/${e.response['file_id']}`).then((response) => {
        const file_info = response.data;
        notificationController.success({ message: `${file_info['name']} removed` });
      });
    },
  };

  return (
    <>
      <PageTitle>{t('common.filesPage')}</PageTitle>
      <S.TablesWrapper>
        <S.Card
          id="file-table"
          key="file-table"
          title={t('common.filesTable')}
          padding="1.25rem 1.25rem 1.25rem"
          extra={
            <Button type="primary" shape="circle" size="small" icon={<UploadOutlined onClick={showModal} />}></Button>
          }
        >
          <FilesTable />
        </S.Card>
      </S.TablesWrapper>
      <Modal
        title="Upload File"
        open={open}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        okButtonProps={{ style: { display: 'none' } }}
        cancelButtonProps={{ style: { display: 'none' } }}
      >
        <Space direction="vertical" style={{ display: 'flex' }}>
          <Space>
            Share?
            <Switch
              checked={share}
              onChange={(e) => {
                setShare(e);
              }}
            />
          </Space>
          <Dragger {...uploadProps}>
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">{t('forms.validationFormLabels.clickToDrag')}</p>
            <p className="ant-upload-hint">{t('forms.validationFormLabels.supportSingle')}</p>
          </Dragger>
        </Space>
      </Modal>
    </>
  );
};
export default FilesPage;
