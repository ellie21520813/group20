import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button, Col, Modal, Row, Space, message, Upload } from 'antd';
import { DeliveredProcedureOutlined, InboxOutlined } from '@ant-design/icons';
import { BaseButtonsForm } from '@app/components/common/forms/BaseButtonsForm/BaseButtonsForm';
import { notificationController } from '@app/controllers/notificationController';

import { Input } from '@app/components/common/inputs/Input/Input';
import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
import { LSTMTable } from '@app/components/tables/LSTMTable/LSTMTable';
import type { RcFile, UploadFile, UploadProps } from 'antd/es/upload/interface';

import * as S from '@app/components/tables/Tables/Tables.styles';
import { readToken } from '@app/services/localStorage.service';
import { deleteFile } from '@app/api/files.api';
import { training, LSTM } from '@app/api/lstm.api';

const { Dragger } = Upload;

const LSTMPage: React.FC = () => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [share, setShare] = useState(false);
  const [fileUrl, setFileURL] = useState('');
  const [isFieldsChanged, setFieldsChanged] = useState(false);
  const [isLoading, setLoading] = useState(false);
  const [initialValues, setInitialValues] = useState({
    batch_size: 100,
    epochs: 100,
    loss_fun: 'mean_squared_error',
    optimizer: 'adam',
    look_back: 10,
    file: fileUrl,
  });
  const layout = {
    labelCol: { span: 24 },
    wrapperCol: { span: 24 },
  };

  const showModal = () => {
    setOpen(true);
  };

  const handleCancel = () => {
    setOpen(false);
  };

  const onFinish = (
    values = {
      name: '',
      batch_size: 0,
      description: '',
      epochs: 0,
      file_url: '',
      look_back: 0,
      loss_fun: '',
      optimizer: '',
    },
  ) => {
    setLoading(true);
    setTimeout(() => {
      setFieldsChanged(false);
      setLoading(false);
      const data: LSTM = { ...values, split: 0.9 };
      training(data)
        .then((res) => {
          notificationController.success({ message: res.data.message });
        })
        .catch((err) => {
          notificationController.error({ message: err.toString() });
        });
    }, 1000);
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
        setInitialValues({ ...initialValues, file: info.file.response.file_id });
      }
      if (status === 'done') {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
    onRemove(e) {
      deleteFile(e.response['file_id']).then((response) => {
        const file_info = response.data;
        message.success(`${file_info['name']} removed`);
        setFileURL('');
      });
    },
  };

  return (
    <>
      <PageTitle>LSTM</PageTitle>
      <S.TablesWrapper>
        <S.Card
          id="lstm-table"
          key="lstm-table"
          title="LSTM Table"
          padding="1.25rem 1.25rem 1.25rem"
          extra={
            <Button type="primary" onClick={showModal} icon={<DeliveredProcedureOutlined />}>
              New Model
            </Button>
          }
        >
          <LSTMTable />
        </S.Card>
      </S.TablesWrapper>
      <Modal
        title="Training Config"
        open={open}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        okButtonProps={{ style: { display: 'none' } }}
        cancelButtonProps={{ style: { display: 'none' } }}
      >
        <BaseButtonsForm
          {...layout}
          name="controlForm"
          isFieldsChanged={isFieldsChanged}
          initialValues={initialValues}
          footer={
            <BaseButtonsForm.Item>
              <Button htmlType="submit" type="primary" loading={isLoading}>
                {t('common.submit')}
              </Button>
            </BaseButtonsForm.Item>
          }
          onFinish={onFinish}
          onFieldsChange={() => {
            setFieldsChanged(true);
          }}
        >
          <Space direction="vertical" style={{ display: 'flex' }}>
            <BaseButtonsForm.Item name="file_dragger" valuePropName="file">
              <Dragger {...uploadProps}>
                <p className="ant-upload-drag-icon">
                  <InboxOutlined />
                </p>
                <p className="ant-upload-text">{t('forms.validationFormLabels.clickToDrag')}</p>
              </Dragger>
            </BaseButtonsForm.Item>
            <BaseButtonsForm.Item
              name="file_url"
              label="File URL:"
              rules={[{ required: true, message: 'File is required' }]}
            >
              <Input />
            </BaseButtonsForm.Item>
            <BaseButtonsForm.Item name="name" label="Name" rules={[{ required: true, message: 'Name is required' }]}>
              <Input />
            </BaseButtonsForm.Item>
            <BaseButtonsForm.Item name="description" label="Description">
              <Input />
            </BaseButtonsForm.Item>
            <BaseButtonsForm.Item
              name="look_back"
              label="Look back"
              rules={[{ required: true, message: 'Look back is required' }]}
            >
              <Input />
            </BaseButtonsForm.Item>
            <BaseButtonsForm.Item
              name="loss_fun"
              label="Loss Func"
              rules={[{ required: true, message: 'Loss Func is required' }]}
            >
              <Input />
            </BaseButtonsForm.Item>
            <BaseButtonsForm.Item
              name="optimizer"
              label="Optimizer"
              rules={[{ required: true, message: 'Optimizer is required' }]}
            >
              <Input />
            </BaseButtonsForm.Item>
            <BaseButtonsForm.Item
              name="epochs"
              label="Epoch"
              rules={[{ required: true, message: 'Epoch is required' }]}
            >
              <Input />
            </BaseButtonsForm.Item>
            <BaseButtonsForm.Item
              name="batch_size"
              label="Batch Size"
              rules={[{ required: true, message: 'Batch Size is required' }]}
            >
              <Input />
            </BaseButtonsForm.Item>
          </Space>
        </BaseButtonsForm>
      </Modal>
    </>
  );
};
export default LSTMPage;
