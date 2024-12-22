import React from 'react';
import { useTranslation } from 'react-i18next';
import { Tables } from '@app/components/tables/Tables/Tables';
import { PageTitle } from '@app/components/common/PageTitle/PageTitle';
import { UsersTables } from '@app/components/tables/UsersTable/UsersTable';
import * as S from '@app/components/tables/Tables/Tables.styles';

const UsersPage: React.FC = () => {
  const { t } = useTranslation();
  return (
    <>
      <PageTitle>{t('common.userPage')}</PageTitle>
      <S.TablesWrapper>
        <S.Card id="basic-table" title={t('tables.userTable')} padding="1.25rem 1.25rem 1.25rem">
          <UsersTables />
        </S.Card>
      </S.TablesWrapper>
    </>
  );
};
export default UsersPage;
