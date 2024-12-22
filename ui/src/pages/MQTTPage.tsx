import React from 'react';
import { Col, Row } from 'antd';
import { useTranslation } from 'react-i18next';
import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
import { Card } from '@app/components/common/Card/Card';
import { MQTTForm } from '@app/components/forms/DynamicForm/MQTTForm';
import { ControlForm } from '@app/components/forms/ControlForm/ControlForm';
import { ValidationForm } from '@app/components/forms/ValidationForm/ValidationForm';
import { StepForm } from '@app/components/forms/StepForm/StepForm';

const MQTTPage: React.FC = () => {
  const { t } = useTranslation();
  return (
    <>
      <PageTitle>MQTT Client</PageTitle>
      <Card id="dynamic-form" title="MQTT Client" padding="1.25rem">
        <MQTTForm />
      </Card>
    </>
  );
};

export default MQTTPage;
